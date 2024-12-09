from PIL import Image as PILImage
from io import BytesIO
import base64

def display_base64_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = PILImage.open(BytesIO(image_data))
    image.show()
