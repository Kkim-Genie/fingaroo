from langchain_core.tools import tool
from app.config import get_settings
from app.knowledge.infra.repository.embeddings_repo import EmbeddingsRepository
from app.knowledge.application.embeddings_service import EmbeddingsService

settings = get_settings()

@tool
def search_knowledge_base(query: str) -> str:
    """
    경제 관련 knowledge base에서 query를 기준으로 검색을 수행하고 그 결과를 반환합니다.
    """
    embeddings_repo = EmbeddingsRepository()
    embeddings_service = EmbeddingsService(embeddings_repo=embeddings_repo)

    contexts = embeddings_service.retrieve_by_query(query, 5)

    result_str = "\n".join([f"""<document>
    <content>{context.content}</content>
    </document>\n""" for context in contexts])

    return result_str