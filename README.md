# 🎬 AI Video Assistant

**An AI-powered application that transforms videos into searchable knowledge using speech recognition, LLM-based summarization, and Retrieval-Augmented Generation (RAG).**

The AI Video Assistant processes video and audio content, generates transcripts, and allows users to ask questions about the content using a locally running Large Language Model.

## ✨ Features

- 🎥 **Video Processing:** Process video and audio content.
- 🎧 **Audio Processing:** Extract and prepare audio for transcription using FFmpeg.
- 📝 **Automatic Transcription:** Convert speech into text using OpenAI Whisper.
- 📚 **Text Chunking:** Split transcripts into smaller chunks for efficient retrieval.
- 🔎 **Semantic Search:** Retrieve relevant transcript sections using vector embeddings.
- 🧠 **RAG-based Question Answering:** Ask questions and receive context-aware answers.
- 🤖 **Local LLM Integration:** Generate responses using Ollama and Gemma 3.
- 💾 **Persistent Vector Storage:** Store transcript embeddings using ChromaDB.

## 🏗️ Architecture

```text
       Video / Audio Input
                |
                v
        Audio Processing
          FFmpeg / yt-dlp
                |
                v
         Audio Transcription
            OpenAI Whisper
                |
                v
             Transcript
                |
                v
          Text Chunking
                |
                v
          Text Embeddings
          nomic-embed-text
                |
                v
             ChromaDB
                |
                v
          Similarity Search
                |
                v
           RAG Pipeline
             LangChain
                |
                v
           Ollama / Gemma 3
                |
                v
        Contextual Answers
```

## 🛠️ Tech Stack

| Technology       | Purpose                               |
| ---------------- | ------------------------------------- |
| Python           | Core development                      |
| uv               | Dependency and environment management |
| OpenAI Whisper   | Speech-to-text transcription          |
| FFmpeg           | Audio and video processing            |
| yt-dlp           | Video downloading                     |
| LangChain        | LLM orchestration and RAG             |
| Ollama           | Local LLM execution                   |
| Gemma 3          | Language model                        |
| nomic-embed-text | Text embeddings                       |
| ChromaDB         | Vector database                       |

## 📂 Project Structure

```text
AI_Video_assistant/
│
├── core/
│   ├── transcriber.py       # Whisper transcription
│   ├── vector_store.py      # Embeddings and ChromaDB
│   └── Rag_engine.py        # RAG pipeline and Q&A
│
├── utils/
│   └── audio_processor.py   # Audio extraction and processing
│
├── downloads/               # Downloaded media files
│
├── main.py                  # Application entry point
├── test.py                  # Testing scripts
├── pyproject.toml           # Project dependencies
├── uv.lock                  # Dependency lock file
└── README.md
```

## ⚙️ Installation

### Prerequisites

- Python
- uv package manager
- Ollama
- FFmpeg

### 1. Clone the repository

```bash
git clone https://github.com/tushar7783/AI_Video_assistant_.git

cd AI_Video_assistant_
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Download Ollama models

```bash
ollama pull gemma3:1b
ollama pull nomic-embed-text
```

### 4. Start Ollama

```bash
ollama serve
```

If Ollama is already running, skip this step.

### 5. Run the application

```bash
uv run python main.py
```

## 🔍 How RAG Works

The application follows a Retrieval-Augmented Generation workflow:

1. **Transcription:** Whisper converts audio into text.
2. **Chunking:** The transcript is divided into smaller text segments.
3. **Embedding:** Each segment is converted into a vector using `nomic-embed-text`.
4. **Storage:** Chunks and their embeddings are stored in ChromaDB.
5. **Retrieval:** The retriever finds the most relevant chunks for a user's question.
6. **Generation:** LangChain passes the retrieved context to Gemma 3 through Ollama.
7. **Answer:** The model generates an answer grounded in the transcript.

## 💬 Example Questions

- What is this video about?
- Summarize the main topics discussed.
- Explain the concept discussed in the video.
- What are the key takeaways?
- What did the speaker say about a particular topic?

## 🚀 Roadmap

The following features are planned for future development.

- [ ] **Streamlit Web Interface:** Build an interactive web application.
- [ ] **Video Upload:** Upload local video and audio files through the UI.
- [ ] **AI Summarization:** Generate concise video summaries.
- [ ] **Interactive AI Chat:** Ask questions through a chat interface.
- [ ] **Chat History:** Maintain conversation history.
- [ ] **Improved UI:** Add processing status, progress indicators, and a clean dashboard.

## 👨‍💻 Author

**Tushar Kumar**

GitHub: [@tushar7783](https://github.com/tushar7783)

Repository: [AI Video Assistant](https://github.com/tushar7783/AI_Video_assistant_)

---

⭐ If you find this project useful, consider giving it a star!
