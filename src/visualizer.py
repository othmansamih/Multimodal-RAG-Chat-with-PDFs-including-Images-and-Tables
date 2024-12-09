import fitz  # PyMuPDF
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image


class Viusalizer():
    def __init__(self, file_path, chunks):
        self.pdf_document = fitz.open(file_path)
        self.chunks = chunks


    def _plot_rectangle_from_pdf_page(self, page, page_number, elements_list, chunk_type):
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        fig, ax = plt.subplots(1, figsize=(13, 13))
        ax.imshow(img)

        for element in elements_list:
            element_metadata = element.to_dict()["metadata"]
            
            points = element_metadata["coordinates"]["points"]
            layout_width = element_metadata["coordinates"]["layout_width"]
            layout_height = element_metadata["coordinates"]["layout_height"]

            points = [(x * pix.width / layout_width, y * pix.height / layout_height) for x, y in points]

            rect = Polygon(points, linewidth=1, edgecolor='green', facecolor="none")
            ax.add_patch(rect)

            min_x = min(point[0] - 60 for point in points)
            min_y = min(point[1] for point in points)

            ax.text(min_x, min_y, chunk_type, color='green', fontsize=8, ha='left', va='bottom')

        ax.axis('off')
        plt.title(f'Rectangles on Page {page_number}')
        plt.show()


    def plot_chunk(self, chunk):
        chunk_type = chunk.to_dict()["type"]

        for page_number in range(1, self.pdf_document.page_count + 1):
            page = self.pdf_document[page_number - 1]

            elements_list = []

            elements = chunk.metadata.orig_elements
            for element in elements:
                element_metadata = element.to_dict()["metadata"]

                if element_metadata["page_number"] == page_number:
                    elements_list.append(element)

            if elements_list:
                self._plot_rectangle_from_pdf_page(page, page_number, elements_list, chunk_type)

        self.pdf_document.close()