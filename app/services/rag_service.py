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
        document_id: int | None = None,
        min_score: float = 0.0,
    ) -> RAGChatResponse:
        query_embedding = self.embedding_service.embed_text(question)

        sources = self.vector_store_service.search_similar_chunks(
            query_embedding=query_embedding,
            top_k=top_k,
            document_id=document_id,
            min_score=min_score,
        )

        if not sources:
            return RAGChatResponse(
                answer="根据当前文档无法确定。没有检索到足够相关的参考资料。",
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

你必须遵守以下规则：
1. 只能根据【参考资料】回答，不要编造参考资料中没有的信息。
2. 如果参考资料不足以回答问题，必须回答：“根据当前文档无法确定。”
3. 回答中尽量标注引用来源，例如：[资料1]、[资料2]。
4. 不要把自己的常识当作文档事实。
5. 如果多个资料内容重复，只需要综合回答一次。
6. 回答要简洁、清楚、有条理。
""".strip()

        user_prompt = f"""
【参考资料】
{context}

【用户问题】
{question}

请严格基于参考资料回答用户问题，并在关键结论后标注资料编号。
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

        for source in sources:
            context_parts.append(
                f"""
[资料{source.source_index}]
filename: {source.filename}
document_id: {source.document_id}
chunk_id: {source.chunk_id}
chunk_index: {source.chunk_index}
score: {source.score:.4f}
content:
{source.content}
""".strip()
            )

        return "\n\n".join(context_parts)