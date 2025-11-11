# Role‑based Creative Chatbot — Auto Fallback

A Streamlit app matching the course screenshots:
- Sidebar: API key field(s), role picker with description
- Main: single question box + "Generate Response"
- Providers: **Auto / Claude / OpenAI / Free Demo (No API)**
- **Auto Fallback**: if secrets/keys missing or API errors (billing/quota), it gracefully falls back to a local templated answer.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- It *tries* to read `st.secrets["OPENAI_API_KEY"]` and `st.secrets["ANTHROPIC_API_KEY"]` if present, but never crashes without them. You can also paste keys in the sidebar.
- In **Auto** mode it prefers Claude (if key present), then OpenAI, otherwise Free Demo.
- No image generation here — this matches the role‑based chatbot spec from your slides.
