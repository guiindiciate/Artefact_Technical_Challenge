from contextvars import ContextVar
from typing import Optional

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")
tool_used_var: ContextVar[Optional[str]] = ContextVar("tool_used", default=None)


def set_trace_id(trace_id: str) -> None:
    """
    Set the trace_id for the current request context.
    """
    trace_id_var.set(trace_id)


def mark_tool_used(name: str) -> None:
    """
    Record the last tool used in the current request context.
    """
    tool_used_var.set(name)


def get_tool_used() -> Optional[str]:
    """
    Get the last tool used for the current request (if any).
    """
    return tool_used_var.get()


def clear_tool_used() -> None:
    """
    Clear tool usage marker for the current request.
    """
    tool_used_var.set(None)
