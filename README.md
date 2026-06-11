# 🎬 Video RAG — AI-Powered Video Intelligence Assistant

An end-to-end CLI tool that takes any YouTube URL or local video/audio file and turns it into an interactive AI assistant. It transcribes the audio, generates a summary, extracts structured insights, builds a RAG (Retrieval-Augmented Generation) pipeline over the transcript, and drops you into a chat session where you can ask anything about the content.

---

## ✨ Features

- **YouTube & local file support** — paste a YouTube URL or point to any local audio/video file
- **Automatic transcription** — uses OpenAI Whisper (runs fully locally, no API key needed)
- **AI-generated title & summary** — map-reduce summarisation via Mistral for long transcripts
- **Structured extraction** — action items, key decisions, and open/unresolved questions
- **RAG Q&A chat** — ChromaDB vector store + HuggingFace embeddings + Mistral LLM for grounded answers
- **Beautiful CLI** — rich terminal UI with spinners, panels, and colour-coded output

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Audio download | `yt-dlp` |
| Audio processing | `pydub`, `ffmpeg` |
| Transcription | `openai-whisper` (local, `small` model by default) |
| LLM | Mistral AI (`mistral-small-latest` / `mistral-small-2506`) |
| LLM orchestration | LangChain LCEL |
| Embeddings | `sentence-transformers` — `all-MiniLM-L6-v2` |
| Vector store | ChromaDB (persisted locally at `vector_db/`) |
| CLI UI | `rich` |

---

## 📁 Project Structure

```
rag-video/
├── main.py                  # Entry point — orchestrates the full pipeline + chat loop
├── core/
│   ├── transcription.py     # Whisper transcription (with Sarvam STT-translate stub for Hinglish)
│   ├── summary.py           # Map-reduce summarisation + title generation
│   ├── extractor.py         # Action items, key decisions, open questions extraction
│   ├── rag_engine.py        # RAG chain (retriever → prompt → Mistral → answer)
│   └── vector_store.py      # ChromaDB build/load + HuggingFace embeddings
├── utils/
│   └── audio_processor.py   # YouTube download, WAV conversion, audio chunking
├── requirements.txt
├── pyproject.toml
└── .env                     # API keys (not committed — see setup below)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- [FFmpeg](https://ffmpeg.org/download.html) installed and available on your `PATH`
- A [Mistral AI API key](https://console.mistral.ai/)

### 1. Clone the repository

```bash
git clone https://github.com/ganeshbirajdar286/rag-video.git
cd rag-video
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Or with `uv` (recommended — uses the lockfile):

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here

# Optional — defaults shown
WHISPER_MODEL=small           # tiny | base | small | medium | large
```

### 4. Run

```bash
python main.py
```

You will be prompted to enter a YouTube URL or a local file path, then optionally choose the transcript language (default: `english`).

---

## 🔄 Pipeline Overview

```
Input (YouTube URL / local file)
        ↓
  Audio download + WAV conversion
        ↓
  10-minute audio chunking
        ↓
  Whisper transcription (per chunk)
        ↓
  Full transcript
  ┌─────┴─────────────────────────┐
  │                               │
  ▼                               ▼
Title & Summary            Vector store build
(Mistral map-reduce)       (ChromaDB + MiniLM)
  │                               │
  ▼                               │
Action items / Decisions /        │
Open questions (Mistral)          │
  │                               │
  └─────────┬─────────────────────┘
            ▼
     Results printed to terminal
            ↓
       Interactive chat loop
       (RAG: retriever → Mistral)
```

---

## 💬 Chat Mode

After analysis, the tool enters an interactive Q&A session. Ask anything about the video:

```
You: What decisions were made about the project timeline?
🤖 Assistant: Based on the transcript, the team agreed to push the release date to Q3 ...

You: Who is responsible for the design review?
🤖 Assistant: Sarah was assigned the design review with a deadline of next Friday ...

You: exit
👋 Goodbye!
```

Type `exit`, `quit`, or `q` to end the session.

---

## ⚙️ Configuration

| Variable | Default | Description |
|---|---|---|
| `MISTRAL_API_KEY` | — | **Required.** Your Mistral AI API key |
| `WHISPER_MODEL` | `small` | Whisper model size (`tiny` → `large`). Larger = more accurate, slower |
| `SARVAM_API_KEY` | — | Optional. For Hinglish transcription via Sarvam STT (stub included) |
| `SARVAM_STT_MODEL` | `saaras:v3` | Sarvam model to use when Hinglish is selected |

---

## 📦 Key Dependencies

```
openai-whisper       # Local speech-to-text
yt-dlp               # YouTube audio download
pydub                # Audio manipulation
langchain            # LLM orchestration (LCEL)
langchain-mistralai  # Mistral LLM integration
langchain-chroma     # ChromaDB vector store
langchain-huggingface # HuggingFace embeddings
sentence-transformers # all-MiniLM-L6-v2 embedding model
rich                 # Terminal UI
python-dotenv        # .env loading
```


---

## 📄 License

This project is open source. Feel free to use, modify, and build on it.

---

> Built by [Ganesh Birajdar](https://github.com/ganeshbirajdar286)
