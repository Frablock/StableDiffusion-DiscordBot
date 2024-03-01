# StableDiffusion DiscordBot
 A midjourney like bot for discord. Powered by StableDiffusion

 
 ![https://raw.githubusercontent.com/Frablock/StableDiffusion-DiscordBot/main/image_cache/coffee.webp](https://raw.githubusercontent.com/Frablock/StableDiffusion-DiscordBot/main/image_cache/coffee.webp)

# Features
 - the famous /imagine command (Text to image)
 - /transform (Image to Image)
 - /inpaint (Precise Image to Image)
 - Compatible with SD 1.5; SD 2; SDXL
 - LoRA support

# Instalation
 - Install StableDiffusion
   - Make sure the required [dependencies](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Dependencies) are met and follow the instructions available for:
    [NVidia](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-NVidia-GPUs) 
    [AMD GPUs](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-AMD-GPUs)
    [Intel CPUs, Intel GPUs](https://github.com/openvinotoolkit/stable-diffusion-webui/wiki/Installation-on-Intel-Silicon)
 - Put your bot Token in the `.env` file ([How to create a discord bot](https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/))
 - Run your StableDiffusion server (with --api flag; You may need to change the URL in `stable_diffusion.py`)
 - Run `stable_bot.py`
- Enjoy

# Todo
 - Remake Inpainting (Commands+Menu)
 - Localization
 - Make a command to show all the LoRAs
