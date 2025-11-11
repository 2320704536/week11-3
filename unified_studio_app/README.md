# Unified Studio (Free Demo + Claude + OpenAI)

A Streamlit app that **works with no API keys** (Free Demo mode) and can optionally switch to **Anthropic Claude** or **OpenAI** when you have API credits.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Modes
- **Free Demo (No API)**: local text suggestions + local placeholder images. No keys, no billing.
- **Anthropic Claude**: set key in sidebar, uses `claude-3-haiku-20240307`.
- **OpenAI**: set key in sidebar, uses Chat Completions (`gpt-4o-mini`). Optional Images (`gpt-image-1`).

> Imports of provider SDKs are inside branches to avoid crashes if packages are missing. Requirements include both for convenience.
