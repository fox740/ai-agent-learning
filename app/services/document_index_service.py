from app.models.document import DocumentResponse
from app.models.index import DocumentIndexResponse
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


class DocumentIndexService:
    def __init__(self) -> None:
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()

    def index_document(
        self,
        document: DocumentResponse,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ) -> DocumentIndexResponse:
        chunks = self.chunk_service.create_chunks(
            document=document,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        self.vector_store_service.delete_embeddings_by_document(document.id)

        embedding_count = 0

        for chunk in chunks:
            embedding = self.embedding_service.embed_text(chunk.content)

            self.vector_store_service.save_embedding(
                chunk_id=chunk.id,
                document_id=document.id,
                embedding=embedding,
            )

            embedding_count += 1

        return DocumentIndexResponse(
            document_id=document.id,
            status="indexed",
            chunk_count=len(chunks),
            embedding_count=embedding_count,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )