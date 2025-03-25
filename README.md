**Requirements:**

- Python 3.12.7 or higher (this code is verified with version 3.12.7).
- Dependencies listed in the `requirements.txt` file.
- Google AI studio API key

### **Setup Guide**

#### **Step 1: Install Python (if necessary)**

1. **Download Python:**

   - If you don't already have Python installed, download Python 3.12.7 or higher from the [official Python website](https://www.python.org/downloads/).

2. **Add Python to Environment Variables:**

   - After installing Python, ensure it's available globally by adding Python to your system’s PATH environment variable.

   **For Windows:**

   - Go to **Control Panel > System and Security > System > Advanced system settings > Environment Variables**.
   - In the **System Variables** section, locate the `Path` variable and click **Edit**.
   - Add the following directories to the list:
     - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\`
     - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\Scripts`
   - **Move these entries to the top of the list** for priority.

#### **Step 2: Set Up a Virtual Environment**

1. **Create a Virtual Environment:**

   - Open **Command Prompt** or **PowerShell**, and navigate to your project folder. Then, create a virtual environment by running:

     ```
     virtualenv venv
     ```

   - This will create a `venv` folder in your project directory.

2. **Activate the Virtual Environment:**

   - To activate the virtual environment, use the following command:

     - **Windows (Command Prompt)**:

       ```
       venv\Scripts\activate
       ```

     - 

#### **Step 3: Install Required Dependencies**

1. **Install Dependencies:**

   - With the virtual environment activated, install the required dependencies by running:

     ```
     pip install -r requirements.txt
     ```

   - This will install all the necessary libraries (like `pyaudio`, `opencv-python`, `PIL`, etc.) for the project.

#### **Step 4: Set Up Google Gemini API Key**

1. **Obtain Google Gemini API Key:**

   - You'll need a valid API key from Google Gemini. Get your key from the [Google Cloud Console](https://aistudio.google.com/prompts/new_chat).

2. **Set the GEMINI_API_KEY:**

   - In your command line or terminal, set the API key as an environment variable. Run the following command:

     ```
     set GEMINI_API_KEY=your_api_key_here
     ```

   - Ensure that this key is set in the terminal session where you will be running the code.

#### **Step 5: Update the Knowledge Base File**

1. **Update Knowledge Base Path:**

   - The `knowledge_base.txt` file contains context to provide to the AI model. By default, the path is set to a specific location, but you should update it to your own file path.

   Update the following line in the code:

   ```
   parser.add_argument("--knowledge", type=str, default="D:\\UE_DigitalTwin_BRAIN\\Gemini\\Gemini\\knowledge_base.txt", help="Path to knowledge base file")
   ```

   Replace the default path with the path to your own knowledge base file. For example:

   ```
   parser.add_argument("--knowledge", type=str, default="C:\\path\\to\\your\\knowledge_base.txt", help="Path to knowledge base file")
   ```

2. **Modify the Knowledge Base:**

   - Open the `knowledge_base.txt` file and modify it with your own content. This file contains key information, facts, and context that your AI model will use when interacting with you.

#### **Step 6: Update Speech Configuration (Optional)**

1. **Change the Voice:**

   - If you don’t like the default voice for the audio responses, you can change it to a different voice from Google Gemini’s options. In the `CONFIG` dictionary in your code, update the `speech_config` field to select a different voice:

   ```
   CONFIG = {"generation_config": {"response_modalities": ["AUDIO"], "speech_config": "Aoede"}}
   ```

   The available voices are:

   - Aoede
   - Charon
   - Fenrir
   - Kore
   - Puck

   You can find more details about voice options from the Google Gemini API documentation.

#### **Step 7: Running the Code**

1. **Run the Project:**

   - Once you've completed the setup, you can run the project with the following command:

   ```
   python GoogleGemini.py
   ```

   
