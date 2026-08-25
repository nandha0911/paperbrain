"""
prompts/templates.py
====================
All prompt templates used in the RAG pipeline.
STRICT enforcement: chatbot ONLY answers from uploaded PDFs.
"""

from string import Template


# ─── Main RAG System Prompt ───────────────────────────────────────────────────
RAG_SYSTEM_PROMPT = """You are PaperBrain, an intelligent and helpful document assistant.
Your goal is to answer the user's questions clearly, accurately, and thoroughly using the provided DOCUMENT CONTEXT.

Guidelines:
1. Ground your answers in the provided context passages. Synthesize the information into a clear, easy-to-read response (using bullet points, formatting, and clean explanations).
2. If the user asks for an explanation, overview, summary, or specific details, use all relevant information present in the context to give a complete and helpful answer.
3. If the provided context truly contains NO relevant information to answer the question, politely reply:
   "I don't have information about that in the uploaded documents."
4. Do not make up facts that are not supported by the context."""


# ─── Main RAG User Prompt ─────────────────────────────────────────────────────
RAG_USER_PROMPT_TEMPLATE = Template("""=== DOCUMENT CONTEXT ===
$context
=== END OF DOCUMENT CONTEXT ===

=== CONVERSATION HISTORY ===
$history
=== END OF CONVERSATION HISTORY ===

=== USER QUESTION ===
$question

=== ANSWER ===
""")


# ─── Standalone Question Rephrasing Prompt ───────────────────────────────────
REPHRASE_SYSTEM_PROMPT = """You are a question reformulator.
Given a conversation history and a follow-up question, rephrase the follow-up question
to be standalone and self-contained, preserving the original intent.
Return ONLY the rephrased question, nothing else. No explanation."""

REPHRASE_USER_TEMPLATE = Template("""Conversation History:
$history

Follow-up Question: $question

Rephrased standalone question:""")


# ─── Standard Response Strings ────────────────────────────────────────────────
NO_CONTEXT_RESPONSE = (
    "I don't have information about that in the uploaded documents."
)

LOW_CONFIDENCE_RESPONSE = (
    "I don't have information about that in the uploaded documents."
)

NO_DOCUMENTS_RESPONSE = (
    "No documents have been uploaded yet. Please upload one or more PDF files to get started."
)


def validate_answer(answer: str, context: str) -> str:
    """
    Post-process LLM answer to ensure validity.
    """
    if not answer or not answer.strip():
        return NO_CONTEXT_RESPONSE

    # If context was empty/not found, return standard response
    if not context or context.strip() in ("No relevant context found.", ""):
        return NO_CONTEXT_RESPONSE

    return answer.strip()


def build_rag_prompt(
    context: str,
    question: str,
    history: str = "",
) -> str:
    """
    Build the complete RAG user prompt.

    Args:
        context: Retrieved and formatted chunk context.
        question: User's (possibly rephrased) question.
        history: Formatted conversation history string.

    Returns:
        Formatted prompt string.
    """
    return RAG_USER_PROMPT_TEMPLATE.substitute(
        context=context,
        question=question,
        history=history or "No previous conversation.",
    )


def build_rephrase_prompt(question: str, history: str) -> str:
    """
    Build the question rephrasing prompt.

    Args:
        question: Follow-up question from the user.
        history: Recent conversation history.

    Returns:
        Formatted rephrase prompt string.
    """
    return REPHRASE_USER_TEMPLATE.substitute(
        history=history,
        question=question,
    )


def format_context_chunks(chunks: list[dict]) -> str:
    """
    Format a list of retrieved chunks into a numbered context string.

    Args:
        chunks: List of dicts with keys: text, filename, page_number, score.

    Returns:
        Formatted multi-line context string.
    """
    if not chunks:
        return "No relevant context found."

    parts: list[str] = []
    for i, chunk in enumerate(chunks, start=1):
        source_label = (
            f"[Source {i} | File: {chunk['filename']} | Page: {chunk['page_number']} "
            f"| Relevance: {round(chunk.get('score', 0) * 100)}%]"
        )
        parts.append(f"{source_label}\n{chunk['text'].strip()}")

    return "\n\n---\n\n".join(parts)


def format_history(messages: list[dict], max_turns: int = 10) -> str:
    """
    Format conversation history for inclusion in prompts.

    Args:
        messages: List of dicts with keys: role, content.
        max_turns: Maximum number of turns to include.

    Returns:
        Formatted history string.
    """
    if not messages:
        return ""

    recent = messages[-max_turns:]
    lines: list[str] = []
    for msg in recent:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)
