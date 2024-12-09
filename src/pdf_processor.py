from unstructured.partition.pdf import partition_pdf


class PDFProcessor():
    def __init__(self, file_path):
        self.file_path = file_path
        self.chunks = []
    

    def process_pdf(self):
        self.chunks = partition_pdf(
            filename=self.file_path,
            strategy="hi_res",
            infer_table_structure=True,
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            chunking_strategy="by_title",
            max_characters=10000,
            combine_text_under_n_chars=2000,
            new_after_n_chars=6000
        )
        return self.chunks