# PDF Insights Processor

## Overview

**PDF Insights Processor** is a Python-based project that processes PDF files to extract and analyze content, enabling efficient question answering, summarization, and visualization. The system leverages advanced AI models like GPT and Groq, along with a robust document retrieval system for accurate responses to user queries.

---

## Features

1. **PDF Processing**: Extracts text, tables, and images from PDF documents using high-resolution processing.
2. **Chunk Processing**: Categorizes and processes PDF content into structured formats.
3. **Summarization**: Summarizes texts, tables, and images for efficient storage and retrieval.
4. **Document Retrieval**: Implements vector-based and in-memory storage for fast query resolution.
5. **Question Answering**: Answers questions based on the context extracted from PDF documents.
6. **Visualization**: Highlights and visualizes extracted elements like text, tables, and images within the PDF.

---

## Installation

### Prerequisites

Ensure Python 3.8 or later is installed.

### Steps

1. Clone the repository:
    
    ```bash
    git clone https://github.com/your-repo/pdf-insights-processor.git
    cd pdf-insights-processor
    ```
    
2. Install the dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. Configure environment variables by creating a `.env` file:
    
    ```
    OPENAI_API_KEY=<your_openai_api_key>
    GROQ_API_KEY=<your_qroq_api_key>
    ```
    

---

## Project Structure

```
plaintext
Copy code
.
├── pdfs/                        # Directory for input PDF files
├── src/
│   ├── chunks_processor.py      # Processes extracted chunks into structured documents
│   ├── pdf_processor.py         # Extracts content from PDF files
│   ├── qa_chain.py              # Handles question answering based on extracted content
│   ├── retriever.py             # Manages document retrieval
│   ├── summarizer.py            # Summarizes text, tables, and images
│   ├── utils.py                 # Utility functions for image handling
│   ├── visualizer.py            # Visualizes extracted PDF elements
├── main.py                      # Entry point of the application
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation

```

---

## Usage

### 1. Process a PDF

- Place the PDF file in the `pdfs` folder.
- Update the file path in `main.py`:
    
    ```python
    
    file_path = os.path.join(current_dir, "pdfs/your-file-name.pdf")
    ```
    
- Run the script:
    
    ```bash
    python main.py
    ```
    

### 2. Summarization and Storage

The script processes the PDF and stores summaries in a retriever for future use.

### 3. Ask Questions

The system supports natural language queries. Modify `main.py` with your question:

```python
response = question_answering_chain.invoke("Your question here")
print(response)
```

---

## Key Modules

### 1. **PDFProcessor**

- Extracts chunks from a PDF file using the `unstructured` library.
- Parameters like `chunking_strategy` and `max_characters` can be customized.

### 2. **ChunksProcessor**

- Categorizes extracted chunks into text, tables, and images.
- Returns structured documents for downstream processing.

### 3. **Summarizer**

- Summarizes text, tables, and images using models like GPT and Groq.

### 4. **Retriever**

- Stores documents and their summaries in vector and in-memory storage.
- Supports multi-vector retrieval for efficient query resolution.

### 5. **QuestionAnsweringChain**

- Combines retrieval and summarization for precise answers to user queries.

### 6. **Visualizer**

- Plots rectangles and annotations over extracted elements in PDF pages.

---

## Example Output

**Question**: *"What do the authors mean by 'attention'?"*

**Response**:

> "Attention refers to the mechanism that allows the model to focus on relevant parts of the input sequence when generating outputs, improving performance in tasks like translation and summarization."
> 

---

## Known Issues

- **Large PDFs**: Processing very large files may result in high memory usage.
- **Image Analysis**: Limited support for analyzing complex image structures.
