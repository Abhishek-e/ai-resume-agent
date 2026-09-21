"""
Resume <-> Job Description Fit Agent
-------------------------------------
A small LLM-powered app: paste a resume and a job description, get back
a fit score, matched/missing skills, and rewrite suggestions for the resume.

Run:
    streamlit run app.py
"""
import os
import json

import streamlit as st

from llm import score_fit, LLMNotConfigured

st.set_page_config(page_title="Resume Fit Agent", page_icon="🎯", layout="wide")

st.title("🎯 Resume ↔ Job Description Fit Agent")
st.caption(
    "Paste a resume and a job description. An LLM scores the fit, lists matched "
    "and missing skills, and suggests concrete resume edits."
)

with st.sidebar:
    st.header("Setup")
    st.markdown(
        "This app calls an LLM API to do the scoring. Set your key as an "
        "environment variable before running:\n\n"
        "```bash\nexport LLM_API_KEY=sk-...\n```\n"
        "Works with OpenRouter, OpenAI, or Anthropic — see `llm.py`."
    )
    provider = st.selectbox("Provider", ["openrouter", "openai", "anthropic"], index=0)
    default_models = {
        "openrouter": "openai/gpt-4o-mini",
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-haiku-latest",
    }
    model = st.text_input("Model", value=default_models[provider])

col1, col2 = st.columns(2)
with col1:
    resume_text = st.text_area("Resume", height=350, placeholder="Paste resume text here...")
with col2:
    jd_text = st.text_area("Job description", height=350, placeholder="Paste job description here...")

if st.button("Score fit", type="primary", use_container_width=True):
    if not resume_text.strip() or not jd_text.strip():
        st.warning("Paste both a resume and a job description first.")
    else:
        with st.spinner("Scoring with the LLM..."):
            try:
                result = score_fit(resume_text, jd_text, provider=provider, model=model)
            except LLMNotConfigured as e:
                st.error(str(e))
                result = None

        if result:
            st.subheader(f"Fit score: {result['score']}/100")
            st.progress(result["score"] / 100)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**✅ Matched skills**")
                for s in result["matched_skills"]:
                    st.markdown(f"- {s}")
            with c2:
                st.markdown("**❌ Missing / weak skills**")
                for s in result["missing_skills"]:
                    st.markdown(f"- {s}")

            st.markdown("**✍️ Suggested resume edits**")
            for tip in result["suggestions"]:
                st.markdown(f"- {tip}")

            with st.expander("Raw LLM response"):
                st.json(result)

