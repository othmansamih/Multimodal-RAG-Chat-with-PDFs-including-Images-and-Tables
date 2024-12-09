import os
from src import (
    ChunksProcessor,
    PDFProcessor,
    QuestionAnsweringChain,
    Retriever,
    Summarizer,
    Viusalizer,
    utils
)
from dotenv import load_dotenv
load_dotenv()



if __name__ == "__main__":
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "pdfs/attention-is-all-you-need-paper.pdf")

    pdf_processor = PDFProcessor(
        file_path=file_path
    )
    chunks = pdf_processor.process_pdf()

    """visualizer = Viusalizer(
        file_path=file_path,
        chunks=chunks
    )
    visualizer.plot_chunk(chunks[0])"""

    chunks_processor = ChunksProcessor(chunks)
    documents = chunks_processor.process_chunks()

    summarizer = Summarizer()
    summaries = summarizer.summarize_documents(documents)

    retriever = Retriever()
    retriever.store_documents_and_summaries(documents, summaries)

    question_answering_chain = QuestionAnsweringChain(retriever)
    response = question_answering_chain.invoke("what the authors means by 'attention'?")
    print(response)
