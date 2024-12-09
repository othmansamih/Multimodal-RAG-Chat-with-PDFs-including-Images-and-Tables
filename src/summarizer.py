from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class Summarizer():
    def __init__(self):
        self.qroq_model = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.5
        )
        self.openai_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5
        )

    
    def summarize_documents(self, documents):
        first_prompt_template = """
            Summarize the following table or text. Provide only the summary without any additional commentary.

            Input: 
            {element}
        """
        second_prompt_template = """
            Summarize the following image. Provide only the summary without any additional commentary.
        """

        first_prompt = PromptTemplate.from_template(first_prompt_template)
        messages = [
            (
                "user",
                [
                    {"type": "text", "text": second_prompt_template},
                    {
                        "type": "image_url",
                        "image_url": {"url": "data:image/jpeg;base64,{image_b64}"},
                    }
                ]
            )
        ]
        second_prompt = ChatPromptTemplate.from_messages(messages)

        
        first_summarize_chain = first_prompt | self.qroq_model | StrOutputParser()
        second_summarize_chain = second_prompt | self.openai_model | StrOutputParser()
        
        texts, tables, images = (list(map(lambda x : x.page_content, v)) for v in documents.values())
        text_summaries = first_summarize_chain.batch(texts)
        table_summaries = first_summarize_chain.batch(tables)
        image_summaries = second_summarize_chain.batch(images)

        return {
            "text_summaries": text_summaries,
            "table_summaries": table_summaries,
            "image_summaries": image_summaries
        }
