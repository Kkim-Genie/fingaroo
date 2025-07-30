from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph.state import CompiledStateGraph
import json
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

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
                    "content": "",
                    "id": msg.id,
                    "tool_name": function_call.get("name"),
                    "usage_metadata": usage_metadata,
                    "arguments": function_call.get("arguments")
                })
            elif(name == "answer_agent"):
                converted.append({
                    "type": "ai", 
                    "content": msg.content,
                    "id": msg.id,
                    "usage_metadata": usage_metadata,
                    "name": name
                })
        elif isinstance(msg, ToolMessage):
            name = msg.name
            converted.append({
                "type": "tool",
                "content": msg.content,
                "id": msg.id,
                "tool_name": name,
                "tool_call_id": msg.tool_call_id
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
                id=msg_dict["id"],
                usage_metadata = msg_dict["usage_metadata"],
                name = msg_dict["name"]
            ))
        elif msg_dict["type"] == "tool":
            converted.append(ToolMessage(
                content=msg_dict["content"],  # type: ignore
                id=msg_dict["id"],
                tool_call_id=msg_dict["tool_call_id"]
            ))
        elif msg_dict["type"] == "tool_call":
            converted.append(AIMessage(
                content="",  # type: ignore
                id=msg_dict["id"],
                additional_kwargs={
                    "function_call": {
                        "name": msg_dict["tool_name"],
                        "arguments": msg_dict["arguments"]
                    }
                },
                usage_metadata=msg_dict["usage_metadata"]
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

async def _stream_graph_internal(
    graph: CompiledStateGraph,
    stream_input: Any,
    config: RunnableConfig,
):
    """Internal function to handle common streaming logic."""
    chat_dict = {
        "messages": [],
        "answer": "",
        "thread_id": config.get("configurable", {}).get("thread_id", ""),
        "__interrupt__": 0
    }
    async for agent, type, metadata in graph.astream(
        stream_input,
        config,
        subgraphs=True,
        stream_mode=["messages", "values"],
    ):
        agent_name = agent[0].split(":")[0] if len(agent) > 0 else ""
        if(type=="values"):
            # for(message) in metadata.get("messages", []):
            #     print(message)
            interrupt_result = metadata.get("__interrupt__", False) # type: ignore
            if(interrupt_result):
                interrupt_data = interrupt_result[0].value
                chat_dict["__interrupt__"] = {
                    "command": interrupt_data["command"], 
                    "payload": interrupt_data["payload"],
                }
                yield f"data:{json.dumps(chat_dict, ensure_ascii=False)}\n\n"
                continue
            messages: List[BaseMessage] = metadata.get("messages", [])  # type: ignore
            chat_dict["messages"] = convert_messages_to_dict(messages)
            yield f"data:{json.dumps(chat_dict, ensure_ascii=False)}\n\n"
        elif(type=="messages" and agent_name == "answer_agent"):
            chat_dict["answer"] += metadata[0].content  # type: ignore
            chat_dict["messages"] = convert_messages_to_dict(
                messages+[AIMessage(content=chat_dict["answer"], name="answer_agent")]
            )
            yield f"data:{json.dumps(chat_dict, ensure_ascii=False)}\n\n"

async def stream_graph(
    graph: CompiledStateGraph,
    inputs: dict,
    config: RunnableConfig,
):
    async for data in _stream_graph_internal(graph, inputs, config):
        yield data

async def stream_graph_interrupt(
    graph: CompiledStateGraph,
    config: RunnableConfig,
    command: Command
):
    async for data in _stream_graph_internal(graph, command, config):
        yield data

async def stream_graph_continue(
    query: str,
    graph: CompiledStateGraph,
    config: RunnableConfig,
):
    async for data in _stream_graph_internal(graph, query, config):
        yield data