📺 TubeTalk: Multimodal Video Analysis AI

TubeTalk is an AI-powered application that allows users to chat with YouTube videos. It leverages Google Gemini 1.5 Flash to analyze video content through two intelligent pipelines:

Transcript Analysis (RAG): Extracts and indexes subtitles for high-speed text querying.

Audio Analysis (Multimodal): Downloads and listens to video audio directly when subtitles are missing.

🚀 Features

Dual-Mode Analysis: Automatically switches between Text RAG and Audio processing based on data availability.

Vector Search Memory: Uses FAISS to store and retrieve relevant video segments instantly.

Smart Fallback: Robust error handling that includes a "Manual Paste" mode for IP-restricted scenarios.

Local Embeddings: Utilizes HuggingFace embeddings locally to avoid API rate limits.

🛠️ Tech Stack

AI Model: Google Gemini 1.5 Flash (via Google GenAI SDK)

Framework: Streamlit (Python)

Vector Database: FAISS

Embeddings: HuggingFace (all-MiniLM-L6-v2)

Video Tools: yt-dlp (Audio Extraction), youtube-transcript-api

📦 Installation

Clone the repository

git clone [https://github.com/prajaktaa93/TubeTalk.git](https://github.com/YOUR_USERNAME/TubeTalk.git)
cd TubeTalk


Install Dependencies

pip install -r requirements.txt


Install System Tools (For Audio Mode)

Mac: brew install ffmpeg

Windows: Download FFmpeg from the official site.

Set up API Keys

Create a .env file in the root folder.

Add your Google API Key: AIzaSyBpJNB1EHwFe92n9kjC6vOL8-qt8pUYocE

Run the App

streamlit run app.py


📸 Screenshots

(Add a screenshot of your running app here later!)

Built with ❤️ using Python.