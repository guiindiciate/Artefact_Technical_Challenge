import uuid
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from llm.assistant import AssistantWithMemory
from observability.context import set_trace_id, clear_tool_used, get_tool_used
from llm.models.models import ChatRequest, ChatResponse, ResetRequest

app = FastAPI(title="Artefact Assistant API")

# Allow Next.js dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (swap to Redis later)
SESSIONS: Dict[str, AssistantWithMemory] = {}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Handle a chat interaction for a given session.

    This endpoint processes a user message within a conversational session,
    maintaining in-memory state and conversational memory across requests.
    A unique trace_id is generated per request to support observability and
    debugging, and the assistant may dynamically route the request to an
    external tool or answer directly via the LLM.

    Flow:
    - Generate and register a unique trace_id for the request context
    - Retrieve or initialize an assistant instance for the session
    - Process the user message via the assistant
    - Identify whether an external tool or the LLM was used
    - Return the assistant reply along with metadata for tracing and observability

    Args:
        req (ChatRequest): Incoming chat payload containing the session ID
                           and the user's message.

    Returns:
        ChatResponse: Assistant reply, tool used to generate the response,
                      and the trace_id associated with the request.
    """
    trace_id = str(uuid.uuid4())
    set_trace_id(trace_id)
    clear_tool_used()

    assistant = SESSIONS.get(req.session_id)
    if assistant is None:
        assistant = AssistantWithMemory()
        SESSIONS[req.session_id] = assistant

    reply = assistant.chat(req.message)
    tool = get_tool_used() or "llm"

    return ChatResponse(reply=reply, tool_used=tool, trace_id=trace_id)


@app.post("/reset")
def reset(req: ResetRequest):
    """
    Reset the conversational memory for a given session.

    This endpoint clears the in-memory conversation history associated
    with the provided session ID. It is useful for restarting a conversation
    without creating a new session identifier.

    Args:
        req (ResetRequest): Payload containing the session ID whose
                            conversation history should be cleared.

    Returns:
        dict: A simple acknowledgment indicating the reset was successful.
    """
    assistant = SESSIONS.get(req.session_id)
    if assistant:
        assistant.clear_history()
    return {"ok": True}

