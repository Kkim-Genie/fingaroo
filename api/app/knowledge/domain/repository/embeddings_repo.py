from abc import ABCMeta, abstractmethod
from app.knowledge.infra.db_models.embeddings import Embeddings


class IEmbeddingsRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_first(self) -> Embeddings:
        raise NotImplementedError

    @abstractmethod
    def retrieve_by_query(self, query_embedding: list[float], top_k: int) -> list[Embeddings]:
        raise NotImplementedError

    @abstractmethod
    def create(self, embeddings: Embeddings):
        raise NotImplementedError

    @abstractmethod
    def create_many(self, embeddings: list[Embeddings]):
        raise NotImplementedError

    @abstractmethod
    def delete_by_date_type(self, date: str, type: str):
        raise NotImplementedError