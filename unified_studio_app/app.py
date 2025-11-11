
import streamlit as st
import numpy as np
from typing import Dict
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Unified Studio", page_icon="🎛️", layout="wide")

# ---------- Sidebar: Provider, Keys, Role ----------
st.sidebar.header("⚙️ Settings")

PROVIDERS = ["Free Demo (No API)", "Anthropic Claude", "OpenAI"]
provider = st.sidebar.selectbox("Provider", PROVIDERS, index=0)

if "CLAUDE_API_KEY" not in st.session_state:
    st.session_state["CLAUDE_API_KEY"] = ""
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""

if provider == "Anthropic Claude":
    ck = st.sidebar.text_input("Claude API Key", type="password", value=st.session_state["CLAUDE_API_KEY"])
    if ck: st.session_state["CLAUDE_API_KEY"] = ck
elif provider == "OpenAI":
    ok = st.sidebar.text_input("OpenAI API Key", type="password", value=st.session_state["OPENAI_API_KEY"])
    if ok: st.session_state["OPENAI_API_KEY"] = ok

ROLES: Dict[str, str] = {
    "Video Director": "You visualize stories and direct how they are brought to life on screen.",
    "Game Designer": "You craft interactive systems, level flow, and player motivation.",
    "Photographer": "You think in light, lens, and composition to capture mood and story.",
    "Graphic Designer": "You shape brand, layout, and hierarchy for clear visual communication.",
    "Illustrator": "You convey ideas through stylized drawing, color, and texture.",
}
role = st.sidebar.selectbox("Role", list(ROLES.keys()))
st.sidebar.write(ROLES[role])

st.title("🎛️ Unified Studio")
st.caption("Works offline in Free Demo mode. Switch provider to use Claude/OpenAI when you have credits.")

tab_chat, tab_image = st.tabs(["💬 Chat Assistant", "🖼️ Image Studio"])

# ---------- Local role templates (no-API) ----------
ROLE_TEMPLATES = {
    "Video Director": lambda q: f"""**Cinematic Plan**
- Logline: {q[:120]}...
- Visual Language: handheld + 35mm look; teal/orange contrast; shallow DoF.
- Coverage: WS for geography, MS for performance, CU for beats.
- Lenses: 24/35/85mm; T2.8 indoors; ND outside.
- Lighting: key (soft), edge (tube), practicals for depth.
- Blocking: cross, over-shoulder reverses; inserts for props.
- Transitions: motivated whip + L-cuts.
- Color: muted base with saturated accents.
- Next: shoot board (8–12 shots), 3h tech scout.
""",
    "Game Designer": lambda q: f"""**Design Slice**
- Fantasy: {q[:120]}...
- Core Loop: Explore → Collect → Upgrade → Challenge → Reward.
- Mechanics: stamina risk, parry window, combo meter.
- Progression: acts 1–3; unlock skill grid every 2 levels.
- Systems: economy (sink/source), crafting tiers, rarity.
- Level: 10-min lane → hub → boss arena.
- Telemetry: failpoints, heatmaps, churn cohort D1/D7.
- Scope: 2-week vertical slice.
""",
    "Photographer": lambda q: f"""**Shoot Plan**
- Concept: {q[:120]}...
- Lens/Camera: 35/85mm; f/1.8–2.8; base ISO 100.
- Light: north window + bounce; golden hour rim; add 1/8 Black Pro-Mist.
- Composition: rule-of-thirds, negative space, leading lines.
- Color: skin‑safe palette; test gray card.
- Post: basic grade, gentle S-curve, HSL skin guard.
""",
    "Graphic Designer": lambda q: f"""**Design Brief**
- Message: {q[:120]}...
- Grid: 8‑pt with 12‑col; baseline 4‑pt.
- Type: Display + Humanist Sans; 1.25 scale.
- Hierarchy: H1 48, H2 28, Body 16; 1.6 leading.
- Color: WCAG AA; 1 accent color only.
- Layout: hero → key value → proof → CTA.
- Export: webp + svg; min CLS shifts.
""",
    "Illustrator": lambda q: f"""**Illustration Plan**
- Prompt: {q[:120]}...
- Thumbs: 3 comps (rule of thirds / central / diagonal).
- Style: textured brushes, 3‑tone palette, soft edge control.
- Process: rough → clean → color key → render → bounce light.
- Delivery: 300dpi CMYK + RGB sRGB.
""",
}

ROLE_SYSTEMS = {
    "Video Director": "You are an award-winning film director. Be concrete and operational.",
    "Game Designer": "You are a senior game designer. Provide systems and scope.",
    "Photographer": "You are a professional photographer. Give settings and light.",
    "Graphic Designer": "You are a brand/layout designer. Stress hierarchy and accessibility.",
    "Illustrator": "You are a concept artist. Provide steps and color guidance.",
}

def ensure_key_for(provider_name: str) -> bool:
    if provider_name == "Anthropic Claude":
        if not st.session_state.get("CLAUDE_API_KEY"):
            st.warning("Enter your Claude API Key in the sidebar or switch to Free Demo mode.")
            return False
    elif provider_name == "OpenAI":
        if not st.session_state.get("OPENAI_API_KEY"):
            st.warning("Enter your OpenAI API Key in the sidebar or switch to Free Demo mode.")
            return False
    return True

# ---------- Chat Assistant ----------
with tab_chat:
    st.subheader(f"💬 {role} — Chat Assistant")
    user_q = st.text_area("Your question / idea:", height=140, placeholder="e.g., Make a moving, intimate short about urban solitude.")

    if st.button("Generate Response"):
        if user_q.strip():
            if provider == "Free Demo (No API)":
                st.markdown(ROLE_TEMPLATES[role](user_q))
            elif provider == "Anthropic Claude":
                if ensure_key_for(provider):
                    try:
                        from anthropic import Anthropic
                        client = Anthropic(api_key=st.session_state["CLAUDE_API_KEY"])
                        msg = client.messages.create(
                            model="claude-3-haiku-20240307",
                            max_tokens=800,
                            system=ROLE_SYSTEMS[role],
                            messages=[{"role": "user", "content": user_q}],
                        )
                        # Claude returns list of content blocks
                        out = ""
                        try:
                            out = "".join([blk.text for blk in msg.content if hasattr(blk, "text")])
                        except Exception:
                            out = str(msg)
                        st.markdown(out)
                    except ModuleNotFoundError:
                        st.error("Missing `anthropic` package. Install with: `pip install anthropic` or use the included requirements.txt.")
                    except Exception as e:
                        st.error(f"Claude API error: {e}")
            elif provider == "OpenAI":
                if ensure_key_for(provider):
                    try:
                        from openai import OpenAI
                        client = OpenAI(api_key=st.session_state["OPENAI_API_KEY"])
                        # Use Chat Completions to avoid Responses API signature issues
                        chat = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": ROLE_SYSTEMS[role]},
                                {"role": "user", "content": user_q},
                            ],
                            temperature=0.7,
                        )
                        st.markdown(chat.choices[0].message.content)
                    except ModuleNotFoundError:
                        st.error("Missing `openai` package. Install with: `pip install openai` or use the included requirements.txt.")
                    except Exception as e:
                        st.error(f"OpenAI API error: {e}")
        else:
            st.info("Please enter a question or idea.")

# ---------- Local Image Generator (always available) ----------
def generate_placeholder_image(text: str, size_str: str) -> Image.Image:
    w, h = map(int, size_str.split("x"))
    # Soft noise background
    arr = np.random.randint(180, 255, (h, w, 3), dtype=np.uint8)
    img = Image.fromarray(arr, "RGB")
    draw = ImageDraw.Draw(img)
    # Text overlay (wrap)
    wrapped = (text[:80] + "…") if len(text) > 80 else text
    # Basic font: default
    draw.rectangle([(0, h-80), (w, h)], fill=(240, 240, 240))
    draw.text((16, h-64), "Prompt:", fill=(40, 40, 40))
    draw.text((16, h-40), wrapped, fill=(10, 10, 10))
    return img

with tab_image:
    st.subheader("🖼️ Image Studio")
    img_prompt = st.text_area("Describe the image:", height=120, placeholder="e.g., Neon rain alley, reflective puddles, cinematic bokeh.")
    size = st.selectbox("Size", ["1024x1024", "768x768", "512x512"], index=1)

    cols = st.columns(2)
    if cols[0].button("Generate (Free Local)"):
        if img_prompt.strip():
            img = generate_placeholder_image(img_prompt, size)
            st.image(img, caption="Local Demo Image", use_container_width=True)
        else:
            st.info("Please enter a description.")

    if provider == "OpenAI":
        if cols[1].button("Generate with OpenAI Images"):
            if ensure_key_for(provider) and img_prompt.strip():
                try:
                    from openai import OpenAI
                    import base64
                    client = OpenAI(api_key=st.session_state["OPENAI_API_KEY"])
                    img_resp = client.images.generate(
                        model="gpt-image-1",
                        prompt=img_prompt.strip(),
                        size=size,
                    )
                    if img_resp and img_resp.data and img_resp.data[0].b64_json:
                        st.image(
                            Image.open(
                                ImageBytes:=
                                None
                            ),
                            caption="Generated Image",
                            use_container_width=True
                        )
                    # Simpler decode/display without PIL:
                    b64 = img_resp.data[0].b64_json
                    st.image(np.frombuffer(base64.b64decode(b64), dtype=np.uint8), caption="Generated Image")
                except ModuleNotFoundError:
                    st.error("Missing `openai` package. Install with: `pip install openai` or use the included requirements.txt.")
                except Exception as e:
                    st.error(f"OpenAI image error: {e}")
    else:
        cols[1].markdown("_Switch provider to **OpenAI** to try real image generation (requires credits)._")

st.markdown("---")
st.caption("Unified Studio — Free Demo ready. Claude/OpenAI optional.")
