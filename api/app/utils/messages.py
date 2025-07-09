from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph.state import CompiledStateGraph
import json
from langchain_core.runnables import RunnableConfig

def convert_messages_to_dict(messages: List[BaseMessage]) -> List[Dict[str, Any]]:
    converted = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            converted.append({
                "type": "human",
                "content": msg.content,
                "id": msg.id
            })
        elif isinstance(msg, AIMessage):
            additional_kwargs = msg.additional_kwargs
            name = msg.name
            usage_metadata = msg.usage_metadata
            function_call = additional_kwargs.get("function_call")
            if(function_call):
                converted.append({
                    "type": "tool_call",
                    "tool_name": function_call.get("name"),
                    "id": msg.id,
                    "usage_metadata": usage_metadata
                })
            elif(name == "supervisor"):
                converted.append({
                    "type": "ai", 
                    "content": msg.content,
                    "id": msg.id,
                    "usage_metadata": usage_metadata
                })
        elif isinstance(msg, ToolMessage):
            name = msg.name
            converted.append({
                "type": "tool",
                "tool_name": name,
                "content": msg.content,
                "id": msg.id,
            })
        elif isinstance(msg, SystemMessage):
            converted.append({
                "type": "system",
                "content": msg.content,
                "id": msg.id
            })
        else:
            converted.append({
                "type": "unknown",
                "content": msg.content,
                "id": msg.id
            })
    return converted

def convert_dict_to_messages(message_dicts: List[Dict[str, Any]]) -> List[BaseMessage]:
    converted = []
    for msg_dict in message_dicts:
        if msg_dict["type"] == "human":
            converted.append(HumanMessage(
                content=msg_dict["content"],  # type: ignore
                id=msg_dict["id"]
            ))
        elif msg_dict["type"] == "ai":
            converted.append(AIMessage(
                content=msg_dict["content"],  # type: ignore
                id=msg_dict["id"]
            ))
        elif msg_dict["type"] == "tool":
            converted.append(ToolMessage(
                content=msg_dict["content"],  # type: ignore
                id=msg_dict["id"]
            ))
        elif msg_dict["type"] == "system":
            converted.append(SystemMessage(
                content=msg_dict["content"],  # type: ignore
                id=msg_dict["id"]
            ))
        else:
            # 알 수 없는 타입의 경우 HumanMessage로 기본 처리
            continue
    return converted

async def stream_graph(
    graph: CompiledStateGraph,
    inputs: dict,
    config: RunnableConfig,
):
    chat_dict = {
        "messages": [],
        "answer": ""
    }
    async for agent, type, metadata in graph.astream(
        inputs,
        config,
        subgraphs=True,
        stream_mode=["messages", "values"],
    ):
        agent_name = agent[0].split(":")[0] if len(agent) > 0 else ""
        if(type=="values"):
            messages: List[BaseMessage] = metadata["messages"]  # type: ignore
            chat_dict["messages"] = convert_messages_to_dict(messages)
            yield f"{json.dumps(chat_dict)}\n\n"
        elif(type=="messages" and agent_name == "supervisor"):
            chat_dict["answer"] += metadata[0].content  # type: ignore
            yield f"{json.dumps(chat_dict)}\n\n"