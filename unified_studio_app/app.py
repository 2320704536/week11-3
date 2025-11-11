
import streamlit as st
from typing import Dict

st.set_page_config(page_title="Role‑based Creative Chatbot", page_icon="🎭", layout="wide")

# ------------------------------- Styles -------------------------------
st.markdown("""
<style>
.block-container {max-width: 1100px;}
.role-desc {background:#e9f0ff;border-left:4px solid #7aa2ff;padding:14px;border-radius:6px;}
.smallcap {color:#6b7280;font-size:13px;}
.hero-title {font-size:36px;font-weight:800;letter-spacing:.2px;}
</style>
""", unsafe_allow_html=True)

# ------------------------------- Sidebar -------------------------------
st.sidebar.subheader("🔑 API & Role Settings")

provider = st.sidebar.selectbox("Choose a provider", ["Auto", "Anthropic Claude", "OpenAI", "Free Demo (No API)"], index=0)

if "CLAUDE_API_KEY" not in st.session_state: st.session_state["CLAUDE_API_KEY"] = ""
if "OPENAI_API_KEY" not in st.session_state: st.session_state["OPENAI_API_KEY"] = ""

# Try to read from secrets if present, but do not require
try:
    if not st.session_state["OPENAI_API_KEY"]:
        st.session_state["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY","")
except Exception:
    pass
try:
    if not st.session_state["CLAUDE_API_KEY"]:
        st.session_state["CLAUDE_API_KEY"] = st.secrets.get("ANTHROPIC_API_KEY","")
except Exception:
    pass

# Key inputs
if provider in ("OpenAI","Auto"):
    val = st.sidebar.text_input("OpenAI API Key", type="password", value=st.session_state["OPENAI_API_KEY"])
    if val: st.session_state["OPENAI_API_KEY"] = val

if provider in ("Anthropic Claude","Auto"):
    val = st.sidebar.text_input("Claude API Key", type="password", value=st.session_state["CLAUDE_API_KEY"])
    if val: st.session_state["CLAUDE_API_KEY"] = val
    # If empty and user picked Claude explicitly, show a gentle prompt (not an error box in main UI)
    if provider == "Anthropic Claude" and not st.session_state["CLAUDE_API_KEY"]:
        st.sidebar.info("请输入 Claude API Key。未填写时将使用本地 Demo。")

# Roles list (expanded per your slides)
ROLES: Dict[str, Dict[str,str]] = {
    "🎬 Video Director": {
        "desc": "Analyzes mood, camera angle, lighting. Speaks in cinematic language (movement, lenses, framing, tone).",
        "system": "You are a professional film director. Always analyze ideas in terms of visual storytelling — camera movement, lens and framing, lighting, color, and emotional beats. Provide a concise shot plan."
    },
    "💃 Dance Instructor": {
        "desc": "Suggests movement, rhythm, expression. Explains body mechanics and choreography blocks.",
        "system": "You are a dance instructor. Provide rhythm/tempo cues, pose-to-pose breakdown, and tips for safe practice and expression."
    },
    "👗 Fashion Stylist": {
        "desc": "Explains color trends, materials, silhouette. Gives outfit matrices and fit rules.",
        "system": "You are a fashion stylist. Give silhouette guidance, color pairing, texture/material tips, and scenario-based outfits."
    },
    "🎭 Acting Coach": {
        "desc": "Teaches emotion delivery, scene breakdown. Practical drills and beats.",
        "system": "You are an acting coach. Provide beats, objectives/obstacles, tactics, and practical drills to deliver the emotion naturally."
    },
    "🖼️ Art Curator": {
        "desc": "Interprets artwork and connects with data/context.",
        "system": "You are an art curator. Analyze composition, color, motif, context, and articulate emotional effect with references."
    },
}

role_label = st.sidebar.selectbox("Choose a role:", list(ROLES.keys()))
st.sidebar.markdown(f"<div class='role-desc'>{ROLES[role_label]['desc']}</div>", unsafe_allow_html=True)

# ------------------------------- Main -------------------------------
st.markdown(f"<div class='hero-title'>Role‑based Creative Chatbot</div>", unsafe_allow_html=True)
st.write("Select a creative role and ask your question!")
st.caption("Built for 'Art & Advanced Big Data' • Role Demo")

st.markdown("<span class='smallcap'>💬 Enter your question or idea:</span>", unsafe_allow_html=True)
user_q = st.text_input("", placeholder="e.g., How can I shoot a dream sequence?")

def local_template_answer(role: str, q: str) -> str:
    q = (q or "").strip() or "your idea"
    if "Video Director" in role:
        return f"""**Cinematic Plan**
- Logline: {q}
- Coverage: WS (geography) → MS (performance) → CU (emotional beats)
- Lenses: 24/35/85mm; shoot around T2.8; ND outdoor
- Movement: slow dolly push; handheld on turning points
- Lighting: soft key + edge; practicals for depth; haze for glow
- Color: muted base, one saturated accent
- Next: 8–12 shot board with time budget"""
    if "Dance Instructor" in role:
        return f"""**Movement Plan**
- Intention: {q}
- Rhythm: 4×8 bars, tempo 96–104 BPM
- Blocks: intro walk → motif A (upper body) → B (footwork) → bridge (turns) → finale pose
- Technique: core engaged, soft knees, breath timing
- Drill: mirror slow → tempo → music; film for review"""
    if "Fashion Stylist" in role:
        return f"""**Style Matrix**
- Vibe: {q}
- Silhouette: 1 fitted + 1 relaxed
- Palette: 1 base, 1 neutral, 1 accent
- Textures: matte + soft sheen
- Looks: smart‑casual (blazer + tee + straight trousers), event (column dress + minimal jewelry)"""
    if "Acting Coach" in role:
        return f"""**Beat Sheet**
- Objective: {q}
- Obstacles: status gap, hidden info
- Tactics: plead → threaten → withdraw → reveal
- Drill: paraphrase + button lines; gesture economy; eye focus triangles
- Note: mark breaths and playable actions"""
    if "Art Curator" in role:
        return f"""**Reading the Work**
- Thesis: {q}
- Composition: rule of thirds / negative space
- Color: limited triad; temperature contrast
- Motif: repetition & variation
- Context: author/time/place; cross‑reference similar works"""
    return q

def try_claude(system_prompt: str, user_prompt: str) -> str:
    # Returns text; raises only for import/setup errors, not shown to user in UI (silent fallback handled by caller)
    from anthropic import Anthropic
    client = Anthropic(api_key=st.session_state.get("CLAUDE_API_KEY",""))
    msg = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=800,
        system=system_prompt,
        messages=[{"role":"user","content": user_prompt}]
    )
    try:
        return "".join([blk.text for blk in msg.content if hasattr(blk, "text")])
    except Exception:
        return str(msg)

def try_openai(system_prompt: str, user_prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=st.session_state.get("OPENAI_API_KEY",""))
    chat = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content": system_prompt},
            {"role":"user","content": user_prompt},
        ],
        temperature=0.7,
    )
    return chat.choices[0].message.content

def auto_fallback_answer(provider_choice: str, role: str, q: str) -> str:
    system = ROLES[role]["system"]
    q = (q or "").strip()
    if not q:
        return "Please type a question first."

    # Explicit Free Demo
    if provider_choice == "Free Demo (No API)":
        return local_template_answer(role, q)

    # Explicit Claude: if key empty → show gentle prompt via sidebar handled above; still return Demo
    if provider_choice == "Anthropic Claude":
        key = st.session_state.get("CLAUDE_API_KEY","")
        if not key:
            return local_template_answer(role, q)
        # If key provided but invalid or any error happens → silent fallback to Demo (no warnings, no red boxes)
        try:
            return try_claude(system, q)
        except Exception:
            return local_template_answer(role, q)

    # Explicit OpenAI: if key empty → demo; on errors → demo (silent)
    if provider_choice == "OpenAI":
        key = st.session_state.get("OPENAI_API_KEY","")
        if not key:
            return local_template_answer(role, q)
        try:
            return try_openai(system, q)
        except Exception:
            return local_template_answer(role, q)

    # Auto mode: try Claude→OpenAI, but NEVER show error/info; silently fall back to Demo
    if provider_choice == "Auto":
        ckey = st.session_state.get("CLAUDE_API_KEY","")
        if ckey:
            try:
                return try_claude(system, q)
            except Exception:
                pass
        okey = st.session_state.get("OPENAI_API_KEY","")
        if okey:
            try:
                return try_openai(system, q)
            except Exception:
                pass
        return local_template_answer(role, q)

    return local_template_answer(role, q)

if st.button("Generate Response"):
    answer = auto_fallback_answer(provider, role_label, user_q)
    st.markdown(answer)
