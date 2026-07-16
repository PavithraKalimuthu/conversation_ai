
import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Conversational AI",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# CSS
# -------------------------

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family: "Segoe UI", sans-serif;
}

.main{
    background:#f5f7fb;
}

h1{
    color:#1f4e79;
    font-weight:700;
}

h2,h3{
    color:#2c3e50;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:45px;
    font-size:16px;
    font-weight:bold;
}

.user-msg{
    background:#DCF8C6;
    padding:12px;
    border-radius:12px;
    margin:8px 0;
}

.bot-msg{
    background:#FFFFFF;
    padding:12px;
    border-radius:12px;
    margin:8px 0;
    border:1px solid #ddd;
}

.sidebar-title{
    font-size:22px;
    font-weight:bold;
    color:#1f4e79;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Session
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "chat" not in st.session_state:
    st.session_state.chat = []

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.markdown(
        "<div class='sidebar-title'>🤖 Conversational AI</div>",
        unsafe_allow_html=True
    )

    menu = st.radio(
        "Menu",
        [
            "Login",
            "Register"
        ]
    )

# -------------------------
# Register
# -------------------------

if menu == "Register" and not st.session_state.logged_in:

    st.title("Create Account")

    username = st.text_input("Username")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        response = requests.post(

            f"{API_URL}/register",

            data={

                "username": username,

                "email": email,

                "password": password

            }

        )

        st.success(response.json()["message"])

# -------------------------
# Login
# -------------------------

elif menu == "Login" and not st.session_state.logged_in:

    st.title("Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = requests.post(

            f"{API_URL}/login",

            data={

                "email": email,

                "password": password

            }

        )

        result = response.json()

        if result["success"]:

            st.session_state.logged_in = True

            st.session_state.user_id = result["user_id"]

            st.rerun()

        else:

            st.error(result["message"])

# -------------------------
# Chat Screen
# -------------------------

if st.session_state.logged_in:

    st.title("🤖 Conversational AI")

    st.caption(
        "FastAPI • Groq • MySQL • MongoDB • ChromaDB"
    )

    uploaded = st.file_uploader(
        "Upload PDF/TXT",
        type=["pdf","txt"]
    )

    if uploaded:

        files = {
            "file": (
                uploaded.name,
                uploaded,
                uploaded.type
            )
        }

        data = {
            "user_id": st.session_state.user_id
        }

        requests.post(
            f"{API_URL}/upload",
            files=files,
            data=data
        )

        st.success("Knowledge uploaded successfully.")

    st.divider()

    for role, msg in st.session_state.chat:

        if role == "user":

            st.markdown(
                f"<div class='user-msg'><b>You:</b><br>{msg}</div>",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"<div class='bot-msg'><b>Assistant:</b><br>{msg}</div>",
                unsafe_allow_html=True
            )

    question = st.chat_input(
        "Ask anything..."
    )

    if question:

        st.session_state.chat.append(
            ("user", question)
        )

        response_placeholder = st.empty()

        answer = ""

        response = requests.post(

            f"{API_URL}/chat",

            data={

                "user_id": st.session_state.user_id,

                "query": question

            },

            stream=True

        )

        for chunk in response.iter_content(
            chunk_size=None
        ):

            if chunk:

                text = chunk.decode()

                answer += text

                response_placeholder.markdown(
                    f"<div class='bot-msg'><b>Assistant:</b><br>{answer}</div>",
                    unsafe_allow_html=True
                )

        st.session_state.chat.append(
            ("assistant", answer)
        )

        st.rerun()