from fastapi import HTTPException

from app.database import SessionLocal
from app.knowledge.domain.repository.embeddings_repo import IEmbeddingsRepository
from app.knowledge.infra.db_models.embeddings import Embeddings
from app.utils.db_utils import row_to_dict


class EmbeddingsRepository(IEmbeddingsRepository):
    def get_first(self) -> Embeddings:
        with SessionLocal() as db:
            embedding = db.query(Embeddings).first()

        if not embedding:
            raise HTTPException(status_code=422)

        return Embeddings(**row_to_dict(embedding))

    def retrieve_by_query(self, query_embedding: list[float], top_k: int) -> list[Embeddings]:

        with SessionLocal() as db:
            embeddings = db.query(Embeddings).order_by(Embeddings.embedding.l2_distance(query_embedding)).limit(top_k).all()

        if not embeddings:
            return []

        return [Embeddings(**row_to_dict(embedding)) for embedding in embeddings]

    def create(self, embeddings: Embeddings):
        with SessionLocal() as db:
            db.add(embeddings)
            db.commit()
            db.refresh(embeddings)

    def create_many(self, embeddings: list[Embeddings]):
        with SessionLocal() as db:
            db.add_all(embeddings)
            db.commit()

    def delete_by_date_type(self, date: str, type: str):
        with SessionLocal() as db:
            db.query(Embeddings).filter(Embeddings.date == date, Embeddings.origin_type == type).delete()
            db.commit()

    def put_embedding_by_id(self, id: str, embedding: list[float]):
        with SessionLocal() as db:
            db.query(Embeddings).filter(Embeddings.id == id).update({"embedding": embedding})
            db.commit()