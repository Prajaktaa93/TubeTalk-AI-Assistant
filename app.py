import streamlit as st
import os
from dotenv import load_dotenv
import yt_dlp
import time

# --- IMPORTS ---
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

# DIRECT IMPORTS
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

load_dotenv()

st.set_page_config(page_title="TubeTalk 🎥", page_icon="🤖", layout="wide")

# --- HELPER: GET WORKING MODEL ---
def get_working_model_name(api_key):
    try:
        genai.configure(api_key=api_key)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if 'models/gemini-1.5-flash' in models: return 'models/gemini-1.5-flash'
        for m in models:
            if 'flash' in m: return m
        return 'models/gemini-pro'
    except:
        return 'gemini-1.5-flash'

# --- HELPER: DOWNLOAD AUDIO (The "No Transcript" Fix) ---
def download_audio(video_url):
    """Downloads audio from YouTube when transcript fails."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
        'outtmpl': 'temp_audio.%(ext)s',
        'quiet': True
    }
    try:
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return "temp_audio.mp3", None
    except Exception as e:
        return None, str(e)

# --- HELPER: GET CONTENT (Transcript OR Audio) ---
def get_video_content(video_url, api_key):
    # 1. Try Transcript First (Fast & Free)
    try:
        video_id = video_url.split("v=")[1].split("&")[0] if "v=" in video_url else video_url.split("/")[-1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript_list])
        return text, "text", None
    except:
        # 2. Fallback to Audio Download (Slower but Powerful)
        st.info("⚠️ No transcript found. Switching to Audio Mode (listening to video)...")
        audio_path, error = download_audio(video_url)
        
        if error:
            return None, None, f"Failed to download audio: {error}"
        
        # Upload Audio to Gemini
        genai.configure(api_key=api_key)
        myfile = genai.upload_file(audio_path)
        
        # Wait for processing
        while myfile.state.name == "PROCESSING":
            time.sleep(2)
            myfile = genai.get_file(myfile.name)
            
        return myfile, "audio", None

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.divider()
    st.info("ℹ️ App auto-switches to 'Audio Mode' if no transcript exists.")

# --- MAIN PAGE ---
st.title("🤖 TubeTalk: Chat with Videos")

# --- INPUT ---
video_url = st.text_input("Paste YouTube Video URL here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Analyze Video"):
    if api_key and video_url:
        with st.spinner("🧠 Analyzing content..."):
            content, content_type, error = get_video_content(video_url, api_key)
            
            if error:
                st.error(error)
            else:
                st.session_state.content = content
                st.session_state.content_type = content_type
                st.success("✅ Video Processed!")
    else:
        st.warning("Please enter API Key and URL.")

# --- CHAT SECTION ---
if "content" in st.session_state and api_key:
    st.divider()
    query = st.text_input("Ask a question about the video:")
    
    if query:
        with st.spinner("Thinking..."):
            try:
                model_name = get_working_model_name(api_key)
                model = genai.GenerativeModel(model_name)
                
                if st.session_state.content_type == "text":
                    # TEXT MODE (RAG)
                    # Simple prompt for text
                    prompt = f"Context: {st.session_state.content[:30000]}... \n\nQuestion: {query}"
                    response = model.generate_content(prompt)
                
                else:
                    # AUDIO MODE (Native Multimodal)
                    # We pass the audio file directly to Gemini!
                    response = model.generate_content([st.session_state.content, query])
                
                st.markdown(f"**Answer:** {response.text}")
                
            except Exception as e:
                st.error(f"Error: {e}")