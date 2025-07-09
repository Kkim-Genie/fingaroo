from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from app.utils.langgraph import random_uuid
from app.utils.messages import convert_dict_to_messages, stream_graph
from app.agent.states.basic_state import GraphState
from app.agent.graphs.main_agent import main_agent
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from app.consts import Consts

class ChatRequest(BaseModel):
    query: str
    messages: List[Dict[str, Any]]


router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", status_code=200)
async def chat(request: ChatRequest):
    graph_app = main_agent()
    system_prompt = Consts.SYSTEM_PROMPT

    messages: List[BaseMessage] = convert_dict_to_messages(request.messages)
    if(len(messages) == 0):
        messages = [
            SystemMessage(content=system_prompt),
        ]
    messages.append(HumanMessage(content=request.query))

    print(messages)

    inputs = GraphState(
        messages=messages,
        remaining_steps=25,
        is_last_step=False,
    )
    config = RunnableConfig(recursion_limit=20, configurable={"thread_id": random_uuid()})

    return StreamingResponse(stream_graph(graph_app, dict(inputs), config), media_type="text/event-stream")
