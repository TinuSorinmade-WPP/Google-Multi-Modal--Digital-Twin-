import asyncio
import base64
import io
import os
import traceback
import json
import cv2
import pyaudio
import PIL.Image
import argparse
import wave
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 24000
RECEIVE_SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
MODEL = "models/gemini-2.0-flash-exp"
DEFAULT_MODE = "camera"

# Initialize Google Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
 raise ValueError("GEMINI_API_KEY is not set. Please set it in your environment variables.")

client = genai.Client(http_options={'api_version': 'v1alpha'}, api_key=GEMINI_API_KEY)
CONFIG = {"generation_config": {"response_modalities": ["AUDIO"],"speech_config": "Aoede"}}

pya = pyaudio.PyAudio()

class KnowledgeBaseManager:
 def __init__(self, knowledge_base_path):
     self.knowledge_base_path = knowledge_base_path
     self.knowledge_base = self.load_knowledge_base()

 def load_knowledge_base(self):
     """Load the knowledge base from a file."""
     try:
         if os.path.exists(self.knowledge_base_path):
             with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                 knowledge_base = f.read()
             print(f"Loaded knowledge base: {len(knowledge_base)} characters")
             return knowledge_base
         else:
             print(f"Knowledge base file not found: {self.knowledge_base_path}")
             return ""
     except Exception as e:
         print(f"Error loading knowledge base: {e}")
         return ""

 def get_context_prompt(self):
     prompt = "Here is some important knowledge to assist you:\n\n"
     prompt += self.knowledge_base
     return prompt

class AudioLoop:
 def __init__(self, video_mode=DEFAULT_MODE, knowledge_base_path=None):
     self.video_mode = video_mode
     self.audio_in_queue = None
     self.out_queue = None
     self.session = None
     self.audio_buffer = bytearray()
     self.response_counter = 0
     self.knowledge_manager = KnowledgeBaseManager(knowledge_base_path=knowledge_base_path)

 async def send_text(self):
     # Send initial context (knowledge base) to the model
     initial_context = self.knowledge_manager.get_context_prompt()
     print("Sending initial knowledge base to model...")
     await self.session.send(initial_context, end_of_turn=True)

     while True:
         try:
             text = await asyncio.to_thread(input, "message > ")
             if text.lower() == "q":
                 break

             # Send the message to the model
             await self.session.send(text, end_of_turn=True)
         except Exception as e:
             print(f"Error in send_text: {e}")
             traceback.print_exc()

 def _get_frame(self, cap):
     ret, frame = cap.read()
     if not ret:
         return None
     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
     img = PIL.Image.fromarray(frame_rgb)
     img.thumbnail([1024, 1024])
     image_io = io.BytesIO()
     img.save(image_io, format="jpeg")
     image_io.seek(0)
     return {"mime_type": "image/jpeg", "data": base64.b64encode(image_io.read()).decode()}

 async def get_frames(self):
     cap = await asyncio.to_thread(cv2.VideoCapture, 0)
     while True:
         frame = await asyncio.to_thread(self._get_frame, cap)
         if frame is None:
             break
         await asyncio.sleep(1.0)
         await self.out_queue.put(frame)
     cap.release()

 async def send_realtime(self):
     while True:
         msg = await self.out_queue.get()
         await self.session.send(msg)

 async def listen_audio(self):
     mic_info = pya.get_default_input_device_info()
     self.audio_stream = await asyncio.to_thread(
         pya.open,
         format=FORMAT,
         channels=CHANNELS,
         rate=SEND_SAMPLE_RATE,
         input=True,
         input_device_index=mic_info["index"],
         frames_per_buffer=CHUNK_SIZE
     )
     while True:
         data = await asyncio.to_thread(self.audio_stream.read, CHUNK_SIZE, exception_on_overflow=False)
         await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})

 async def receive_audio(self):
     output_filename = "response.wav"  # Fixed filename

     while True:
         audio_data = bytearray()

         try:
             async for response in self.session.receive():
                 if data := response.data:
                     # Accumulate audio data
                     audio_data.extend(data)
                     # Send to audio queue for real-time playback
                     self.audio_in_queue.put_nowait(data)
                 elif text := response.text:
                     print(f"\nResponse text: {text}")

                     # Save accumulated audio data after the complete response
                     if audio_data:
                         print(f"\nSaving complete response to {output_filename}")
                         await self.save_audio_to_file(bytes(audio_data), output_filename)
                         # Stream audio to Omniverse after saving
                         print("Streaming audio to Omniverse...")
                         from audio2face_streaming_utils import main  # Import inside the method if necessary
                         main(output_filename, '/World/audio2face/PlayerStreaming')
                     # Clear audio buffer for the next response
                     audio_data.clear()

             # If we have accumulated audio data but no text (end of turn)
             if audio_data:
                 print(f"\nSaving audio-only response to {output_filename}")
                 await self.save_audio_to_file(bytes(audio_data), output_filename)
                 # Stream audio to Omniverse after saving
                 print("Streaming audio to Omniverse...")
                 from audio2face_streaming_utils import main  # Ensure it's imported
                 main(output_filename, '/World/audio2face/PlayerStreaming')

         except Exception as e:
             print(f"Error in receive_audio: {e}")
             traceback.print_exc()

 async def save_audio_to_file(self, data, filename="response.wav"):
     try:
         with wave.open(filename, 'wb') as wav_file:
             wav_file.setnchannels(1)  # Mono
             wav_file.setsampwidth(2)  # 16-bit audio
             wav_file.setframerate(SEND_SAMPLE_RATE)  # Sample rate
             wav_file.writeframes(data)

         print(f"Saved audio to {filename}")
     except Exception as e:
         print(f"Error saving audio to {filename}: {e}")
         traceback.print_exc()

 async def run(self):
     try:
         async with (
             client.aio.live.connect(model=MODEL, config=CONFIG) as session,
             asyncio.TaskGroup() as tg,
         ):
             self.session = session
             self.audio_in_queue = asyncio.Queue()
             self.out_queue = asyncio.Queue(maxsize=5)

             send_text_task = tg.create_task(self.send_text())
             tg.create_task(self.send_realtime())
             tg.create_task(self.listen_audio())
             if self.video_mode == "camera":
                 tg.create_task(self.get_frames())
             tg.create_task(self.receive_audio())

             await send_text_task
             raise asyncio.CancelledError("User requested exit")
     except asyncio.CancelledError:
         pass
     except Exception as e:
         if hasattr(self, 'audio_stream'):
             self.audio_stream.close()
         print(f"Error: {e}")
         traceback.print_exc()

if __name__ == "__main__":
 parser = argparse.ArgumentParser()
 parser.add_argument("--mode", type=str, default=DEFAULT_MODE, choices=["camera", "screen", "none"], help="Pixels to stream from")
 parser.add_argument("--knowledge", type=str, default="D:\\UE_DigitalTwin_BRAIN\\Gemini\\Gemini\\knowledge_base.txt", help="Path to knowledge base file")
 args = parser.parse_args()

 audio_loop = AudioLoop(video_mode=args.mode, knowledge_base_path=args.knowledge)
 asyncio.run(audio_loop.run())