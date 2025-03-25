
    <h1>Setup Instructions</h1>

    <h2>Requirements</h2>
    <ul>
        <li>Python 3.12.7 or higher (this code is verified with version 3.12.7).</li>
        <li>Dependencies listed in the <code>requirements.txt</code> file.</li>
    </ul>

    <h2>Setup Guide</h2>

    <h3>Step 1: Install Python (if necessary)</h3>
    <ol>
        <li>
            <strong>Download Python:</strong>
            <p>If you don't already have Python installed, download Python 3.12.7 or higher from the <a href="https://www.python.org/downloads/">official Python website</a>.</p>
        </li>
        <li>
            <strong>Add Python to Environment Variables:</strong>
            <p>After installing Python, ensure it's available globally by adding Python to your system’s PATH environment variable.</p>
            <p><strong>For Windows:</strong></p>
            <ul>
                <li>Go to <strong>Control Panel > System and Security > System > Advanced system settings > Environment Variables</strong>.</li>
                <li>In the <strong>System Variables</strong> section, locate the <code>Path</code> variable and click <strong>Edit</strong>.</li>
                <li>Add the following directories to the list:</li>
                <ul>
                    <li><code>C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\</code></li>
                    <li><code>C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\Scripts</code></li>
                </ul>
                <li><strong>Move these entries to the top of the list</strong> for priority.</li>
            </ul>
        </li>
    </ol>

    <h3>Step 2: Set Up a Virtual Environment</h3>
    <ol>
        <li>
            <strong>Create a Virtual Environment:</strong>
            <p>Open <strong>Command Prompt</strong> or <strong>PowerShell</strong>, and navigate to your project folder. Then, create a virtual environment by running:</p>
            <pre><code>virtualenv venv</code></pre>
            <p>This will create a <code>venv</code> folder in your project directory.</p>
        </li>
        <li>
            <strong>Activate the Virtual Environment:</strong>
            <p>To activate the virtual environment, use the following command:</p>
            <ul>
                <li><strong>Windows (Command Prompt):</strong>
                    <pre><code>venv\Scripts\activate</code></pre>
                </li>
                <li><strong>Windows (PowerShell):</strong>
                    <pre><code>.\venv\Scripts\Activate.ps1</code></pre>
                </li>
            </ul>
        </li>
    </ol>

    <h3>Step 3: Install Required Dependencies</h3>
    <ol>
        <li>
            <strong>Install Dependencies:</strong>
            <p>With the virtual environment activated, install the required dependencies by running:</p>
            <pre><code>pip install -r requirements.txt</code></pre>
            <p>This will install all the necessary libraries (like <code>pyaudio</code>, <code>opencv-python</code>, <code>PIL</code>, etc.) for the project.</p>
        </li>
    </ol>

    <h3>Step 4: Set Up Google Gemini API Key</h3>
    <ol>
        <li>
            <strong>Obtain Google Gemini API Key:</strong>
            <p>You’ll need a valid API key from Google Gemini. Get your key from the <a href="https://aistudio.google.com/prompts/new_chat">Google Cloud Console</a>.</p>
        </li>
        <li>
            <strong>Set the GEMINI_API_KEY:</strong>
            <p>In your command line or terminal, set the API key as an environment variable. Run the following command:</p>
            <pre><code>set GEMINI_API_KEY=your_api_key_here</code></pre>
            <p>Ensure that this key is set in the terminal session where you will be running the code.</p>
        </li>
    </ol>

    <h3>Step 5: Update the Knowledge Base File</h3>
    <ol>
        <li>
            <strong>Update Knowledge Base Path:</strong>
            <p>The <code>knowledge_base.txt</code> file contains context to provide to the AI model. By default, the path is set to a specific location, but you should update it to your own file path.</p>
            <p>Update the following line in the code:</p>
            <pre><code>parser.add_argument("--knowledge", type=str, default="D:\\UE_DigitalTwin_BRAIN\\Gemini\\Gemini\\knowledge_base.txt", help="Path to knowledge base file")</code></pre>
            <p>Replace the default path with the path to your own knowledge base file. For example:</p>
            <pre><code>parser.add_argument("--knowledge", type=str, default="C:\\path\\to\\your\\knowledge_base.txt", help="Path to knowledge base file")</code></pre>
        </li>
        <li>
            <strong>Modify the Knowledge Base:</strong>
            <p>Open the <code>knowledge_base.txt</code> file and modify it with your own content. This file contains key information, facts, and context that your AI model will use when interacting with you.</p>
        </li>
    </ol>

    <h3>Step 6: Update Speech Configuration (Optional)</h3>
    <ol>
        <li>
            <strong>Change the Voice:</strong>
            <p>If you don’t like the default voice for the audio responses, you can change it to a different voice from Google Gemini’s options. In the <code>CONFIG</code> dictionary in your code, update the <code>speech_config</code> field to select a different voice:</p>
            <pre><code>CONFIG = {"generation_config": {"response_modalities": ["AUDIO"], "speech_config": "Aoede"}}</code></pre>
            <p>The available voices are:</p>
            <ul>
                <li>Aoede</li>
                <li>Charon</li>
                <li>Fenrir</li>
                <li>Kore</li>
                <li>Puc</li>
            </ul>
            <p>You can find more details about voice options from the <a href="https://cloud.google.com/dialogflow/docs/voice-options">Google Gemini API documentation</a>.</p>
        </li>
    </ol>

    <h3>Step 7: Running the Code</h3>
    <ol>
        <li>
            <strong>Run the Project:</strong>
            <p>Once you've completed the setup, you can run the project with the following command:</p>
            <pre><code>python GoogleGemini.py</code></pre>
        </li>
    </ol>

</body>
</html>
