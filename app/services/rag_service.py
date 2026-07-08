from app.models.rag import RAGChatResponse, RAGSource
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_store_service import VectorStoreService


class RAGService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.llm_service = LLMService()

    def chat(
        self,
        question: str,
        top_k: int = 3,
    ) -> RAGChatResponse:
        query_embedding = self.embedding_service.embed_text(question)

        sources = self.vector_store_service.search_similar_chunks(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        if not sources:
            return RAGChatResponse(
                answer="当前还没有可检索的文档内容，请先上传并索引文档。",
                sources=[],
            )

        messages = self._build_rag_messages(
            question=question,
            sources=sources,
        )

        answer = self.llm_service.generate_with_messages(messages)

        return RAGChatResponse(
            answer=answer,
            sources=sources,
        )

    def _build_rag_messages(
        self,
        question: str,
        sources: list[RAGSource],
    ) -> list[dict[str, str]]:
        context = self._build_context(sources)

        system_prompt = """
你是一个严谨的 RAG 文档问答助手。

回答规则：
1. 优先根据【参考资料】回答用户问题。
2. 如果参考资料中没有足够信息，请明确说“根据当前文档无法确定”。
3. 不要编造参考资料中没有出现的事实。
4. 回答要清晰、简洁、有条理。
5. 如果资料之间有冲突，要指出冲突。
""".strip()

        user_prompt = f"""
【参考资料】
{context}

【用户问题】
{question}

请基于参考资料回答用户问题。
""".strip()

        return [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

    def _build_context(self, sources: list[RAGSource]) -> str:
        context_parts = []

        for index, source in enumerate(sources, start=1):
            context_parts.append(
                f"""
[资料 {index}]
document_id: {source.document_id}
chunk_id: {source.chunk_id}
chunk_index: {source.chunk_index}
score: {source.score:.4f}
content:
{source.content}
""".strip()
            )

        return "\n\n".join(context_parts)