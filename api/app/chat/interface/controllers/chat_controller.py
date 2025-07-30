from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from app.utils.langgraph import random_uuid
from app.utils.messages import stream_graph, stream_graph_interrupt
from app.agent.states.basic_state import GraphState
from app.agent.graphs.main_agent import main_agent
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langgraph.types import Command
import json

class ChatFirstRequest(BaseModel):
    query: str

class ChatContinueRequest(BaseModel):
    query:str
    thread_id: str

class InterruptRequest(BaseModel):
    payload: Dict[str, Any]
    thread_id: str


router = APIRouter(prefix="/chat", tags=["chat"])

# OPTIONS 메소드 핸들러 추가 - preflight 요청 처리
@router.options("/first")
async def options_first():
    return {"message": "OK"}

@router.options("/continue")
async def options_continue():
    return {"message": "OK"}

@router.options("/interrupt")
async def options_interrupt():
    return {"message": "OK"}

@router.post("/first", status_code=200)
async def chat_first(request: ChatFirstRequest):
    messages: List[BaseMessage] = [HumanMessage(content=request.query)]
    
    inputs = GraphState(
        messages=messages,
        remaining_steps=25,
        is_last_step=False,
        answer=""
    )
    config = RunnableConfig(recursion_limit=20, configurable={"thread_id": random_uuid()})

    graph_app = main_agent()
    return StreamingResponse(stream_graph(graph_app, dict(inputs), config), media_type="text/event-stream")

@router.post("/continue", status_code=200)
async def chat_continue(request: ChatContinueRequest):

    graph_app = main_agent()
    config = RunnableConfig(recursion_limit=20, configurable={"thread_id": request.thread_id})
    saved_state = graph_app.get_state(config)
    graph_app.update_state(config, saved_state.values)


    input = {
        "messages": saved_state.values["messages"] + [HumanMessage(content=request.query)],
        "answer":""
    }

    return StreamingResponse(stream_graph(graph_app, dict(input), config), media_type="text/event-stream")

@router.post("/interrupt", status_code=200)
async def chat_interrupt(request: InterruptRequest):
    graph_app = main_agent()

    config = RunnableConfig(recursion_limit=20, configurable={"thread_id": request.thread_id})

    command = Command(
        resume={"result": json.dumps(request.payload, ensure_ascii=False)}
    )

    return StreamingResponse(stream_graph_interrupt(graph_app, config, command), media_type="text/event-stream")