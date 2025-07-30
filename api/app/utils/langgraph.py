import random
from IPython.display import Image, display
from langgraph.graph.state import CompiledStateGraph
from langchain_core.runnables import RunnableConfig
from typing import Any, Dict, List, Callable, Optional
import uuid
from langchain_core.messages import BaseMessage
from app.utils.messages import convert_messages_to_dict
import json
from app.config import get_settings
import requests

settings = get_settings()

def visualize_graph(graph, xray=False):
    """
    CompiledStateGraph 객체를 시각화하여 표시합니다.

    이 함수는 주어진 그래프 객체가 CompiledStateGraph 인스턴스인 경우
    해당 그래프를 Mermaid 형식의 PNG 이미지로 변환하여 표시합니다.

    Args:
        graph: 시각화할 그래프 객체. CompiledStateGraph 인스턴스여야 합니다.

    Returns:
        None

    Raises:
        Exception: 그래프 시각화 과정에서 오류가 발생한 경우 예외를 출력합니다.
    """
    try:
        # 그래프 시각화
        if isinstance(graph, CompiledStateGraph):
            display(
                Image(
                    graph.get_graph(xray=xray).draw_mermaid_png(
                        background_color="white",
                    )
                )
            )
    except Exception as e:
        print(f"[ERROR] Visualize Graph Error: {e}")


def generate_random_hash():
    return f"{random.randint(0, 0xffffff):06x}"

async def print_graph(
    graph: CompiledStateGraph,
    inputs: dict,
    config: RunnableConfig,
    isPrintAll: bool = False
):
    async for agent, type, metadata in graph.astream(
        inputs,
        config,
        subgraphs=True,
        stream_mode=["messages", "values"],
    ):
        agent_name = agent[0].split(":")[0] if len(agent) > 0 else ""
        print(agent_name, "(", type, ")")
        if(type=="values"):
            interrupt_result = metadata.get("__interrupt__", False) # type: ignore
            if(interrupt_result):
                print(interrupt_result)
                continue
            messages = metadata.get("messages", []) # type: ignore
            for message in messages:
                print(message)
        elif(type=="messages"):
            print(metadata)
        print("----")
        
async def embedding_string(text: str):
    url = f"https://clovastudio.stream.ntruss.com/v1/api-tools/embedding/v2"

    headers = {
        "Authorization": f"Bearer {settings.CLOVASTUDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text":text
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    embeddig = result["result"]["embedding"]
    return embeddig

def random_uuid():
    return str(uuid.uuid4())