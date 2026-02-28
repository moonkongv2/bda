import streamlit as st
import requests

# Fast API backend address
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Private RAG service", page_icon="🤖", layout="wide")
st.title("Private RAG 🤖")

# -- initialize Session State --
# Storage for data maintained even after  refresh
if "token" not in st.session_state:
    st.session_state.token = None
if "doc_id" not in st.session_state:
    st.session_state.doc_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar on left: sign in & upload
with st.sidebar:
    st.header("sign in")
    email = st.text_input("email")
    password = st.text_input("password", type="password")

    if st.button("sign in"):
        # FastAPI OAuth2 requires username/password as form-data
        res = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
        if res.status_code == 200:
            st.session_state.token = res.json().get("access_token")
            st.success("sign-in success!")
        else:
            st.error("sign-in failed. please confirm id/pw.")

    st.divider()

    if st.session_state.token:
        st.header("upload docs")
        uploaded_file = st.file_uploader("upload PDF/TXT files", type=["pdf","txt"])

        # 1. upload new doc
        if st.button("upload and process"):
            if uploaded_file:
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                with st.spinner("uploading doc and saving vector DB..."):
                    res = requests.post(f"{API_URL}/documents/upload", headers=headers, files=files)
                    if res.status_code == 200:
                        st.session_state.doc_id = res.json().get("id")
                        # initialize chat history since new doc is uploaded
                        st.session_state.messages = []
                        st.success(f"upload completed! (doc ID: {st.session_state.doc_id})")
                    else:
                        st.error(f"upload failed: {res.text}")

        st.divider()

        # 2. load uploaded doc
        st.subheader("My docs")
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        res = requests.get(f"{API_URL}/documents/", headers=headers)

        if res.status_code == 200:
            docs = res.json()
            if docs:
                # make dictionary of doc list {id: title}
                doc_options = {doc["id"]: f"[{doc['title']}] {doc['title']}" for doc in docs}
                # choose from select box
                selected_doc_id = st.selectbox(
                    "please choose from my docs",
                    options=list(doc_options.keys()),
                    format_func=lambda x: doc_options[x]
                )
                # Enter chat page with selected document
                if st.button("chat with this document"):
                    st.session_state.doc_id = selected_doc_id
                    st.session_state_message = [] # initialize a chat with selected doc
                    st.success(f"{selected_doc_id} doc is loaded!")
                else:
                    st.info("No uploaded doc")

if st.session_state.doc_id:
    st.header(f"Analyzing doc id {st.session_state.doc_id}")

    # summarization function
    if st.button("3-line-summary"):
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        with st.spinner("AI is summarizing..."):
            res = requests.post(f"{API_URL}/documents/{st.session_state.doc_id}/summarize", headers=headers)
            if res.status_code == 200:
                st.info(res.json().get("summary"))
            else:
                st.error("summarization failed")

    st.divider()
    st.subheader("Ask about docs")

    # show chat history on screen
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # user prompt
    if prompt := st.chat_input("Ask anything about document!"):
        # 1. Add my prompt on screen
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. shoot the prompt to backend(FastAPI)
        with st.chat_message("assistant"):
            with st.spinner("searching in doc..."):
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                res = requests.post(
                    f"{API_URL}/documents/{st.session_state.doc_id}/chat",
                    headers=headers,
                    json={"question": prompt}
                )

                if res.status_code == 200:
                    answer = res.json().get("answer")
                    st.markdown(answer)
                    # save answer to session
                    st.session_state.message.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Failed to answer: {res.text}")
else:
    # if not signed in yet
    if not st.session_state.token:
        st.info("sign in first on left sidebar")
    else:
        st.info("you can chat with AI once you upload doc")

