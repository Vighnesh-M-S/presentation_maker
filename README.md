# 🧠 Presentation Generator from URL using Firecrawl + Alai

This project lets you generate AI-powered slide presentations from any URL. It uses Firecrawl to extract content and OpenAI to summarize and identify key points. Then, it automates slide creation using Alai through a headless Selenium browser.

## 🚀 Features

- Extracts content summary + key points from any webpage.
- Auto-login to [app.getalai.com](https://app.getalai.com) using Selenium.
- Creates a new slide deck using AI.
- Selects 2–5 slides preset and auto-pastes extracted summary.
- Calibrates tone, generates slides, and returns a **shareable link**.
- Clean frontend with one-click input + result.

## 🛠 Tech Stack

- **FastAPI** - Backend API
- **Firecrawl** - Content scraping and intelligent extraction
- **Selenium** - Automated browser interaction with Alai
- **Frontend** - HTML + JS
- **uvicorn** - ASGI server

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/presentation-generator.git
cd presentation-generator
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Make sure `chromedriver` is installed and matches your Chrome version.

### 3. Environment Variables

Create a `.env` file in the root directory with the following:

```
FIRECRAWL_API=your_firecrawl_api_key
EMAIL=your_alai_login_email
PASSWORD=your_alai_login_password
```

### 4. Run the Server

```bash
uvicorn main:app --reload --port 9090
```

### 5. Visit the Frontend

Open [http://127.0.0.1:9090](http://127.0.0.1:9090) in your browser.

## 📂 Project Structure

```
.
├── Backend
│   ├── main.py
│   ├── requirements.txt          # FastAPI backend + Firecrawl + Selenium
├── .env                # Your API keys and credentials
├── Frontend/
│   ├── index.html
└── README.md
```

## 📸 Sample Output

The final result will be a shareable slide deck hosted on Alai:
```
https://app.getalai.com/view/your-deck-id
```

---

## 🧠 Note
This project is for educational purposes. Use responsibly and do not abuse automation on third-party platforms.

