# Resume ↔ Job Description Fit Agent

An LLM-powered app that scores how well a resume fits a job description, lists
matched and missing skills, and suggests concrete resume edits — built to
close a specific skill gap: a working, deployable **LLM application**, not a
notebook.

**Live demo:** add your deployed Streamlit Cloud / Hugging Face Spaces link here once deployed.

## What it does

Paste a resume and a job description. The app sends both to an LLM (OpenAI or
Anthropic, your choice) with a structured prompt and gets back:

- an overall fit score (0-100)
- skills the resume already demonstrates
- skills the JD wants that the resume is missing
- 3-5 specific rewrite suggestions

## Tech stack

Python · Streamlit (UI) · OpenAI / Anthropic API (LLM call) · JSON-structured
prompting for reliable parsing.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env      # then edit .env with your key
export LLM_API_KEY=sk-...  # or: source .env

streamlit run app.py
```

Try it immediately with the included sample data in `sample_data/` —
`sample_resume.txt` and `sample_jd.txt` — just paste their contents into the
two text boxes.

## Deploy a live demo

**Streamlit Community Cloud** (free, easiest):
1. Go to share.streamlit.io, connect this repo, point it at `app.py`.
2. Add `LLM_API_KEY` under the app's Secrets settings.
3. Copy the resulting URL into the "Live demo" line at the top of this README.

## Notes

- No API key is ever committed — it's read from an environment variable only.
- The LLM is asked to return strict JSON so the app can parse it reliably;
  see `llm.py` for the prompt and parsing.
- Swap providers/models from the sidebar without touching code.

