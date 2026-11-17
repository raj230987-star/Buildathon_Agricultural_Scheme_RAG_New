
import streamlit as st
import requests

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="வேளாண்மை தோழன் AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F5F7F3;
    }

    [data-testid="stSidebar"] {
        background-color: #102C3A;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    .brand-title {
        color: #FFFFFF;
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .brand-subtitle {
        color: #B9D8CD;
        font-size: 13px;
    }

    .hero {
        background: linear-gradient(120deg, #102C3A, #176B60);
        padding: 35px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 32px;
    }

    .hero p {
        color: #E1F0E9;
        font-size: 16px;
    }

    .info-card {
        background: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #E1E8E0;
        min-height: 135px;
    }

    .info-card h3 {
        color: #176B60;
        margin-top: 0px;
    }

    .info-card p {
        color: #52636A;
        font-size: 14px;
    }

    .section-title {
        color: #173B43;
        font-size: 23px;
        font-weight: 700;
    }

    .stButton > button {
        background-color: #176B60;
        color: white;
        border-radius: 9px;
        border: none;
        min-height: 42px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #105348;
        color: white;
        border: none;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_unique_sources(sources):
    unique_sources = {}

    for source in sources:
        key = (
            source.get("source", "Unknown PDF"),
            source.get("page_number", "Unknown")
        )

        score = source.get("similarity_score", 0)

        if key not in unique_sources:
            unique_sources[key] = source
        else:
            existing_score = unique_sources[key].get(
                "similarity_score", 0
            )

            if score > existing_score:
                unique_sources[key] = source

    return list(unique_sources.values())


def check_backend():
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def display_sources(sources):
    if not sources:
        return

    unique_sources = get_unique_sources(sources)

    with st.expander("📚 View PDF Sources and Page References"):
        for source in unique_sources:
            filename = source.get("source", "Unknown PDF")
            page = source.get("page_number", "Unknown")

            st.markdown(
                f"- **{filename}** — Page {page}"
            )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="brand-title">🌾 வேளாண்மை தோழன் AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'உங்கள் விவசாயத்திற்கு அறிவார்ந்த துணை!'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Main Menu",
        [
            "Dashboard",
            "Ask Agri",
            "Knowledge Base",
            "About"
        ],
        label_visibility="collapsed",
        key="navigation"
    )

    st.session_state.page = page

    st.divider()

    st.markdown("### System Status")

    if check_backend():
        st.success("Backend Connected")
    else:
        st.error("Backend Offline")

    st.caption("FastAPI + Streamlit")

    st.divider()

    if st.button(
        "🗑️ Clear Chat History",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.caption("Agricultural Government Scheme Assistant")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if st.session_state.page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🌾 Welcome to வேளாண்மை தோழன் AI</h1>
        <p>
        AI-Powered Agricultural Government Schemes Assistant
        </p>
        <p>
        Discover agricultural government schemes, understand
        subsidies and find useful information from official
        scheme documents.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Your Smart Agricultural Assistant</div>',
        unsafe_allow_html=True
    )

    st.write("Explore the available features.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>💬 Ask Agri</h3>
            <p>
            Ask questions about agricultural schemes and
            receive AI-generated answers supported by
            PDF references.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Ask Agri →", key="ask_dashboard"):
            st.session_state.page = "Ask Agri"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>📄 Knowledge Base</h3>
            <p>
            Upload agricultural government scheme PDFs
            and build your searchable knowledge database.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Knowledge Base →"):
            st.session_state.page = "Knowledge Base"
            st.rerun()

    st.write("")

    st.markdown(
        '<div class="section-title">How It Works</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>1. Upload</h3>
            <p>Upload agricultural scheme PDF documents.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>2. Search</h3>
            <p>AI searches relevant information using hybrid retrieval.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>3. Understand</h3>
            <p>Get answers with supporting PDF page references.</p>
        </div>
        """, unsafe_allow_html=True)


# --------------------------------------------------
# ASK AGRI
# --------------------------------------------------

elif st.session_state.page == "Ask Agri":

    st.title("💬 Ask Agri")

    st.caption(
        "Ask questions about agricultural government schemes."
    )

    st.info(
        "Example: What is the subsidy available for "
        "agricultural machinery?"
    )

    # Display previous messages

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):
                display_sources(message["sources"])

    # Accept new question

    question = st.chat_input(
        "Type your agricultural question here..."
    )

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        conversation_history = [
            {
                "role": message["role"],
                "content": message["content"]
            }
            for message in st.session_state.messages[:-1]
            if message["role"] in ["user", "assistant"]
        ]

        conversation_history = conversation_history[-10:]

        try:

            with st.spinner(
                "Searching scheme documents and preparing your answer..."
            ):

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question,
                        "top_k": 5,
                        "conversation_history": conversation_history
                    },
                    timeout=240
                )

            if response.status_code == 200:

                data = response.json()

                assistant_message = {
                    "role": "assistant",
                    "content": data.get(
                        "answer",
                        "No answer was returned."
                    ),
                    "sources": data.get("sources", [])
                }

            else:

                assistant_message = {
                    "role": "assistant",
                    "content": f"API Error: {response.text}",
                    "sources": []
                }

        except requests.exceptions.RequestException as error:

            assistant_message = {
                "role": "assistant",
                "content": f"Backend connection error: {error}",
                "sources": []
            }

        except Exception as error:

            assistant_message = {
                "role": "assistant",
                "content": f"Unexpected error: {error}",
                "sources": []
            }

        st.session_state.messages.append(assistant_message)

        st.rerun()


# --------------------------------------------------
# KNOWLEDGE BASE
# --------------------------------------------------

elif st.session_state.page == "Knowledge Base":

    st.title("📄 Knowledge Base")

    st.write(
        "Upload agricultural government scheme PDF documents "
        "to expand the searchable knowledge database."
    )

    st.markdown("### Upload Scheme Document")

    uploaded_file = st.file_uploader(
        "Select a PDF document",
        type=["pdf"],
        help="Only PDF documents are supported."
    )

    if uploaded_file:

        st.success(
            f"Selected document: {uploaded_file.name}"
        )

        if st.button(
            "🚀 Upload and Process PDF",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Extracting text, creating embeddings "
                    "and updating the knowledge database..."
                ):

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }

                    response = requests.post(
                        f"{API_URL}/upload-pdf",
                        files=files,
                        timeout=600
                    )

                if response.status_code == 200:

                    data = response.json()

                    if data.get("status") == "duplicate":

                        st.warning(
                            "This PDF is already available "
                            "in the knowledge database."
                        )

                        st.write(
                            "Existing filename:",
                            data.get("existing_filename")
                        )

                        st.write(
                            "New vectors added:",
                            data.get("vectors_added", 0)
                        )

                    else:

                        st.success(
                            "PDF processed successfully!"
                        )

                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric(
                                "Total Pages",
                                data.get("total_pages", 0)
                            )

                        with col2:
                            st.metric(
                                "New Chunks",
                                data.get("total_chunks", 0)
                            )

                        with col3:
                            st.metric(
                                "Original FAISS",
                                data.get("original_faiss_vectors", 0)
                            )

                        with col4:
                            st.metric(
                                "Multilingual FAISS",
                                data.get("multilingual_faiss_vectors", 0)
                            )

                        st.write(
                            "Filename:",
                            data.get("original_filename")
                        )

                else:

                    st.error(
                        f"Upload failed: {response.text}"
                    )

            except requests.exceptions.RequestException as error:

                st.error(
                    f"Backend connection error: {error}"
                )

    st.divider()

    st.markdown("### Supported Processing")

    st.markdown("""
    - PDF document upload
    - Text extraction and chunking
    - Multilingual embeddings
    - FAISS vector database
    - Duplicate document detection
    - Semantic and keyword retrieval
    """)


# --------------------------------------------------
# ABOUT
# --------------------------------------------------

elif st.session_state.page == "About":

    st.title("ℹ️ About the Project")

    st.markdown("""
    ## 🌾 வேளாண்மை தோழன் AI

    **உங்கள் விவசாயத்திற்கு அறிவார்ந்த துணை!**

    வேளாண்மை தோழன் AI is an AI-powered agricultural
    government scheme assistant designed to help users
    understand agricultural schemes through uploaded
    government documents.

    ### Key Features

    - AI-powered question answering
    - Retrieval-Augmented Generation (RAG)
    - Hybrid search using FAISS and BM25
    - Reciprocal Rank Fusion (RRF)
    - Multilingual query support
    - Context-aware follow-up questions
    - Evidence validation
    - PDF source citations

    ### Technology Stack

    | Component | Technology |
    |---|---|
    | Programming | Python |
    | Frontend | Streamlit |
    | Backend | FastAPI |
    | Embeddings | Hugging Face |
    | Vector Database | FAISS |
    | Keyword Search | BM25 |
    | Ranking | RRF |
    | PDF Processing | PyPDF |
    | AI Generation | OpenAI API |

    ### Important Note

    This application provides information based on
    available uploaded documents. It does not replace
    official government scheme notifications or
    eligibility decisions.
    """)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<center style='color:#718078;font-size:13px;'>"
    "🌾 வேளாண்மை தோழன் AI | AI-Powered Agricultural "
    "Government Schemes Assistant"
    "<br>Powered by Python · Streamlit · FastAPI · FAISS · OpenAI"
    "</center>",
    unsafe_allow_html=True
)
