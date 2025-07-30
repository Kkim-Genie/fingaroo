from app.knowledge.domain.repository.embeddings_repo import IEmbeddingsRepository
from app.knowledge.infra.db_models.embeddings import Embeddings
from google import genai
from google.genai.types import EmbedContentConfig
from app.config import get_settings
from app.utils.knowledge_utils import make_weekly_report_dates

settings = get_settings()

class EmbeddingsService:
    def __init__(
        self,
        embeddings_repo: IEmbeddingsRepository,
    ):
        self.embeddings_repo = embeddings_repo    

    def get_first(self) -> Embeddings:
        return self.embeddings_repo.get_first()

    def retrieve_by_query(self, query: str, top_k: int) -> list[Embeddings]:
        query_embedding = self.make_embeddings([query], "query")
        return self.embeddings_repo.retrieve_by_query(query_embedding, top_k)

    def create(self, embeddings: Embeddings):
        return self.embeddings_repo.create(embeddings)

    def create_many(self, embeddings: list[Embeddings]):
        return self.embeddings_repo.create_many(embeddings)

    def make_embeddings(self, contents: list[str], type: str) -> list[float]:
        client = genai.Client(vertexai=True, project=settings.GOOGLE_CLOUD_PROJECT, location=settings.GOOGLE_CLOUD_LOCATION)
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=contents,
            config=EmbedContentConfig(
                task_type="RETRIEVAL_QUERY" if type=="query" else "RETRIEVAL_DOCUMENT",
            ),
        )
        embedding = response.embeddings[0].values

        return embedding

    def delete_embeddings_based_weekly_report(self, end_date: str):
        datesToFetch = make_weekly_report_dates(end_date)
        for date in datesToFetch:
            self.embeddings_repo.delete_by_date_type(date, "news")
            self.embeddings_repo.delete_by_date_type(date, "daily_market_condition")

    def put_embedding_by_id(self, id: str, embedding: list[float]):
        return self.embeddings_repo.put_embedding_by_id(id, embedding)