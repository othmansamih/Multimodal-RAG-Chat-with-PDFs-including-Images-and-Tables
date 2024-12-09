from langchain_openai.chat_models.base import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages.human import HumanMessage


class QuestionAnsweringChain():
    def __init__(self, retriever):
        self.openai_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5
        )
        self.retriever = retriever

    
    def _parse_docs(self, docs):
        texts = [] # it includes tables too (because the tables will be formated as texts)
        images = []

        for doc in docs:
            doc_page_content = doc.page_content
            doc_type = doc.metadata["type"]
            if doc_type == "image":
                images.append(doc_page_content)
            else:
                texts.append(doc_page_content)
        
        return {
            "texts": texts,
            "images": images
        }
    
    
    def _build_prompt(self, question, parsed_context):
        images = parsed_context["images"]
        texts = parsed_context["texts"]
        
        context_text = ""
        if len(texts) > 0:
            for text in texts:
                context_text += f"{text}\n\n"

        prompt_template = f"""
            Answer the question based only on the provided context, which may include text, tables, or below an image input:

            Context: 
            {context_text}

            Question: 
            {question}
        """

        prompt_content = [{"type": "text", "text": prompt_template}]
            
        if len(images) > 0:
            for image in images:
                prompt_content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                    }
                )
            
        return ChatPromptTemplate.from_messages([
            HumanMessage(content=prompt_content)
            ])
    

    def invoke(self, question):
        context = self.retriever.invoke(question)
        parsed_context = self._parse_docs(context)
        prompt = self._build_prompt(question, parsed_context)
        response = self.openai_model.invoke(prompt.messages)
        return response.content