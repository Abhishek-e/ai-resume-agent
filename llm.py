"""
Thin LLM wrapper so app.py doesn't care which provider is behind it.
Supports OpenAI and Anthropic; add another provider by adding a branch here.
"""
import json
import os

PROMPT = """You are a technical recruiter. Compare the RESUME against the JOB DESCRIPTION.

Return ONLY valid JSON with this exact shape, no other text:
{{
  "score": <integer 0-100, overall fit>,
  "matched_skills": [<skills/requirements the resume clearly covers>],
  "missing_skills": [<skills/requirements in the JD the resume doesn't show>],
  "suggestions": [<3-5 concrete, specific edits to the resume to close the gap>]
}}

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""


class LLMNotConfigured(Exception):
    pass


def _extract_json(text: str) -> dict:
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found in model response: {text[:200]}")
    return json.loads(text[start : end + 1])


def score_fit(resume: str, jd: str, provider: str = "openai", model: str = "gpt-4o-mini") -> dict:
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise LLMNotConfigured(
            "Set the LLM_API_KEY environment variable before running "
            "(export LLM_API_KEY=sk-...)."
        )

    prompt = PROMPT.format(resume=resume[:6000], jd=jd[:6000])

    if provider == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw = resp.choices[0].message.content

    elif provider == "anthropic":
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text

    else:
        raise ValueError(f"Unknown provider: {provider}")

    return _extract_json(raw)
