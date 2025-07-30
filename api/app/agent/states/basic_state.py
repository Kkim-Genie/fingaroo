from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langgraph.prebuilt.chat_agent_executor import StateSchemaType
from langgraph.managed import RemainingSteps, IsLastStep
from langchain_core.messages import BaseMessage
from typing import Sequence

class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    answer: Annotated[str, ""]
    remaining_steps: RemainingSteps
    is_last_step: IsLastStep