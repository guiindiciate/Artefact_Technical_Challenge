from langchain_openai import ChatOpenAI
from llm.models.models import AgentState

from tools.tools import calculator, fx_convert, crypto_convert

TOOLS = [calculator, fx_convert, crypto_convert]

def call_model(state: AgentState) -> dict:
    """
    Invoke the LLM with tool binding enabled.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools(TOOLS)
    resp = llm_with_tools.invoke(state["messages"])
    return {"messages": [resp]}