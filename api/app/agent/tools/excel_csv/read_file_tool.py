from typing import Annotated, Literal
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from app.agent.states.basic_state import GraphState
from app.config import get_settings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import UnstructuredExcelLoader

settings = get_settings()

@tool
def read_file_tool(file_name: str, file_type: Literal["csv", "excel"], state:Annotated[GraphState, InjectedState]) -> str:
    """
    유저가 업로드한 파일의 내용을 조회합니다.
    file_name: 조회할 파일 이름(예: 20250729223112035683.xlsx)
    file_type: 조회할 파일 타입(예: "csv", "excel")
    """

    print("state", state["files"], file_name, file_type)
    target = [file for file in state["files"] if file == file_name]
    if len(target) == 0:
        return "파일이 존재하지 않습니다."

    filename = target[0]
    if file_type == "csv":
        loader = CSVLoader(file_path=settings.UPLOAD_DIRECTORY + "/" + filename)
        docs = loader.load()
        return docs[0].page_content
    elif file_type == "excel":
        loader = UnstructuredExcelLoader(file_path=settings.UPLOAD_DIRECTORY + "/" + filename)
        docs = loader.load()
        return docs[0].page_content

    return target[0].content