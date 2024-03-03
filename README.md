# StableDiffusion DiscordBot
 A midjourney like bot for discord. Powered by StableDiffusion

 
 ![https://raw.githubusercontent.com/Frablock/StableDiffusion-DiscordBot/main/image_cache/coffee.webp](https://raw.githubusercontent.com/Frablock/StableDiffusion-DiscordBot/main/image_cache/coffee.webp)

# Features
 - the famous /imagine command (Text to image)
 - /transform (Image to Image)
 - /inpaint (Precise Image to Image)
 - Compatible with SD 1.5; SD 2; SDXL
 - LoRA support : `<lora:lora_model:1>`
 - Prompt weighting : `(prompt:1.5)`
 - Batch output

# Instalation
 - Install StableDiffusion (With AUTOMATIC1111 WebUI)
   - Make sure the required [dependencies](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Dependencies) are met and follow the instructions available for:
    [NVidia](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-NVidia-GPUs) 
    [AMD GPUs](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-AMD-GPUs)
    [Intel CPUs, Intel GPUs](https://github.com/openvinotoolkit/stable-diffusion-webui/wiki/Installation-on-Intel-Silicon)
 - Put your bot Token in the `.env` file ([How to create a discord bot](https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/))
 - Run your StableDiffusion server (with --api flag; You may need to change the URL in `stable_diffusion.py`)
 - Run `start.py`
- Enjoy

# Todo
 - Remake Inpainting (Commands+Menu)
 - Finish the Localization
 - Make a command to show all the LoRAs
 - Choice between different ratio (SQUARE, TALL, WIDE)

# Licence
Copyright (C) 2024  Frablock

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html).
