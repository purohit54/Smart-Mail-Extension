# Smart Mail Assistant

Smart Mail Assistant is an AI-powered email assistant that connects to a Gmail inbox, extracts email information, generates concise summaries and priority information using an LLM, and stores the processed email data in a MySQL database.

## Features
* Data stays in the your machine.
* Connects to Gmail using IMAP.
* Fetches emails from the inbox.
* Extracts important email information such as:

  * Sender
  * Subject
  * Date
  * Email body
* Generates concise email summaries using an LLM.
* Assigns a priority to emails.
* Stores email metadata and generated summaries in MySQL.
* Uses a Chrome extension content script to interact with the Gmail webpage.

## Tech Stack

### Backend

* Python
* IMAP
* MySQL
* SQL
* FastAPI
* Qwen LLM
* Ollama

### Frontend

* JavaScript
* Chrome Extension APIs

### Development Tools

* Git
* GitHub
* VS Code

## System Architecture

```text
                    Gmail
                      |
                      | IMAP
                      v
              +---------------------+
              |   Chrome Extension  |
              |     content.js      |
              +---------------------+
                      |
                      | Extract mail data
                      v
              +---------------------+
              |     Background.js   |
              +---------------------+
                      |
                      | API Request
                      v
              +---------------------+
              |    Backend API      |
              +---------------------+
                       |
                       v
              +----------------------+
              |    Email Fetcher     |
              |   / Email Parser     |
              +----------------------+
                   |       |
                   |       |
              +----------------------+
              |    Qwen LLM          |
              |       Ollama         |
              +----------------------+
                        |
                        v
              +----------------------+
              |       Summary        |
              +----------------------+
                       |
                       v
                +-------------+
                |    MySQL    |
                |   Database  |
                +-------------+

```

## Project Workflow

The application follows these general steps:

1. Chrome extension provide which mail is open
2. Find the relevant mail using IMAP
3. Parse the email content and metadata.
4. Check that it mail processed before 
5. Send relevant email content to the Qwen model.
6. Generate a concise summary and priority information.
7. Store the processed information in the MySQL database.
8. The Chrome extension communicates with the backend/background process.


## Project Structure

```text
Smart_Mail/
│
├── js/
│   ├── content.js
│   ├── background.js
│
├── py/
│   └── email_fetcher.py
│   ├── summarizer.py
│   ├── db.py
│   └── main.py
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
└── requirements.txt
```

> Update the project structure above according to the actual files in the repository.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Smart_Mail
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root.

Example:

```env
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password

DB_HOST=localhost
DB_PORT=3306
DB_NAME=smart_mail
DB_USER=your_database_user
DB_PASSWORD=your_database_password

OLLAMA_MODEL=qwen2.5:7b
```

## Ollama Setup

Install Ollama and download the required model.

Example:

```bash
ollama pull qwen2.5:7b
```

Verify that the model is available:

```bash
ollama list
```

## Database

The application uses MySQL to store processed email information.

Example database structure:

```text
Summary
│
├── messageid
├── Summary
├── Purpose
└── Reply

email
│
├── messageid
├── From
├── subject
└── date
```

## Chrome Extension

The Chrome extension contains the frontend components responsible for interacting with the Gmail webpage.

Important files include:

```text
content.js
background.js
```

### Loading the extension

1. Open Chrome.
2. Navigate to:

```text
chrome://extensions/
```

3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the extension directory.
6. Open Gmail and test the extension.

Make sure the FastAPi is running before using the extension.

## Future Improvements

Possible future improvements include:

* Automatic email categorization.
* Better email priority classification.
* Attachment processing.
* Support for multiple email providers.
* Improved response generation.
* Email action recommendations.
* Improved Chrome extension UI.
* Integration with a vector database for semantic email search.

## License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

## Author

**Rajendra Purohit**

