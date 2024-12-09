from langchain_core.documents import Document


class ChunksProcessor():
    def __init__(self, chunks):
        self.texts = []
        self.tables = []
        self.images = []
        self.chunks = chunks
    

    def process_chunks(self):
        for chunk in self.chunks:
            if "CompositeElement" in str(type(chunk)):
                text = ""
                for element in chunk.metadata.orig_elements:
                    element_dict = element.to_dict()
                    if "Image" in str(type(element)):
                        self.images.append(
                            Document(
                                metadata={"type": "image"},
                                page_content=element_dict["metadata"]["image_base64"]
                            ))
                    else:
                        text += element_dict["text"] + "\n\n"
                self.texts.append(
                    Document(
                        metadata={"type": "text"},
                        page_content=text
                    ))
            
            elif "Table" in str(type(chunk)):
                for element in chunk.metadata.orig_elements:
                    element_dict = element.to_dict()
                    self.tables.append(
                        Document(
                            metadata={"type": "table"},
                            page_content=element_dict["metadata"]["text_as_html"]
                        ))
        
        return {
            "texts": self.texts,
            "tables": self.tables,
            "images": self.images
        }