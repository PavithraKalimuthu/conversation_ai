import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Conversational AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------
# CSS
# ---------------------------------------------------

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

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.markdown(
        "<div class='sidebar-title'>🤖 Conversational AI</div>",
        unsafe_allow_html=True
    )

    if st.session_state.logged_in:

        st.success("Logged In")

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.session_state.user_id = ""
            st.session_state.chat = []

            st.rerun()

    else:

        menu = st.radio(
            "Menu",
            [
                "Login",
                "Register"
            ]
        )

# ---------------------------------------------------
# Register
# ---------------------------------------------------

if (not st.session_state.logged_in) and menu == "Register":

    st.title("Create Account")

    username = st.text_input("Username")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        if not username or not email or not password:

            st.warning("Please fill all fields.")

        else:

            try:

                response = requests.post(

                    f"{API_URL}/register",

                    data={
                        "username": username,
                        "email": email,
                        "password": password
                    }

                )

                result = response.json()

                if result.get("success"):

                    st.success("✅ Registration successful. Please login.")

                else:

                    st.error(
                        result.get(
                            "message",
                            "Registration failed."
                        )
                    )

            except Exception as e:

                st.error(str(e))

# ---------------------------------------------------
# Login
# ---------------------------------------------------

elif (not st.session_state.logged_in) and menu == "Login":

    st.title("Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if not email or not password:

            st.warning("Please enter email and password.")

        else:

            try:

                response = requests.post(

                    f"{API_URL}/login",

                    data={

                        "email": email,
                        "password": password

                    }

                )

                result = response.json()

                if result.get("success"):

                    st.session_state.logged_in = True
                    st.session_state.user_id = result["user_id"]

                    st.rerun()

                else:

                    st.error(
                        result.get(
                            "message",
                            "Invalid credentials."
                        )
                    )

            except Exception as e:

                st.error(str(e))

# ---------------------------------------------------
# Chat Screen
# ---------------------------------------------------

if st.session_state.logged_in:

    st.title("🤖 Conversational AI")

    st.caption(
        "FastAPI • Groq • MySQL • MongoDB • ChromaDB"
    )

    st.subheader("📄 Upload Knowledge")

    uploaded = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"]
    )

    if uploaded:

        if st.button("Upload Document"):

            try:

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

                response = requests.post(

                    f"{API_URL}/upload",

                    files=files,

                    data=data

                )

                if response.status_code == 200:

                    st.success("✅ Knowledge uploaded successfully.")

                else:

                    st.error("Upload failed.")

            except Exception as e:

                st.error(str(e))

    st.divider()

    # -----------------------------
    # Chat History
    # -----------------------------

    for role, msg in st.session_state.chat:

        if role == "user":

            st.markdown(

                f"""
                <div class='user-msg'>
                <b>You:</b><br>{msg}
                </div>
                """,

                unsafe_allow_html=True

            )

        else:

            st.markdown(

                f"""
                <div class='bot-msg'>
                <b>Assistant:</b><br>{msg}
                </div>
                """,

                unsafe_allow_html=True

            )

    # -----------------------------
    # Chat Input
    # -----------------------------

    question = st.chat_input("Ask anything...")

    if question:

        question = question.strip()

        if question:

            st.session_state.chat.append(
                ("user", question)
            )

            response_placeholder = st.empty()

            answer = ""

            try:

                response = requests.post(

                    f"{API_URL}/chat",

                    data={

                        "user_id": st.session_state.user_id,

                        "query": question

                    },

                    stream=True,

                    timeout=120

                )

                response.raise_for_status()

                for chunk in response.iter_content(chunk_size=None):

                    if chunk:

                        token = chunk.decode()

                        answer += token

                        response_placeholder.markdown(

                            f"""
                            <div class='bot-msg'>
                            <b>Assistant:</b><br>{answer}
                            </div>
                            """,

                            unsafe_allow_html=True

                        )

                st.session_state.chat.append(
                    ("assistant", answer)
                )

                st.rerun()

            except Exception as e:

                st.error(f"Chat Error: {e}")