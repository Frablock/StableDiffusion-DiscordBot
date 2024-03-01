from PIL import Image, ImageDraw
import random
import requests
import tempfile
import os

def create_image_mask(img_url, x, y, size):
    # Fetch the image
    response = requests.get(img_url)
    response.raise_for_status()  # Ensure the request was successful

    # Save the image temporarily
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_name = temp_file.name  # Store the temporary file name
        image_size = Image.open(temp_file_name).size

    # Load the image
    image_path = temp_file_name
    image = Image.open(image_path)

    # Draw a rectangle on the image
    # Parameters: (x, y, width, height)
    draw = ImageDraw.Draw(image)
    im = Image.new(mode="RGB", size=image_size)
    draw2 = ImageDraw.Draw(im)
    
    rectangle_position = (x, y, x+size, y+size) # Example rectangle position and size
    draw.rectangle(rectangle_position, outline="red", width=5)
    draw2.rectangle(rectangle_position, fill="white")

    iid ="./image_cache/output-"+str(random.randint(0, 99999999))+".png"
    mid ="./image_cache/maskoutput-"+str(random.randint(0, 99999999))+".png"

    # Save the image with the rectangle
    image.save(iid)
    im.save(mid)

    os.remove(temp_file_name)
    return iid, mid
