# Real-Time Audio & Video Interaction with Google Gemini

## Requirements

- Python 3.12.7 or higher (this code is verified with version 3.12.7).
- Dependencies listed in the `requirements.txt` file.
- API key from Google AI studio

## Setup Instructions

### Step 1: Install Python (if necessary)

1. **Download Python**:
   If you don't already have Python installed, download Python 3.12.7 or higher from the [official Python website](https://www.python.org/downloads/).

2. **Add Python to Environment Variables**:
   After installing Python, ensure it's available globally by adding Python to your system’s PATH environment variable.

   **For Windows**:
   - Go to **Control Panel > System and Security > System > Advanced system settings > Environment Variables**.
   - In the **System Variables** section, locate the `Path` variable and click **Edit**.
   - Add the following directories to the list:
     - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\`
     - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\Scripts`
   - **Move these entries to the top of the list** for priority.

### Step 2: Set Up a Virtual Environment

1. **Create a Virtual Environment**:
   Open **Command Prompt** or **PowerShell**, and navigate to your project folder. Then, create a virtual environment by running:
   ```bash
   python -m venv your_virtual_env
