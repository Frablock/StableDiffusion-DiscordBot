import requests
import base64

from PIL import Image
import tempfile

import random
import os

# Define the URL and the payload to send.
url = "http://127.0.0.1:7860"

async def get_image(aid, txt="", n_txt=""):
        
    # Define the size of the image to generate (SQUARE).
    size = 768

    # Define the payload to send.
    payload = {
        "prompt": txt,
        "negative_prompt": n_txt,
        "steps": 14,
        "width": 960,
        "height":  540,
        "sampler_name" : sampler,
        "style": [style],
        "cfg_scale": 4
    }
    
    # Send said payload to said URL through the API.
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    
    
    iid = "./image_cache/output"+str(aid)+"-"+str(random.randint(0, 99999999))+".png"
    
    # Decode and save the image.
    with open(iid, 'wb') as f:
        f.write(base64.b64decode(r['images'][0]))
    
    return iid

def img_to_base64(img_url):
    # Fetch the image
    response = requests.get(img_url)
    response.raise_for_status()  # Ensure the request was successful

    # Save the image temporarily
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_name = temp_file.name  # Store the temporary file name
        image_size = Image.open(temp_file_name).size

    # Convert the image to base64
    with open(temp_file_name, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Clean up the temporary file
    os.remove(temp_file_name)

    # Return the base64 encoded image
    return encoded_image, image_size

async def sd_inpaint(aid, im, mask_im, p_env, n_p_mod="", denoising=0.75):
    img_base64, img_size = img_to_base64(im.replace(" ",""))
    with open(mask_im, "rb") as image_file:
        mask_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    if not 0<=denoising<=1:
        return
    
    if img_size[0]<=2048 and img_size[1]<=2048:
        img2img_payload = {
            "init_images": [img_base64],
            "prompt": p_env,
            "negative_prompt": n_p_mod,
            "denoising_strength": denoising,
            "steps": 14,
            "width": img_size[0],
            "height": img_size[1],
            "mask": mask_base64,
            "mask_blur" : 4,
            "inpainting_fill": 1,
            "sampler_name" : "DPM++ 2M Karras",
            "initial_noise_multiplier" : 1,
            "inpaint_full_res" : 0,
            "restore_faces" : False,
        }
    
        img2img_response = requests.post(url=f'{url}/sdapi/v1/img2img', json=img2img_payload)
        
        r =img2img_response.json()
                
        iid = "./image_cache/output"+str(aid)+"-"+str(random.randint(0, 99999999))+".png"
        
        # Decode and save the image.
        with open(iid, 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))
    else:
        im = "./the-picture-is-too-large.jpg"
        im1 = Image.open(im)
        im2 = im1.copy()
        iid = "./image_cache/output"+str(aid)+"-"+str(random.randint(0, 99999999))+".png"
        im2.save(iid)


    return iid
async def img2img(aid, im, p_env="", n_p_mod="", denoising=0.6):
    img_base64, img_size = img_to_base64(im.replace(" ",""))
    
    if not 0<=denoising<=1:
        return
    
    if img_size[0]<=2048 and img_size[1]<=2048:
        img2img_payload = {
            "init_images": [img_base64],
            "prompt": p_env,
            "negative_prompt": n_p_mod,
            "denoising_strength": denoising,
            "steps": 14,
            "width": img_size[0],
            "height": img_size[1],
        }
    
        img2img_response = requests.post(url=f'{url}/sdapi/v1/img2img', json=img2img_payload)
        
        r =img2img_response.json()
        
        
        iid = "./image_cache/output"+str(aid)+"-"+str(random.randint(0, 99999999))+".png"
        
        # Decode and save the image.
        with open(iid, 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))
    else:
        im = "./the-picture-is-too-large.jpg"
        im1 = Image.open(im)
        im2 = im1.copy()
        iid = "./image_cache/output"+str(aid)+"-"+str(random.randint(0, 99999999))+".png"
        im2.save(iid)


    return iid


async def get_lora_list():
    response = requests.get(url=f'{url}/sdapi/v1/loras')
    r = response.json()
    l = []
    for ele in r:
        l.append(ele["name"])
    return str(l)
