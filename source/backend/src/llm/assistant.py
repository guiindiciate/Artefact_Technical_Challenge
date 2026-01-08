"""
Assistant interface with per-session conversational memory.
"""
from langchain_core.messages import HumanMessage, AIMessage
from llm.graph import create_graph

class AssistantWithMemory:
    """
    Memory-enabled assistant wrapper around the LangGraph workflow.
    """
    def __init__(self):
        self.graph = create_graph()
        self.conversation_history = []

    def chat(self, query: str) -> str:
        """
        Append user message, run the graph, persist history, return last AI reply.
        """
        self.conversation_history.append(HumanMessage(content=query))
        result = self.graph.invoke({"messages": self.conversation_history})
        self.conversation_history = list(result["messages"])

        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage):
                return msg.content
        return "Sorry, I could not process your question."

    def clear_history(self) -> None:
        """
        Reset conversation context.
        """
        self.conversation_history = []
