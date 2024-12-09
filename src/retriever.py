from langchain_core.documents import Document
from langchain.storage import InMemoryByteStore
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
import uuid

class Retriever():
    def __init__(self):
        self.vectorstore = Chroma(collection_name="summaries", embedding_function=OpenAIEmbeddings())
        self.store = InMemoryByteStore()
        self.id_key = "doc_id"
        self.retriever = MultiVectorRetriever(
            vectorstore=self.vectorstore,
            byte_store=self.store,
            id_key=self.id_key,
        )

    
    def store_documents_and_summaries(self, documents, summaries):
        texts, tables, images = (v for v in documents.values())
        text_summaries, table_summaries, image_summaries = (v for v in summaries.values())

        text_ids = [str(uuid.uuid4()) for _ in texts]
        table_ids = [str(uuid.uuid4()) for _ in tables]
        image_ids = [str(uuid.uuid4()) for _ in images]

        text_summary_docs = [
            Document(page_content=text, metadata={self.id_key: text_ids[i]})
            for i, text in enumerate(text_summaries)
        ]
        table_summary_docs = [
            Document(page_content=table, metadata={self.id_key: table_ids[i]})
            for i, table in enumerate(table_summaries)
        ]
        image_summary_docs = [
            Document(page_content=image, metadata={self.id_key: image_ids[i]})
            for i, image in enumerate(image_summaries)
        ]

        self.retriever.vectorstore.add_documents(text_summary_docs)
        self.retriever.vectorstore.add_documents(table_summary_docs)
        self.retriever.vectorstore.add_documents(image_summary_docs)

        self.retriever.docstore.mset(list(zip(text_ids, texts)))
        self.retriever.docstore.mset(list(zip(table_ids, tables)))
        self.retriever.docstore.mset(list(zip(image_ids, images)))
    

    def invoke(self, query):
        return self.retriever.invoke(query)