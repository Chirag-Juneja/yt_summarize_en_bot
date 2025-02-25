# 🎥 YouTube Summarization Telegram Bot  

This repository contains a **YouTube Summarization Telegram Bot** that extracts transcripts from YouTube videos and generates concise summaries using **Large Language Models (LLMs)**. This tool is useful for quickly understanding long-form video content without watching the entire video.  

## 🚀 Features  

- **Extracts YouTube Video Transcripts** – Uses YouTube API to fetch transcripts.  
- **Summarizes Content** – Applies LLM-based models to generate a concise summary.  
- **Supports English Transcripts** – Works specifically with English-language videos.  
- **Easy to Use** – Automates the entire process from transcript retrieval to summarization.  

## 🔧 How It Works  

1. **Fetch Transcript** – The bot extracts the video’s transcript using the YouTube API.  
2. **Preprocess Text** – Cleans and structures the transcript for better summarization.  
3. **Generate Summary** – Uses an LLM (such as DeepSeekR1) to summarize the transcript.  
4. **Output the Summary** – Presents the key points of the video in a readable format.  

## 🛠️ Installation  

**Clone the Repository**  
   ```bash
   git clone https://github.com/Chirag-Juneja/yt_summarize_en_bot.git
   cd yt_summarize_en_bot
   ```

**Run the summarizer from terminal**

   ```bash
   python agent.py --url="https://www.youtube.com/watch?v=7GmD_cCHfiE"
   ```

**Run the bot**
   ```bash
   python bot.py
   ```
