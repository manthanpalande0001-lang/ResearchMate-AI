import streamlit as st
from research import search_web
from ai_engine import generate_research
from history import save_history, get_history

from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="ResearchMate AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

/* GENERAL PAGE */

.stApp {
    background-color: #ffffff;
    color: #202124;
    font-family: Arial, sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* TOP TOOLBAR */

header[data-testid="stHeader"] {
    background-color: #ffffff !important;
}

[data-testid="stToolbar"] {
    background-color: #ffffff !important;
}

[data-testid="stHeader"] button {
    color: #202124 !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #f8fafb;
    border-right: 1px solid #e8ecef;
    min-width: 270px;
}

section[data-testid="stSidebar"] > div {
    padding: 2rem 1.2rem;
}

section[data-testid="stSidebar"] * {
    color: #30343b;
}

/* SIDEBAR BRAND */

.brand {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.8px;
    color: #202124;
    padding: 8px 0;
    white-space: nowrap;
}

.brand span {
    color: #168b91;
}

.sidebar-caption {
    font-size: 13px;
    color: #858b93;
    margin-top: 3px;
    margin-bottom: 25px;
}

/* SIDEBAR RADIO BUTTONS */

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 10px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 10px 12px;
    border-radius: 9px;
    font-size: 15px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: #eaf4f4;
}

/* POWERED BY */

.powered-title {
    color: #90969e;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 20px;
    margin-bottom: 12px;
}

/* HOME PAGE */

.main-title {
    font-size: 43px;
    font-weight: 800;
    letter-spacing: -1.8px;
    color: #202124;
    text-align: center;
    margin-top: 65px;
    margin-bottom: 10px;
}

.subtitle {
    color: #777e87;
    font-size: 17px;
    text-align: center;
    margin-bottom: 38px;
}

/* SEARCH INPUT */

div[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #202124 !important;
    border: 1px solid #dfe3e8 !important;
    border-radius: 15px !important;
    min-height: 60px;
    padding: 15px 20px !important;
    font-size: 16px !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04);
}

div[data-testid="stTextInput"] input:focus {
    border-color: #168b91 !important;
    box-shadow: 0 0 0 2px rgba(22, 139, 145, 0.10);
}

/* SEARCH BUTTON */

div.stButton > button {
    background-color: #168b91;
    color: #ffffff !important;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    min-height: 48px;
    transition: 0.2s;
}

div.stButton > button:hover {
    background-color: #11777c;
    color: #ffffff !important;
    border: none;
}

/* DOWNLOAD BUTTON */

div.stDownloadButton > button {
    background-color: #edf8f8;
    color: #168b91 !important;
    border: 1px solid #d5e9e9;
    border-radius: 10px;
    font-weight: 600;
}

/* REPORT SECTION */

.report-title {
    font-size: 28px;
    font-weight: 750;
    color: #202124;
    margin-top: 25px;
    margin-bottom: 10px;
}

/* SOURCE CARDS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #e8ecef;
    border-radius: 12px;
    background-color: #ffffff;
}

/* EXPANDERS */

div[data-testid="stExpander"] {
    border: 1px solid #e8ecef;
    border-radius: 12px;
    background-color: #ffffff;
}

/* DIVIDER */

hr {
    border-color: #edf0f2;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #9299a1;
    font-size: 12px;
    padding: 35px 10px;
    margin-top: 40px;
}

/* RESPONSIVE DESIGN */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .main-title {
        font-size: 32px;
        margin-top: 35px;
    }

    .subtitle {
        font-size: 14px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================
# PDF GENERATION
# =========================================

def create_pdf(report, results):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(
        Paragraph(
            "ResearchMate AI - Research Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    safe_report = report.encode(
        "latin-1",
        errors="replace"
    ).decode("latin-1")

    content.append(
        Preformatted(
            escape(safe_report),
            styles["Code"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Research Sources",
            styles["Heading2"]
        )
    )

    for result in results:

        content.append(
            Paragraph(
                escape(result["title"]),
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                escape(result["link"]),
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 12))

    pdf.build(content)

    buffer.seek(0)

    return buffer.getvalue()


# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.markdown(
        '<div class="brand">Research<span>Mate</span> AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-caption">'
        'Your AI research companion'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "MENU",
        [
            "Home",
            "Research History",
            "About"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        '<div class="powered-title">POWERED BY</div>',
        unsafe_allow_html=True
    )

    st.caption("⚡ Groq AI")
    st.caption("🐍 Python")
    st.caption("🌐 Web Search")


# =========================================
# HOME PAGE
# =========================================

if page == "Home":

    st.markdown(
        '<div class="main-title">'
        'Where knowledge begins.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Ask anything. Explore sources. Discover insights.'
        '</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Research topic",
        placeholder="Ask anything or enter a research topic...",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        generate = st.button(
            "Search and Research →",
            use_container_width=True
        )

    if generate:

        if topic.strip():

            try:

                with st.spinner("Searching the web..."):

                    results = search_web(topic)

                if not results:

                    st.warning("No search results found.")

                else:

                    summary = ""

                    for result in results:

                        summary += f"""
Title: {result['title']}
Description: {result['body']}
Source: {result['link']}

"""

                    with st.spinner(
                        "ResearchMate is analysing sources..."
                    ):

                        report = generate_research(summary)

                    save_history(topic, report)

                    st.session_state["report"] = report
                    st.session_state["results"] = results
                    st.session_state["topic"] = topic

                    st.success("Research completed!")

            except Exception as e:

                st.error(f"Something went wrong: {e}")

        else:

            st.warning("Please enter a research topic.")

    # DISPLAY REPORT

    if "report" in st.session_state:

        st.divider()

        st.markdown(
            '<div class="report-title">Research Results</div>',
            unsafe_allow_html=True
        )

        st.caption(
            f"Research topic: {st.session_state['topic']}"
        )

        st.markdown(
            st.session_state["report"]
        )

        # PDF DOWNLOAD

        pdf_file = create_pdf(
            st.session_state["report"],
            st.session_state["results"]
        )

        st.download_button(
            "Download Research Report (PDF)",
            data=pdf_file,
            file_name="ResearchMate_Report.pdf",
            mime="application/pdf"
        )

        # SOURCES

        st.divider()

        st.subheader("Sources")

        for index, result in enumerate(
            st.session_state["results"],
            start=1
        ):

            with st.container(border=True):

                st.markdown(
                    f"**{index}. {result['title']}**"
                )

                st.caption(result["body"])

                st.markdown(
                    f"[Visit source ↗]({result['link']})"
                )

    else:

        st.markdown(
            '<div class="footer">'
            'ResearchMate AI · Explore knowledge intelligently.'
            '</div>',
            unsafe_allow_html=True
        )


# =========================================
# RESEARCH HISTORY
# =========================================

elif page == "Research History":

    st.title("Research History")

    st.caption("Your previous research reports.")

    history = get_history()

    if history:

        for item in reversed(history):

            with st.expander(item["topic"]):

                st.markdown(item["report"])

    else:

        st.info("No research history available yet.")


# =========================================
# ABOUT PAGE
# =========================================

elif page == "About":

    st.title("About ResearchMate AI")

    st.write("""
    ResearchMate AI is an AI-powered research assistant
    that helps users discover information and generate
    structured research reports.

    ### Features

    - Web search
    - AI-powered research
    - Structured reports
    - PDF downloads
    - Research history

    ### Technology Stack

    - Python
    - Streamlit
    - Groq API
    - DuckDuckGo Search
    - ReportLab
    """)


# =========================================
# FOOTER
# =========================================

if page != "Home" or "report" in st.session_state:

    st.markdown("""
    <div class="footer">
        ResearchMate AI · Explore knowledge intelligently.
    </div>
    """, unsafe_allow_html=True)