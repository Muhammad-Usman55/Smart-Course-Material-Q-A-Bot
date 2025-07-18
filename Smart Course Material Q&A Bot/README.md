# Smart Course Material Q&A Bot with Personality Adaptation

This project is a minimal, easy-to-explain Streamlit application that allows you to upload course materials (PDF, DOCX, TXT), select a bot personality, and ask questions about the content. It uses Retrieval-Augmented Generation (RAG) with Google Gemini (Generative AI) via LangChain, and can be easily adapted for paper writing or research assistance by connecting to an LLM.

## Features
- **Document Upload:** Supports PDF, DOCX, and TXT files.
- **Retrieval-Augmented Generation (RAG):** Finds relevant content from your uploaded documents and uses an LLM to answer questions.
- **Personality Adaptation:** Choose from different bot personalities (system messages) for tailored responses.
- **Streamlit UI:** Simple, interactive web interface.
- **Google Gemini Integration:** Uses Gemini models for high-quality answers.

## How to Use for Paper Writing
1. **Upload your research papers, notes, or any reference material** (PDF, DOCX, TXT).
2. **Select a personality** (e.g., formal academic, friendly tutor, etc.).
3. **Ask questions** about your material (e.g., "Summarize the main findings", "Write a related work section", "Suggest a research gap").
4. **Copy the generated answers** to use in your paper writing process.

## How It Works
- Documents are split into chunks and embedded into a vector database (FAISS).
- When you ask a question, the app retrieves the most relevant chunks.
- The context and your question are sent to a Gemini LLM, which generates a detailed answer in your chosen style.

## Example Prompts for Paper Writing
- "Summarize the methodology section."
- "Write an abstract for this paper."
- "List the key contributions."
- "Suggest future work based on the findings."
- "Generate a related work paragraph using the uploaded sources."

## Quick Start
1. Clone this repo and install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Add your Google Gemini API key to a `.env` file:
   ```env
   GOOGLE_API_KEY=your-key-here
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## File Structure
- `app.py` — Streamlit UI
- `bot_core.py` — Core logic (document loading, RAG, answer generation)
- `personalities.py` — Bot personalities (system messages)
- `.env` — API key
- `requirements.txt` — Dependencies

## Adapting for LLM Paper Writing
- You can use the same RAG pipeline to feed your own research corpus and prompt the LLM for academic writing tasks.
- Modify the system message in `personalities.py` for more academic or creative writing styles.
- Use the Q&A interface to iteratively build sections of your paper.

## Credits
- Built with [LangChain](https://python.langchain.com/), [Streamlit](https://streamlit.io/), and [Google Gemini](https://ai.google.dev/).

---

**Tip:** This README can be given to an LLM to generate a research paper, related work, or any academic writing based on your uploaded materials!
