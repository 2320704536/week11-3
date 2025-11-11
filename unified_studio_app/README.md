# Role‑based Creative Chatbot — Auto Fallback (Silent Claude Fail)

**What’s new (per your request):**
- If **Claude key is invalid** → **no warnings, no red error box, no messages**. The app **silently** falls back to **Free Demo** and answers normally.
- If **Claude key is empty** (and provider=Claude) → a **gentle prompt in the sidebar** asks for a key. It still answers using **Free Demo** meanwhile.
- In **Auto** mode, the app tries Claude → OpenAI → Demo **silently**, with zero UI noise on failures.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Providers
- Auto / Anthropic Claude / OpenAI / Free Demo (No API)
- Keys can be pasted in the sidebar. If you also configure `st.secrets`, the app will read them when available but never requires them.
