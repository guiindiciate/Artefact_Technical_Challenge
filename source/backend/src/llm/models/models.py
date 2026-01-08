from typing import Annotated, Sequence, TypedDict
import operator
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

# Agent State for workflow graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# CHAT INTERACTION - main.py
class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    tool_used: str
    trace_id: str

class ResetRequest(BaseModel):
    session_id: str