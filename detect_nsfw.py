from PIL import Image
from transformers import pipeline

classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")

def detect_nsfw(image):
    img = Image.open(image)

    ret = classifier(img)

    return ret[0]["label"] == "nsfw"
