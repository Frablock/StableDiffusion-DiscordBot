# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 15:20:32 2024

@author: user
"""

from dotenv import dotenv_values

from stable_diffusion import *

from interactions import OptionType, slash_option, slash_command, SlashContext, Embed
import interactions

from interactions import Client, Intents, listen

from discord import File

import asyncio

import random

import re

from interactions import Button, ButtonStyle, ActionRow, StringSelectMenu, StringSelectOption 
from interactions.api.events import Component
from interactions import Modal, ParagraphText, ShortText, SlashContext, slash_command, modal_callback, ModalContext

import mask

messages_attente = [
    "Veuillez patienter pendant que le hamster dans le CPU fait tourner sa roue.",
    "Attendez un instant, nous sommes en train de convaincre les électrons de se déplacer plus rapidement.",
    "Nous sommes en pause café avec le serveur, ça ne devrait pas prendre trop longtemps.",
    "En cours de chargement... Nos programmeurs sont à la recherche de leur tasse de café perdue.",
    "Attendez s'il vous plaît, nous sommes en train de négocier avec le Wi-Fi pour qu'il soit plus rapide.",
    "Le lutin dans le disque dur travaille dur pour retrouver votre fichier. Merci de patienter.",
    "Nous faisons une séance de méditation avec le processeur pour améliorer sa concentration. Merci pour votre patience.",
    "Veuillez attendre que le peintre dans le GPU ait terminé de choisir les couleurs de votre œuvre d'art numérique.",
    "Nous sommes en train de compter jusqu'à l'infini. Soyez patient, cela peut prendre un certain temps.",
    "Attendez s'il vous plaît, le serveur est en train de jongler avec des bits. Ça peut prendre un moment.",
]


bot = Client(intents=Intents.DEFAULT)

TOKEN = dotenv_values(".env")["TOKEN"]

bot = interactions.Client(token=TOKEN)

@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@slash_command(name="imagine", description="Generate a picture using StableDiffusion")
@slash_option(
    name="prompt",
    description="What you want to see",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="negative_prompt",
    description="What you don't want to see",
    required=False,
    opt_type=OptionType.STRING
)
async def generate(ctx: SlashContext, prompt: str = "", negative_prompt: str = ""):
    await ctx.send(random.choice(messages_attente), ephemeral=True)

    image = await get_image(ctx.author,prompt,negative_prompt)

    # Update the response after processing is complete
    await ctx.send(content="Processing complete!\n"+prompt+"\nNegatives : "+negative_prompt, files=[image])
    os.remove(image)
    
@slash_command(name="transform", description="Transform a picture using StableDiffusion")
@slash_option(
    name="image_url",
    description="Original image URL to transform (PNG, JPG, GIF)",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="prompt",
    description="What you want to see",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="negative_prompt",
    description="What you don't want to see",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="denoising",
    description="How similar should it be (0.0 MAX - 1.0 MIN)",
    required=False,
    opt_type=OptionType.NUMBER
)
async def transform(ctx: SlashContext, image_url: str, prompt: str = "", negative_prompt: str = "", denoising: float = 0.5):
    await ctx.send(random.choice(messages_attente), ephemeral=True)

    if not 0<=denoising<=1:
        await ctx.send("Incorrect denoising",ephemeral=True)
        return
        
    try:
        image = await img2img(ctx.author,image_url,prompt,negative_prompt, denoising)
    except Exception as e:
        await ctx.send(str(e)+"\nI can't access to this image, please ensure that you give me a working url next time",ephemeral=True)
        return

    # Update the response after processing is complete
    await ctx.send(content="Processing complete!\n"+prompt+"\nNegatives : "+negative_prompt+"\nImage : "+image_url, files=[image])
    os.remove(image)
    


inpaint_action_menu: list[ActionRow] = [
    ActionRow(
        StringSelectMenu(
            StringSelectOption(
                label="Bigger",
                emoji="<:zoomin:972506443938934814>",
                value="bigger"
            ),
            StringSelectOption(
                label="Smaller",
                emoji="<:zoomout:972511245112586240>",
                value="smaller"
            ),
            StringSelectOption(
                label="UP",
                emoji="<:uparrow:972510553497014282>",
                value="move_up"
            ),
            StringSelectOption(
                label="DOWN",
                emoji="<:downarrow:972510590847315988>",
                value="move_down"
            ),
            StringSelectOption(
                label="LEFT",
                emoji="<:leftarrow:972504681257500682>",
                value="move_left"
            ),
            StringSelectOption(
                label="RIGHT",
                emoji="<:rightarrow:972510572883087380>",
                value="move_right"
            ),
            StringSelectOption(
                label="Enter MaskCode",
                emoji="<:pen:972506421767847946>",
                value="maskcode"
            ),
            StringSelectOption(
                label="Validate",
                emoji="<:check:972503604592250940>",
                value="validate"
            ),
            custom_id="inpaint_act",
            placeholder="Agrandir ou Rétrécir",
            min_values=1,
            max_values=1,
        )
    )
]

@slash_command(name="inpaint", description="Inpaint a picture using StableDiffusion")
@slash_option(
    name="image_url",
    description="Original image URL to transform (PNG, JPG, GIF)",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="mask_code",
    description="size;x;y:maskcode",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="prompt",
    description="What you want to see",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="negative_prompt",
    description="What you don't want to see",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="denoising",
    description="How similar should it be (0.0 MAX - 1.0 MIN)",
    required=False,
    opt_type=OptionType.NUMBER
)
@slash_option(
    name="mask_blur",
    description="How similar should it be (0.0 MIN - 64 MAX)",
    required=False,
    opt_type=OptionType.NUMBER
)
async def inpaint(ctx: SlashContext, image_url: str, mask_code:str, prompt: str = "", negative_prompt: str = "", denoising: float = 0.5):
    #mask_code = "50;0;0:maskcode"#size;x;y
    maskcode_l = mask_code.replace(":maskcode","").split(";")
    
    try:
        iid, mid = mask.create_image_mask(image_url, int(maskcode_l[1]), int(maskcode_l[2]), int(maskcode_l[0]))
    except Exception as e:
        await ctx.send(str(e)+"\nI can't access to this image, please ensure that you give me a working url next time",ephemeral=True)
        return

    await ctx.send(mask_code+"\n`"+image_url+"`\n[Prompt] "+prompt+"\n[Negatives] "+negative_prompt, components=inpaint_action_menu, ephemeral=True, files=[iid, mid])
    os.remove(iid)
    os.remove(mid)

ask_maskcode = Modal(
        ShortText(label="size;x;y (End with :maskcode)", custom_id="maskcode_text"),
        title="Enter your maskcode",
        custom_id="maskcode_modal",
    )
@listen(Component)
async def on_component(event: Component):
    ctx = event.ctx
    value = str(ctx.values[0])

    mask_code = ctx.message.content.split(":maskcode\n")[0]
    maskcode_l = mask_code.split(";")

    image_url = ctx.message.content.split("`")[1]

    prompt = ctx.message.content.split("[Prompt] ")[1]
    negative_prompt = prompt.split("[Negatives]")[1]
    prompt = prompt.split("[Negatives]")[0]

    if ctx.custom_id == str("inpaint_act"):
        if value == "maskcode":
            await ctx.send_modal(ask_maskcode)
        if value == "bigger":
            maskcode_l[0] = str(int(maskcode_l[0]) + 5)
        if value == "smaller":
            maskcode_l[0] = str(int(maskcode_l[0]) - 5)
        if value == "move_up":
            maskcode_l[2] = str(int(maskcode_l[2]) - 5)
        if value == "move_down":
            maskcode_l[2] = str(int(maskcode_l[2]) + 5)
        if value == "move_left":
            maskcode_l[1] = str(int(maskcode_l[1]) - 5)
        if value == "move_right":
            maskcode_l[1] = str(int(maskcode_l[1]) + 5)
        
        if value == "validate":
            await ctx.send(content=random.choice(messages_attente), ephemeral=True)
            iid, mid = mask.create_image_mask(image_url, int(maskcode_l[1]), int(maskcode_l[2]), int(maskcode_l[0]))
            image = await sd_inpaint(ctx.author,image_url, mid,prompt,negative_prompt)
            await ctx.send(content="\n[Prompt] "+prompt+"\n[Negatives] "+negative_prompt,files=[image])
            os.remove(image)
            os.remove(iid)
            os.remove(mid)
            return
        
        iid, mid = mask.create_image_mask(image_url, int(maskcode_l[1]), int(maskcode_l[2]), int(maskcode_l[0]))

        mask_code = str(";".join(maskcode_l))+":maskcode"
        await ctx.edit_origin(content=mask_code+"\n`"+image_url+"`\n[Prompt] "+prompt+"\n[Negatives] "+negative_prompt,  components=inpaint_action_menu, files=[iid, mid])
        os.remove(iid)
        os.remove(mid)

@modal_callback("maskcode_modal")
async def on_modal_answer(ctx: ModalContext, maskcode_text: str):
    image_url = ctx.message.content.split("`")[1]

    prompt = ctx.message.content.split("[Prompt] ")[1]
    negative_prompt = prompt.split("[Negatives]")[1]
    prompt = prompt.split("[Negatives] ")[0]
    if re.match(r"^[0-9]+;[0-9]+;[0-9]+:maskcode$", maskcode_text) is not None:
        mask_code = maskcode_text.split(":maskcode")[0]
        maskcode_l = mask_code.split(";")
        iid, mid = mask.create_image_mask(image_url, int(maskcode_l[1]), int(maskcode_l[2]), int(maskcode_l[0]))
        await ctx.send(maskcode_text+"\n`"+image_url+"`\n[Prompt] "+prompt+"\n[Negatives] "+negative_prompt, components=inpaint_action_menu, ephemeral=True, files=[iid, mid])
        os.remove(iid)
        os.remove(mid)
    else:
        await ctx.send(maskcode_text+" is an invalid maskcode", ephemeral=True)

@slash_command(name="credit", description="See contributors")
async def credit(ctx: SlashContext):
    embed = Embed(
        title="Credit",
        description="Devs :\n- Frablock\n- Rypoint\n\nPowered by : \n- StableDiffusion (StabilityAI)\n - SD WebUI (AUTOMATIC1111)\n\nThe code is under the [GPLv3 licence](https://www.gnu.org/licenses/gpl-3.0.html)\n\nAll generated image are under the [CC4.0-BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en)\nWhen crediting, please use```Image generated with StableDiffusion by using https://github.com/Frablock/StableDiffusion-DiscordBot. Image under CC4.0-BY-NC-SA - https://creativecommons.org/licenses/by-nc-sa/4.0```",
        color=0xff0000 # Green color
    )
    await ctx.send(embed=embed)

bot.start()