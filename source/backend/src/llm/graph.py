"""
LangGraph execution graph: LLM node <-> Tools node loop until no tool calls.
"""
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from llm.models.models import AgentState
from tools.tools import calculator, fx_convert, crypto_convert

from llm.llm_call import call_model

load_dotenv()

TOOLS = [calculator, fx_convert, crypto_convert]

def should_continue(state: AgentState) -> str:
    """
    Determine whether the workflow should continue to the tools node or terminate.

    This function inspects the most recent message in the agent state to check
    whether the LLM requested any tool executions. If tool calls are present,
    the graph routes execution to the tools node; otherwise, the workflow ends.

    Args:
        state (AgentState): Current graph state containing the message history.

    Returns:
        str: The next node identifier ("tools") or END to terminate the graph.
    """
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END


def create_graph():
    """
    Build and compile the LangGraph execution workflow.

    The graph consists of:
    - An agent node responsible for LLM inference
    - A tools node responsible for executing external tools
    - A conditional loop that routes between agent and tools until completion

    Returns:
        CompiledGraph: A compiled LangGraph workflow ready for execution.
    """
    wf = StateGraph(AgentState)
    wf.add_node("agent", call_model)
    wf.add_node("tools", ToolNode(TOOLS))
    wf.set_entry_point("agent")
    wf.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    wf.add_edge("tools", "agent")
    return wf.compile()
