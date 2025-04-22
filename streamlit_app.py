# app.py – Streamlit + Google OIDC + OpenAI (production‑only)

import streamlit as st
from openai import OpenAI

# ── 1. force user login ───────────────────────────────────────────
if not st.experimental_user.is_logged_in:
    st.button("Log in with Google", on_click=st.login)   # one‑click OIDC flow&#8203;:contentReference[oaicite:0]{index=0}
    st.stop()

# ── 2. main UI after login ────────────────────────────────────────
st.title("📄 Document question answering")
st.write(
    f"Hi **{st.experimental_user.name}** – upload a document and ask away! "
    "Your OpenAI key stays client‑side."  # personalised greeting&#8203;:contentReference[oaicite:1]{index=1}
)

openai_api_key = st.text_input("OpenAI API key", type="password")
if not openai_api_key:
    st.info("Add your API key to start 🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)

uploaded = st.file_uploader("Upload .txt or .md", type=("txt", "md"))
question  = st.text_area("Ask a question about the doc",
                         placeholder="e.g. Give me a short summary",
                         disabled=uploaded is None)

def gpt_stream(doc: str, q: str):
    for chunk in client.chat.completions.create(
        model="gpt-4o-mini",
        stream=True,
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant; answer using ONLY the document."},
            {"role": "user", "content": f"Document:\n{doc}\n\nQuestion: {q}"}
        ],
    ):
        if (delta := chunk.choices[0].delta.content):
            yield delta  # Streamlit needs plain strings&#8203;:contentReference[oaicite:2]{index=2}

if uploaded and question:
    st.subheader("Answer")
    st.write_stream(gpt_stream(uploaded.read().decode("utf‑8", errors="ignore"),
                               question))

st.divider()
st.button("Log out", on_click=st.logout)   # instant sign‑out&#8203;:contentReference[oaicite:3]{index=3}

