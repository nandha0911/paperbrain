"""
Generate PaperBrain Project Report as PDF using reportlab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus.flowables import HRFlowable

OUTPUT = "PaperBrain_Project_Report.pdf"

# ── Page Setup ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2.5*cm, leftMargin=2.5*cm,
    topMargin=2.5*cm,   bottomMargin=2.5*cm,
    title="PaperBrain – Project Report",
    author="PaperBrain Team",
)

W, H = A4
NAVY  = colors.HexColor("#0f172a")
BLUE  = colors.HexColor("#1d4ed8")
LGRAY = colors.HexColor("#f1f5f9")
DGRAY = colors.HexColor("#64748b")
WHITE = colors.white
BLACK = colors.HexColor("#1b2029")

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

cover_title = style("CoverTitle",
    fontName="Helvetica-Bold", fontSize=28, textColor=WHITE,
    alignment=TA_CENTER, leading=36, spaceAfter=8)

cover_sub = style("CoverSub",
    fontName="Helvetica", fontSize=14, textColor=colors.HexColor("#bfdbfe"),
    alignment=TA_CENTER, leading=20, spaceAfter=6)

cover_meta = style("CoverMeta",
    fontName="Helvetica", fontSize=11, textColor=colors.HexColor("#94a3b8"),
    alignment=TA_CENTER, leading=16)

ch_num = style("ChNum",
    fontName="Helvetica-Bold", fontSize=10, textColor=BLUE,
    alignment=TA_LEFT, spaceBefore=24, spaceAfter=2)

ch_title = style("ChTitle",
    fontName="Helvetica-Bold", fontSize=20, textColor=NAVY,
    alignment=TA_LEFT, spaceBefore=4, spaceAfter=10, leading=26)

sec_head = style("SecHead",
    fontName="Helvetica-Bold", fontSize=13, textColor=NAVY,
    spaceBefore=14, spaceAfter=6, leading=18)

subsec_head = style("SubSecHead",
    fontName="Helvetica-Bold", fontSize=11, textColor=BLUE,
    spaceBefore=10, spaceAfter=4, leading=15)

body = style("Body",
    fontName="Helvetica", fontSize=10.5, textColor=BLACK,
    alignment=TA_JUSTIFY, leading=16, spaceAfter=8)

bullet_style = style("Bullet",
    fontName="Helvetica", fontSize=10.5, textColor=BLACK,
    leftIndent=18, bulletIndent=6,
    alignment=TA_LEFT, leading=16, spaceAfter=4)

code_style = style("Code",
    fontName="Courier", fontSize=9, textColor=colors.HexColor("#1e3a5f"),
    backColor=LGRAY, leftIndent=12, rightIndent=12,
    leading=14, spaceAfter=8, spaceBefore=4,
    borderPad=6)

toc_head = style("TocHead",
    fontName="Helvetica-Bold", fontSize=13, textColor=NAVY,
    alignment=TA_CENTER, spaceBefore=20, spaceAfter=14)

toc_item = style("TocItem",
    fontName="Helvetica", fontSize=11, textColor=BLACK,
    leftIndent=0, leading=22)

toc_sub = style("TocSub",
    fontName="Helvetica", fontSize=10, textColor=DGRAY,
    leftIndent=22, leading=18)

caption = style("Caption",
    fontName="Helvetica-Oblique", fontSize=9, textColor=DGRAY,
    alignment=TA_CENTER, spaceAfter=10)

# ── Helper functions ──────────────────────────────────────────────────────────
def hr(color=BLUE, thickness=1):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=8, spaceBefore=4)

def thin_hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=6, spaceBefore=6)

def B(txt):   return f"<b>{txt}</b>"
def I(txt):   return f"<i>{txt}</i>"
def Blue(txt): return f'<font color="#1d4ed8">{txt}</font>'

def chapter(num, title):
    return [
        Spacer(1, 0.3*cm),
        Paragraph(f"CHAPTER {num}", ch_num),
        Paragraph(title, ch_title),
        hr(),
        Spacer(1, 0.2*cm),
    ]

def section(title):
    return [Paragraph(title, sec_head)]

def subsection(title):
    return [Paragraph(title, subsec_head)]

def para(text):
    return Paragraph(text, body)

def bull(text):
    return Paragraph(f"• &nbsp; {text}", bullet_style)

def space(h=0.3):
    return Spacer(1, h*cm)

def info_table(rows, col_widths=None):
    if col_widths is None:
        col_widths = [5*cm, 10*cm]
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9.5),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LGRAY]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME",      (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,1), (0,-1), NAVY),
    ]))
    return t

# ── COVER PAGE ────────────────────────────────────────────────────────────────
def cover_page():
    elems = []

    # Dark header block (simulated with a colored table)
    cover_data = [[""]]
    cover_tbl = Table(cover_data, colWidths=[W - 5*cm], rowHeights=[7*cm])
    cover_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("ROUNDEDCORNERS", [12,12,12,12]),
    ]))
    elems.append(cover_tbl)
    elems.append(Spacer(1, -7*cm))  # overlap text on top

    # Overlay text
    elems.append(Spacer(1, 1.2*cm))
    elems.append(Paragraph("🧠 PaperBrain", cover_title))
    elems.append(Paragraph("AI-Powered PDF Question Answering System", cover_sub))
    elems.append(Paragraph("Using Retrieval-Augmented Generation (RAG)", cover_sub))
    elems.append(Spacer(1, 4.5*cm))

    # Divider
    elems.append(HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=20))

    # Meta info table
    meta = [
        ["Project Title", "PaperBrain – PDF RAG Chatbot"],
        ["Technology Stack", "Python, FastAPI, Streamlit, LangChain, ChromaDB, Ollama"],
        ["LLM Model", "phi3:mini (Ollama Local)  |  GPT-4o (Optional)"],
        ["Embedding Model", "BAAI/bge-small-en-v1.5 (Sentence Transformers)"],
        ["Vector Database", "ChromaDB with cosine similarity"],
        ["Year", "2026"],
    ]
    t = info_table(meta, col_widths=[4.5*cm, 10.5*cm])
    elems.append(t)
    elems.append(space(1.5))

    foot_style = style("FootStyle",
        fontName="Helvetica-Oblique", fontSize=9, textColor=DGRAY, alignment=TA_CENTER)
    elems.append(Paragraph("Confidential Project Report  |  All Rights Reserved", foot_style))
    elems.append(PageBreak())
    return elems

# ── TABLE OF CONTENTS ─────────────────────────────────────────────────────────
def toc():
    elems = []
    elems.append(Paragraph("TABLE OF CONTENTS", toc_head))
    elems.append(hr(BLUE, 2))
    elems.append(space(0.4))

    entries = [
        ("1.", "Introduction", ""),
        ("", "1.1 Overview", True),
        ("", "1.2 Objectives", True),
        ("", "1.3 Scope", True),
        ("2.", "Literature Review", ""),
        ("", "2.1 RAG Systems", True),
        ("", "2.2 Vector Databases", True),
        ("", "2.3 LLM Integration", True),
        ("3.", "Problem Description", ""),
        ("", "3.1 Existing System", True),
        ("4.", "System Methodology", ""),
        ("", "4.1 Architecture Overview", True),
        ("", "4.2 RAG Pipeline", True),
        ("", "4.3 Hybrid Search", True),
        ("5.", "System Requirements", ""),
        ("", "5.1 Hardware Requirements", True),
        ("", "5.2 Software Requirements", True),
        ("6.", "Software Description", ""),
        ("", "6.1 Technology Stack", True),
        ("", "6.2 Key Libraries", True),
        ("7.", "Proposed System", ""),
        ("", "7.1 Features", True),
        ("", "7.2 System Design", True),
        ("8.", "System Testing and Implementation", ""),
        ("", "8.1 Testing Strategy", True),
        ("", "8.2 API Endpoints", True),
        ("9.", "Conclusion and Future Enhancements", ""),
        ("", "Appendix", True),
        ("", "References", True),
    ]

    for num, title, is_sub in entries:
        if not is_sub:
            txt = f"{num}  {B(title)}"
            elems.append(Paragraph(txt, toc_item))
        else:
            elems.append(Paragraph(f"    {title}", toc_sub))

    elems.append(PageBreak())
    return elems

# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 1 – INTRODUCTION
# ─────────────────────────────────────────────────────────────────────────────
def ch1():
    e = []
    e += chapter("1", "Introduction")

    e += section("1.1 Overview")
    e.append(para(
        "PaperBrain is an intelligent, privacy-first document question-answering system "
        "that allows users to upload PDF documents and receive accurate, citation-backed "
        "answers using state-of-the-art Artificial Intelligence techniques. Unlike "
        "cloud-based AI services that transmit sensitive data to external servers, "
        "PaperBrain operates entirely on local hardware, ensuring complete data "
        "confidentiality and offline capability."
    ))
    e.append(para(
        "The system leverages Retrieval-Augmented Generation (RAG), a paradigm that "
        "combines the precision of document retrieval with the language fluency of "
        "large language models (LLMs). This approach fundamentally eliminates the "
        "hallucination problem common in standalone LLMs by grounding every answer "
        "in verified document content."
    ))
    e.append(space())

    e += section("1.2 Objectives")
    e.append(para("The primary objectives of this project are:"))
    for obj in [
        "To build a fully offline, local AI system capable of intelligently answering questions from uploaded PDF documents.",
        "To implement a hybrid retrieval pipeline combining semantic vector search with BM25 keyword search for maximum recall accuracy.",
        "To integrate a cross-encoder reranking model that re-scores retrieved chunks for precision before passing them to the LLM.",
        "To provide exact source citations with page numbers and document references for every generated answer.",
        "To support multiple LLM providers (Ollama for local, OpenAI GPT-4o, and Google Gemini) through a unified interface.",
        "To deliver a clean, professional web interface built with Streamlit and a robust REST API built with FastAPI.",
    ]:
        e.append(bull(obj))
    e.append(space())

    e += section("1.3 Scope")
    e.append(para(
        "The scope of this project covers the complete end-to-end pipeline from PDF "
        "ingestion to natural language answer generation. The system supports:"
    ))
    for s in [
        "Upload and processing of single or multiple PDF files (up to 200MB each, 20 files per session).",
        "Automatic text extraction using PyPDF and PDFPlumber with OCR fallback via Tesseract.",
        "Document chunking with configurable overlap to preserve semantic context across boundaries.",
        "Dense vector embeddings using the BAAI/bge-small-en-v1.5 model.",
        "Persistent vector storage in ChromaDB with session-aware document management.",
        "Conversational memory with a configurable context window of 10 messages.",
        "Real-time query caching with a 1-hour TTL for repeated queries.",
    ]:
        e.append(bull(s))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 2 – LITERATURE REVIEW
# ─────────────────────────────────────────────────────────────────────────────
def ch2():
    e = []
    e += chapter("2", "Literature Review")

    e += section("2.1 Retrieval-Augmented Generation (RAG)")
    e.append(para(
        "Retrieval-Augmented Generation was first formally introduced by Lewis et al. (2020) "
        "in their paper 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.' "
        "The core insight was that LLMs, despite their vast parametric knowledge, are "
        "fundamentally limited by their training data cutoff and the inability to consult "
        "external, domain-specific documents at inference time."
    ))
    e.append(para(
        "RAG addresses this by pairing an LLM with a retriever component. When a query "
        "arrives, the retriever fetches the most relevant document chunks from a knowledge "
        "base, and these chunks are prepended to the LLM prompt as grounding context. "
        "This enables the LLM to generate answers that are factually anchored to the "
        "retrieved evidence, dramatically reducing confabulation."
    ))
    e.append(para(
        "Subsequent work by Gao et al. (2023) in 'Retrieval-Augmented Generation for "
        "Large Language Models: A Survey' identified key challenges including retrieval "
        "quality, context window limits, and the integration of structured and unstructured "
        "data — challenges that this project directly addresses."
    ))
    e.append(space())

    e += section("2.2 Vector Databases and Semantic Search")
    e.append(para(
        "Traditional keyword-based information retrieval (IR) systems like BM25 operate "
        "on exact term matching and TF-IDF weighting. While effective for keyword-rich "
        "queries, they fail on paraphrased or semantically equivalent queries that use "
        "different vocabulary."
    ))
    e.append(para(
        "Dense retrieval using sentence embeddings transformed the field. Models such as "
        "SBERT (Sentence-BERT, Reimers & Gurevych, 2019) produce fixed-dimension vector "
        "representations of sentences where semantic similarity corresponds to geometric "
        "proximity in the embedding space. This enables approximate nearest-neighbour (ANN) "
        "search over large document corpora."
    ))
    e.append(para(
        "ChromaDB, used in this project, is an open-source vector database designed for "
        "AI applications. It stores embeddings alongside metadata and supports efficient "
        "cosine-similarity search. Its lightweight design makes it suitable for local "
        "deployment without infrastructure dependencies."
    ))
    e.append(space())

    e += section("2.3 Hybrid Search and Reranking")
    e.append(para(
        "Research by Ma et al. (2021) and subsequent work in the BEIR benchmark "
        "(Thakur et al., 2021) demonstrated that neither pure sparse (BM25) nor pure "
        "dense (embedding) retrieval dominates across all query types. Hybrid retrieval, "
        "combining both signals through interpolation, consistently outperforms either "
        "approach alone."
    ))
    e.append(para(
        "Cross-encoder reranking (introduced in the context of BERT by Nogueira & Cho, 2019) "
        "provides a second-pass precision boost. A cross-encoder processes the query and "
        "each candidate document jointly, producing a fine-grained relevance score. While "
        "computationally more expensive than bi-encoders, it significantly improves "
        "answer precision when applied to a short candidate list."
    ))
    e.append(para(
        "The ms-marco-MiniLM-L-6-v2 model used in PaperBrain is trained on the Microsoft "
        "Machine Reading Comprehension (MS MARCO) passage ranking dataset and achieves "
        "state-of-the-art performance on reranking tasks with minimal latency overhead."
    ))
    e.append(space())

    e += section("2.4 Local LLM Deployment with Ollama")
    e.append(para(
        "The emergence of highly capable small LLMs such as Microsoft's Phi-3 Mini, "
        "Meta's Llama 3, and Mistral 7B has made local, on-device inference practical. "
        "Ollama is an open-source framework that packages LLMs as self-contained "
        "binaries, providing an OpenAI-compatible REST API at localhost. This enables "
        "privacy-preserving deployments where no data leaves the user's machine."
    ))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 3 – PROBLEM DESCRIPTION
# ─────────────────────────────────────────────────────────────────────────────
def ch3():
    e = []
    e += chapter("3", "Problem Description")

    e.append(para(
        "The explosion of digital documents — research papers, legal contracts, technical "
        "manuals, financial reports — has created an information overload problem. "
        "Professionals regularly need to extract specific information from dense, lengthy "
        "documents but lack efficient tools to do so intelligently."
    ))
    e.append(para(
        "Manual reading is time-consuming and error-prone. Keyword search tools return "
        "raw text passages without synthesising an answer. Cloud-based AI assistants "
        "(ChatGPT, Claude, Gemini) raise serious privacy concerns when handling "
        "confidential or proprietary documents."
    ))
    e.append(space())

    e += section("3.1 Existing System")
    e += subsection("3.1.1 Limitations of Current Approaches")

    rows = [
        [B("Approach"), B("Limitation")],
        ["Manual Reading", "Time-consuming; human error; impractical for 100+ page documents"],
        ["Ctrl+F / Keyword Search", "Returns raw excerpts; no answer synthesis; vocabulary mismatch"],
        ["Cloud AI (ChatGPT etc.)", "Sends confidential data to external servers; privacy violation risk"],
        ["Traditional IR Systems", "No semantic understanding; misses paraphrased queries"],
        ["Basic PDF Summarisers", "Summarise entire document; cannot answer targeted questions"],
        ["Copy-paste into ChatGPT", "Context window limits; no multi-document support; insecure"],
    ]
    e.append(info_table(rows, col_widths=[5*cm, 10*cm]))
    e.append(space())

    e += subsection("3.1.2 Gap Analysis")
    e.append(para(
        "The key gap identified is the absence of a tool that simultaneously offers: "
        "(1) intelligent semantic question answering, (2) grounded citation of sources, "
        "(3) complete data privacy through local execution, and (4) support for multiple "
        "documents in a single session. PaperBrain is designed to fill exactly this gap."
    ))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 4 – SYSTEM METHODOLOGY
# ─────────────────────────────────────────────────────────────────────────────
def ch4():
    e = []
    e += chapter("4", "System Methodology")

    e += section("4.1 Architecture Overview")
    e.append(para(
        "PaperBrain follows a clean, service-oriented architecture with three logical tiers: "
        "the frontend (Streamlit UI), the backend API (FastAPI), and the service layer "
        "(PDF processing, vector store, LLM, RAG orchestration, and caching)."
    ))

    arch_rows = [
        [B("Tier"), B("Component"), B("Technology")],
        ["Frontend", "Web User Interface", "Streamlit 1.36"],
        ["API Layer", "REST API Server", "FastAPI + Uvicorn"],
        ["PDF Service", "Text Extraction & Chunking", "PyPDF, PDFPlumber, LangChain"],
        ["Embedding", "Sentence Vectorisation", "BAAI/bge-small-en-v1.5"],
        ["Vector Store", "Semantic Storage & Retrieval", "ChromaDB 0.5"],
        ["Hybrid Search", "BM25 + Vector Fusion", "rank-bm25, ChromaDB"],
        ["Reranking", "Cross-encoder Precision", "ms-marco-MiniLM-L-6-v2"],
        ["LLM Service", "Answer Generation", "Ollama / OpenAI / Gemini"],
        ["Cache", "Query Result Caching", "In-memory LRU Cache"],
    ]
    e.append(info_table(arch_rows, col_widths=[3.5*cm, 5*cm, 6.5*cm]))
    e.append(space())

    e += section("4.2 RAG Pipeline — Step by Step")
    steps = [
        ("Step 1: PDF Upload", "The user uploads one or more PDF files via the Streamlit UI. Files are transmitted to the FastAPI backend via multipart HTTP POST."),
        ("Step 2: Text Extraction", "PDFPlumber extracts text with layout awareness. PyPDF provides a fallback. Tesseract OCR is invoked for scanned pages with no extractable text."),
        ("Step 3: Document Chunking", "LangChain's RecursiveCharacterTextSplitter divides each page's text into overlapping chunks (1000 characters, 200-character overlap) to preserve contextual continuity at boundaries."),
        ("Step 4: Embedding Generation", "Each chunk is transformed into a 384-dimensional dense vector using the BAAI/bge-small-en-v1.5 sentence transformer model running locally on CPU."),
        ("Step 5: Vector Storage", "Chunk vectors and associated metadata (filename, page number, chunk index) are stored persistently in ChromaDB using cosine distance for similarity computation."),
        ("Step 6: Query Processing", "At query time, the user's question is embedded using the same model. A hybrid search is performed: vector similarity search (70% weight) combined with BM25 keyword match (30% weight)."),
        ("Step 7: Reranking", "The top-K retrieved chunks are fed through the cross-encoder reranker alongside the query. Each (query, chunk) pair receives a fine-grained relevance score and the list is re-ordered."),
        ("Step 8: Prompt Construction", "The top-ranked chunks are assembled into a structured prompt that includes the user query, retrieved context, and conversation history for multi-turn dialogue."),
        ("Step 9: LLM Generation", "The prompt is sent to the configured LLM (default: phi3:mini via Ollama). The LLM generates a precise, grounded answer."),
        ("Step 10: Response & Citations", "The answer is returned to the UI alongside structured source citations containing the originating filename, page number, and relevant text excerpt."),
    ]
    for title, desc in steps:
        e.append(Paragraph(f"<b>{title}</b>", subsec_head))
        e.append(para(desc))
    e.append(space())

    e += section("4.3 Hybrid Search Algorithm")
    e.append(para(
        "The hybrid search fuses dense and sparse retrieval signals using a weighted "
        "interpolation formula:"
    ))
    e.append(Paragraph(
        "<i>score = α × vector_score + (1 - α) × bm25_score</i>",
        style("Formula", fontName="Courier-Bold", fontSize=11, textColor=NAVY,
              alignment=TA_CENTER, spaceBefore=6, spaceAfter=6, leading=16)
    ))
    e.append(para(
        "Where α = 0.7 (configurable via HYBRID_SEARCH_ALPHA). The BM25 scores are "
        "normalised to [0,1] before fusion. This formulation allows the system to "
        "leverage semantic understanding for paraphrased queries while retaining keyword "
        "precision for technical terms and proper nouns."
    ))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 5 – SYSTEM REQUIREMENTS
# ─────────────────────────────────────────────────────────────────────────────
def ch5():
    e = []
    e += chapter("5", "System Requirements")

    e += section("5.1 Hardware Requirements")
    hw = [
        [B("Component"), B("Minimum"), B("Recommended")],
        ["Processor", "Intel Core i5 / AMD Ryzen 5", "Intel Core i7 / AMD Ryzen 7 (8+ cores)"],
        ["RAM", "8 GB DDR4", "16 GB DDR4 or higher"],
        ["Storage", "20 GB free space (SSD preferred)", "50 GB+ SSD"],
        ["GPU (optional)", "Not required", "NVIDIA GPU for faster LLM inference"],
        ["Network", "Required for model download", "Offline after initial setup"],
        ["OS", "Windows 10 / Ubuntu 20.04", "Windows 11 / Ubuntu 22.04 / macOS 13+"],
    ]
    e.append(info_table(hw, col_widths=[4*cm, 5.5*cm, 5.5*cm]))
    e.append(space())

    e += section("5.2 Software Requirements")
    sw = [
        [B("Software"), B("Version"), B("Purpose")],
        ["Python", "3.10 – 3.11", "Primary runtime"],
        ["Ollama", "0.3.0+", "Local LLM runner"],
        ["phi3:mini / llama3", "Latest", "Language model"],
        ["Streamlit", "1.36.0", "Web frontend"],
        ["FastAPI", "0.111.1", "REST API backend"],
        ["ChromaDB", "0.5.3", "Vector database"],
        ["LangChain", "0.2.11", "Document processing"],
        ["Sentence-Transformers", "3.0.1", "Embedding model"],
        ["PyTorch", "2.3.1", "Model inference"],
        ["PyPDF / PDFPlumber", "4.3.1 / 0.11.2", "PDF text extraction"],
        ["Tesseract OCR", "5.x", "Scanned PDF support"],
        ["rank-bm25", "0.2.2", "Keyword search"],
        ["Uvicorn", "0.30.1", "ASGI web server"],
    ]
    e.append(info_table(sw, col_widths=[4.5*cm, 3*cm, 7.5*cm]))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 6 – SOFTWARE DESCRIPTION
# ─────────────────────────────────────────────────────────────────────────────
def ch6():
    e = []
    e += chapter("6", "Software Description")

    e += section("6.1 Technology Stack")
    e.append(para(
        "PaperBrain is built entirely in Python 3.11 and uses a carefully chosen set "
        "of open-source libraries that are each best-in-class for their respective tasks."
    ))
    e.append(space(0.2))

    e += subsection("6.1.1 FastAPI")
    e.append(para(
        "FastAPI is a modern, high-performance Python web framework built on Starlette "
        "and Pydantic. It supports asynchronous request handling, automatic OpenAPI "
        "(Swagger) documentation generation, and type-safe request/response validation. "
        "PaperBrain uses FastAPI to expose a RESTful API that the Streamlit frontend "
        "calls for all operations including document upload, query, and health monitoring."
    ))

    e += subsection("6.1.2 Streamlit")
    e.append(para(
        "Streamlit is a Python-native framework for building interactive data applications. "
        "It converts Python scripts into web applications without requiring HTML/CSS/JS "
        "knowledge. PaperBrain's frontend is a Streamlit application styled with custom "
        "CSS following a Groww-inspired design aesthetic: white background, navy blue "
        "accents, Inter typeface, and smooth micro-animations."
    ))

    e += subsection("6.1.3 ChromaDB")
    e.append(para(
        "ChromaDB is an AI-native open-source vector database. It provides persistent "
        "storage of embeddings alongside arbitrary metadata, supports filtered search, "
        "and operates as an embedded database (no separate server process required). "
        "PaperBrain uses ChromaDB's cosine similarity index to retrieve semantically "
        "relevant document chunks in sub-millisecond time."
    ))

    e += subsection("6.1.4 LangChain")
    e.append(para(
        "LangChain provides the document loading, text splitting, and orchestration "
        "primitives used in PaperBrain's ingestion pipeline. Specifically, "
        "RecursiveCharacterTextSplitter is used for chunking, which respects paragraph "
        "and sentence boundaries before falling back to character-level splits."
    ))

    e += subsection("6.1.5 Ollama")
    e.append(para(
        "Ollama is an open-source platform for running large language models locally. "
        "It packages model weights, runtime, and a REST API server into a single "
        "application. Models run as native processes, achieving near-native inference "
        "speed. PaperBrain defaults to phi3:mini, a 3.8B parameter model from Microsoft "
        "that achieves strong performance on instruction-following tasks while fitting "
        "comfortably in 8 GB of RAM."
    ))
    e.append(space())

    e += section("6.2 Key Algorithms and Models")
    alg = [
        [B("Component"), B("Model/Algorithm"), B("Key Property")],
        ["Text Embedding", "BAAI/bge-small-en-v1.5", "384-dim, English-optimised"],
        ["Reranking", "ms-marco-MiniLM-L-6-v2", "Cross-encoder, MS MARCO trained"],
        ["BM25", "rank-bm25 (Okapi BM25)", "Sparse TF-IDF keyword retrieval"],
        ["LLM (default)", "phi3:mini (3.8B)", "Local, instruction-tuned, fast"],
        ["LLM (optional)", "GPT-4o / Gemini 1.5", "Cloud, maximum quality"],
        ["Chunking", "RecursiveCharacterTextSplitter", "1000 chars, 200 overlap"],
        ["Caching", "LRU Cache (TTL=3600s)", "256-entry query result cache"],
    ]
    e.append(info_table(alg, col_widths=[3.5*cm, 5.5*cm, 6*cm]))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 7 – PROPOSED SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
def ch7():
    e = []
    e += chapter("7", "Proposed System")

    e.append(para(
        "PaperBrain is proposed as a complete, production-quality, locally deployable "
        "document intelligence system that combines the best of retrieval-based and "
        "generative AI approaches. The system is designed for researchers, legal "
        "professionals, analysts, students, and anyone who needs to extract knowledge "
        "from PDF documents without compromising privacy."
    ))
    e.append(space())

    e += section("7.1 Core Features")
    features = [
        ("Multi-Document Upload", "Upload up to 20 PDFs simultaneously (200 MB per file). Each document is independently indexed and retrievable."),
        ("Semantic Question Answering", "Ask questions in natural language. The system understands paraphrased and synonym-rich queries through dense embedding search."),
        ("Hybrid Retrieval", "Combines vector search (70%) with BM25 keyword search (30%) for superior recall across both semantic and keyword-specific queries."),
        ("Cross-Encoder Reranking", "Retrieved chunks are reranked using a cross-encoder model trained on MS MARCO for precision-optimised results."),
        ("Cited Answers", "Every answer includes exact source citations: document name, page number, and the relevant text excerpt."),
        ("Conversational Memory", "The system maintains a 10-turn conversation window, enabling follow-up questions and context-aware dialogue."),
        ("OCR Support", "Scanned PDFs and image-based pages are processed using Tesseract OCR, broadening compatibility."),
        ("Query Caching", "Repeated queries are served from an LRU cache with a 1-hour TTL, reducing response latency for common questions."),
        ("Multi-LLM Support", "Switch between Ollama (local, free), OpenAI GPT-4o (cloud, premium), and Google Gemini via environment configuration."),
        ("100% Offline Operation", "After initial model download, the entire system runs without internet connectivity."),
    ]
    for title, desc in features:
        e.append(Paragraph(f"<b>{title}</b>", subsec_head))
        e.append(para(desc))
    e.append(space())

    e += section("7.2 System Design — Data Flow")
    e.append(para(
        "The following describes the complete data flow from document upload to answer delivery:"
    ))
    flow = [
        [B("Stage"), B("Input"), B("Output")],
        ["Upload", "PDF file bytes (multipart POST)", "Stored file, extraction initiated"],
        ["Extraction", "Raw PDF binary", "Plain text with page metadata"],
        ["Chunking", "Page text strings", "List of (text, metadata) tuples"],
        ["Embedding", "Text chunk strings", "384-dimensional float vectors"],
        ["Indexing", "Vectors + metadata", "ChromaDB collection entries"],
        ["Query Embedding", "User question string", "384-dim query vector"],
        ["Hybrid Search", "Query vector + BM25 tokens", "Top-K scored chunks"],
        ["Reranking", "(Query, chunk) pairs", "Reordered chunk list"],
        ["Prompt Build", "Chunks + history + query", "Structured LLM prompt"],
        ["Generation", "LLM prompt", "Natural language answer string"],
        ["Response", "Answer + sources", "JSON response to Streamlit UI"],
    ]
    e.append(info_table(flow, col_widths=[3*cm, 5.5*cm, 6.5*cm]))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 8 – TESTING AND IMPLEMENTATION
# ─────────────────────────────────────────────────────────────────────────────
def ch8():
    e = []
    e += chapter("8", "System Testing and Implementation")

    e += section("8.1 Testing Strategy")
    e.append(para(
        "PaperBrain employs a multi-layer testing approach covering unit tests, "
        "integration tests, and end-to-end validation. The pytest framework is used "
        "with the pytest-asyncio plugin for asynchronous API endpoint testing."
    ))
    e.append(space(0.2))

    e += subsection("8.1.1 Unit Tests")
    for t in [
        "PDFService: Text extraction correctness across normal, scanned, and corrupt PDFs.",
        "ChunkingService: Correct chunk sizes, overlap preservation, and minimum length filtering.",
        "EmbeddingService: Vector dimensionality (384), normalization, and batch processing.",
        "CacheService: TTL expiry, LRU eviction, cache hit/miss rates.",
        "ConfidenceScoring: Correct score computation and threshold filtering.",
    ]:
        e.append(bull(t))
    e.append(space())

    e += subsection("8.1.2 Integration Tests")
    for t in [
        "End-to-end PDF upload → chunk → embed → store pipeline.",
        "Query → hybrid search → rerank → LLM → response pipeline.",
        "Multi-document retrieval: Correct source attribution across multiple indexed PDFs.",
        "Session isolation: Queries in one session do not bleed into another.",
    ]:
        e.append(bull(t))
    e.append(space())

    e += section("8.2 REST API Endpoints")
    api = [
        [B("Method"), B("Endpoint"), B("Description")],
        ["GET",    "/health",               "System health check — LLM status, chunk count, uptime"],
        ["POST",   "/upload",               "Upload and process a PDF file"],
        ["GET",    "/documents",            "List all indexed documents with metadata"],
        ["DELETE", "/documents/{doc_id}",   "Remove a specific document from the index"],
        ["DELETE", "/documents",            "Clear all indexed documents"],
        ["POST",   "/chat",                 "Submit a question and receive a RAG answer"],
        ["GET",    "/chat/history/{session}","Retrieve conversation history for a session"],
        ["DELETE", "/chat/history/{session}","Clear conversation history for a session"],
    ]
    e.append(info_table(api, col_widths=[1.8*cm, 6*cm, 7.2*cm]))
    e.append(space())

    e += section("8.3 Implementation Guide")
    e += subsection("8.3.1 Installation")
    steps = [
        "Clone the repository or extract the project archive.",
        "Create a Python virtual environment: python -m venv venv",
        "Activate: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)",
        "Install dependencies: pip install -r requirements.txt",
        "Install and start Ollama from ollama.ai",
        "Pull the default model: ollama pull phi3:mini",
        "Start the API: python api.py",
        "Start the UI: streamlit run app.py",
        "Open browser at http://localhost:8501",
    ]
    for i, s in enumerate(steps, 1):
        e.append(bull(f"Step {i}: {s}"))
    e.append(space())

    e += subsection("8.3.2 Configuration")
    e.append(para(
        "All configuration is managed via environment variables in the .env file. "
        "Key parameters include:"
    ))
    cfg = [
        [B("Variable"), B("Default"), B("Description")],
        ["LLM_PROVIDER", "ollama", "LLM backend: ollama | openai | gemini"],
        ["OLLAMA_MODEL", "phi3:mini", "Ollama model to use"],
        ["CHUNK_SIZE", "1000", "Characters per chunk"],
        ["CHUNK_OVERLAP", "200", "Overlap between consecutive chunks"],
        ["TOP_K", "5", "Chunks retrieved per query"],
        ["HYBRID_SEARCH_ALPHA", "0.7", "Vector vs BM25 balance (1=pure vector)"],
        ["RERANK_ENABLED", "true", "Enable cross-encoder reranking"],
        ["CONFIDENCE_THRESHOLD", "0.40", "Minimum relevance score to include a chunk"],
    ]
    e.append(info_table(cfg, col_widths=[4.5*cm, 2.5*cm, 8*cm]))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER 9 – CONCLUSION
# ─────────────────────────────────────────────────────────────────────────────
def ch9():
    e = []
    e += chapter("9", "Conclusion and Future Enhancements")

    e += section("9.1 Conclusion")
    e.append(para(
        "PaperBrain successfully demonstrates that production-quality, privacy-preserving "
        "document intelligence is achievable on consumer hardware without cloud dependencies. "
        "By combining retrieval-augmented generation with hybrid search, cross-encoder "
        "reranking, and a clean multi-tier architecture, the system delivers accurate, "
        "citation-backed answers from user-provided PDFs."
    ))
    e.append(para(
        "The project validates several key hypotheses: (1) local LLMs such as phi3:mini "
        "are sufficiently capable for document question-answering tasks, (2) hybrid "
        "retrieval consistently outperforms either pure vector or pure keyword search, "
        "and (3) cross-encoder reranking meaningfully improves answer quality with "
        "acceptable latency overhead."
    ))
    e.append(para(
        "The dual-server architecture (FastAPI backend + Streamlit frontend) provides "
        "clean separation of concerns, making the system extensible and maintainable. "
        "The REST API design allows the backend to be consumed by any frontend — "
        "web, mobile, or CLI — without modification."
    ))
    e.append(space())

    e += section("9.2 Future Enhancements")
    future = [
        ("Table and Image Extraction", "Extend PDF processing to extract structured data from tables using Camelot or Tabula, and analyse images using vision LLMs (LLaVA, GPT-4V)."),
        ("Graph RAG", "Build a knowledge graph from extracted entities and relationships, enabling multi-hop reasoning queries across documents."),
        ("Streaming Responses", "Implement Server-Sent Events (SSE) for token-streaming LLM responses, providing a ChatGPT-like live typing experience."),
        ("Multi-User Support", "Add authentication, per-user document namespaces, and role-based access control for team deployment."),
        ("Web Scraping Source", "Extend the ingestion pipeline to support URLs alongside PDFs, enabling web page and article question-answering."),
        ("Evaluation Dashboard", "Integrate automated RAG evaluation using RAGAS metrics (faithfulness, answer relevancy, context precision) with a visual dashboard."),
        ("Fine-Tuning Support", "Allow domain-specific fine-tuning of the embedding model on user-provided document corpora for specialised retrieval."),
        ("Mobile Application", "Develop a mobile frontend using React Native that communicates with the FastAPI backend via the existing REST API."),
        ("GPU Acceleration", "Add CUDA support for the embedding and reranking models to reduce inference latency on GPU-equipped machines."),
    ]
    for title, desc in future:
        e.append(Paragraph(f"<b>{title}</b>", subsec_head))
        e.append(para(desc))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# APPENDIX
# ─────────────────────────────────────────────────────────────────────────────
def appendix():
    e = []
    e += chapter("", "Appendix")

    e += section("A. Project Directory Structure")
    e.append(Paragraph(
"""\
rag-chatbot/
├── api.py               ← FastAPI application entry point
├── app.py               ← Streamlit frontend entry point
├── config.py            ← Centralised configuration
├── requirements.txt     ← Python dependencies
├── .env                 ← Environment variables (secrets)
├── .streamlit/          ← Streamlit theme configuration
│   └── config.toml
├── frontend/            ← UI components and styles
│   ├── components.py
│   └── styles.py
├── services/            ← Business logic services
│   ├── pdf_service.py
│   ├── vector_store.py
│   ├── llm_service.py
│   ├── rag_service.py
│   └── cache_service.py
├── models/              ← Pydantic request/response models
├── prompts/             ← LLM prompt templates
├── utils/               ← Utility modules (logging, file helpers)
├── chroma_db/           ← ChromaDB persistent storage
├── uploads/             ← Uploaded PDF files
└── logs/                ← Application log files""", code_style))
    e.append(space())

    e += section("B. Environment Variables Reference")
    env_rows = [
        [B("Variable"), B("Default"), B("Description")],
        ["API_HOST", "127.0.0.1", "API server bind address"],
        ["API_PORT", "8000", "API server port"],
        ["LLM_PROVIDER", "ollama", "LLM backend provider"],
        ["OLLAMA_BASE_URL", "http://localhost:11434", "Ollama API URL"],
        ["OLLAMA_MODEL", "phi3:mini", "Default Ollama model"],
        ["OPENAI_API_KEY", "(empty)", "OpenAI API key (optional)"],
        ["GEMINI_API_KEY", "(empty)", "Google Gemini API key (optional)"],
        ["EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5", "HuggingFace embedding model"],
        ["CHUNK_SIZE", "1000", "Chunk size in characters"],
        ["CHUNK_OVERLAP", "200", "Chunk overlap in characters"],
        ["TOP_K", "5", "Chunks per query"],
        ["CONFIDENCE_THRESHOLD", "0.40", "Minimum relevance score"],
        ["HYBRID_SEARCH_ALPHA", "0.7", "Vector search weight"],
        ["RERANK_ENABLED", "true", "Cross-encoder reranking toggle"],
        ["CACHE_ENABLED", "true", "Query cache toggle"],
        ["CACHE_TTL_SECONDS", "3600", "Cache entry TTL (seconds)"],
        ["MAX_FILE_SIZE_MB", "200", "Maximum upload file size"],
    ]
    e.append(info_table(env_rows, col_widths=[4.5*cm, 3.5*cm, 7*cm]))
    e.append(PageBreak())
    return e

# ─────────────────────────────────────────────────────────────────────────────
# REFERENCES
# ─────────────────────────────────────────────────────────────────────────────
def references():
    e = []
    e += chapter("", "References")

    refs = [
        ("[1] Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. "
         "Advances in Neural Information Processing Systems (NeurIPS), 33, 9459–9474."),
        ("[2] Gao, Y., et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. "
         "arXiv preprint arXiv:2312.10997."),
        ("[3] Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese "
         "BERT-Networks. Proceedings of EMNLP 2019."),
        ("[4] Thakur, N., et al. (2021). BEIR: A Heterogeneous Benchmark for Zero-Shot Evaluation of "
         "Information Retrieval Models. NeurIPS 2021 Datasets and Benchmarks Track."),
        ("[5] Nogueira, R., & Cho, K. (2019). Passage Re-ranking with BERT. "
         "arXiv preprint arXiv:1901.04085."),
        ("[6] Abdin, M., et al. (2024). Phi-3 Technical Report: A Highly Capable Language Model "
         "Locally on Your Phone. arXiv preprint arXiv:2404.14219. (Microsoft Research)"),
        ("[7] Robertson, S., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and "
         "Beyond. Foundations and Trends in Information Retrieval, 3(4), 333–389."),
        ("[8] FastAPI Documentation. Sebastián Ramírez. https://fastapi.tiangolo.com/"),
        ("[9] Streamlit Documentation. Snowflake Inc. https://docs.streamlit.io/"),
        ("[10] ChromaDB Documentation. Chroma Core Inc. https://docs.trychroma.com/"),
        ("[11] LangChain Documentation. LangChain Inc. https://python.langchain.com/"),
        ("[12] Ollama Documentation. Ollama Inc. https://ollama.ai/docs"),
        ("[13] Sentence-Transformers Documentation. Nils Reimers. https://sbert.net/"),
        ("[14] BAAI/bge-small-en-v1.5 Model Card. Beijing Academy of Artificial Intelligence. "
         "https://huggingface.co/BAAI/bge-small-en-v1.5"),
        ("[15] ms-marco-MiniLM-L-6-v2 Model Card. UKP Lab. "
         "https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2"),
    ]

    for ref in refs:
        e.append(para(ref))
        e.append(thin_hr())

    return e

# ─────────────────────────────────────────────────────────────────────────────
# BUILD PDF
# ─────────────────────────────────────────────────────────────────────────────
story = []
story += cover_page()
story += toc()
story += ch1()
story += ch2()
story += ch3()
story += ch4()
story += ch5()
story += ch6()
story += ch7()
story += ch8()
story += ch9()
story += appendix()
story += references()

doc.build(story)
print(f"Report saved as {OUTPUT}")
