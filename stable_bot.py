# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 15:20:32 2024

@author: user
"""

from dotenv import dotenv_values

from stable_diffusion import *

from interactions import OptionType, slash_option, slash_command, SlashContext, Embed, SlashCommandChoice
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

import localization as l

import detect_nsfw

waiting_messages = ["waiting_message."+str(i) for i in range(10)]


bot = Client(intents=Intents.DEFAULT)

TOKEN = dotenv_values(".env")["TOKEN"]

bot = interactions.Client(token=TOKEN)

MAX_BATCH_SIZE = str(dotenv_values(".env")["MAX_BATCH_SIZE"])

DEFAULT_IMG_RATIO = dotenv_values(".env")["DEFAULT_IMG_RATIO"]

SQUARE_IMG_SIZE  = str(dotenv_values(".env")["SQUARE_IMG_SIZE"])+"x"+str(dotenv_values(".env")["SQUARE_IMG_SIZE"])
LANDSCAPE_IMG_SIZE  = dotenv_values(".env")["LANDSCAPE_IMG_SIZE"]
PORTRAIT_IMG_SIZE = dotenv_values(".env")["PORTRAIT_IMG_SIZE"]

MAX_WIDTH = int(dotenv_values(".env")["MAX_WIDTH"])
MAX_HEIGHT = int(dotenv_values(".env")["MAX_HEIGHT"])

PROMPT_REQUIRED = int(dotenv_values(".env")["PROMPT_REQUIRED"])

FIXED_SIZE_TXT2IMG = int(dotenv_values(".env")["FIXED_SIZE_TXT2IMG"])

@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@slash_command(name="imagine", description="Generate a picture using StableDiffusion")
@slash_option(
    name="prompt",
    description="What you want to see",
    required=PROMPT_REQUIRED,
    opt_type=OptionType.STRING
)
@slash_option(
    name="negative_prompt",
    description="What you don't want to see",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="size",
    description="Choose a size [10, "+str(MAX_WIDTH)+"]x[10, "+str(MAX_WIDTH)+"]",
    required=False,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name=SQUARE_IMG_SIZE, value=SQUARE_IMG_SIZE),
        SlashCommandChoice(name=LANDSCAPE_IMG_SIZE, value=LANDSCAPE_IMG_SIZE),
        SlashCommandChoice(name=PORTRAIT_IMG_SIZE, value=PORTRAIT_IMG_SIZE)
    ] if FIXED_SIZE_TXT2IMG else []
)
@slash_option(
    name="batch_size",
    description="How many image ? [1-"+MAX_BATCH_SIZE+"]",
    required=False,
    opt_type=OptionType.INTEGER
)
async def generate(ctx: SlashContext, prompt: str = "", negative_prompt: str = "", size: str = "",batch_size: int =1):
    if not 1<=batch_size<=int(MAX_BATCH_SIZE):
        await ctx.send(content=l.get(ctx.locale, "invalid_batch_size", MAX_BATCH_SIZE),ephemeral=True)
        return

    if size=="":
        size = {"SQUARE":SQUARE_IMG_SIZE, "LANDSCAPE":LANDSCAPE_IMG_SIZE, "PORTRAIT":PORTRAIT_IMG_SIZE}.get("DEFAULT_IMG_RATIO", SQUARE_IMG_SIZE)

    size = size.split("x")
    size[0] = int(size[0])
    size[1] = int(size[1])
    if not (10<=size[0]<=MAX_WIDTH and 10<=size[1]<=MAX_HEIGHT):
        await ctx.send(content=l.get(ctx.locale, "invalid_size", MAX_BATCH_SIZE),ephemeral=True)
        return

    await ctx.send(l.get(ctx.locale, random.choice(waiting_messages)), ephemeral=True)

    for i in range(batch_size):
        image = await get_image(ctx.author,prompt,negative_prompt, size)

        is_nsfw = detect_nsfw.detect_nsfw(image)

        if is_nsfw and not ctx.channel.nsfw:
            await ctx.send(l.get(ctx.locale, "nsfw_detected"), ephemeral=True)
            negative_prompt += "NSFW, nude, explicit, sexual, nudity, explicit sexual acts, sexual organs, adult content, pornography, sexual fantasies, adult material, erotic, sexual imagery, adult themes, explicit adult content"
        else:

            embed = Embed(
                title= l.get(ctx.locale, "processing_complete") if batch_size==1 else l.get(ctx.locale, "processing_complete_batch",i+1, batch_size),
                description= l.get(ctx.locale, "description", prompt, negative_prompt) if negative_prompt!="" else l.get(ctx.locale, "description_neg", prompt),
                footer=l.get(ctx.locale, "footer")
            )

            # Send the response after processing is complete
            await ctx.send(embed=embed, files=[image])
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
@slash_option(
    name="batch_size",
    description="How many image ? [1-"+MAX_BATCH_SIZE+"]",
    required=False,
    opt_type=OptionType.INTEGER
)
async def transform(ctx: SlashContext, image_url: str, prompt: str = "", negative_prompt: str = "", denoising: float = 0.5, batch_size=1):
    if not 1<=batch_size<=int(MAX_BATCH_SIZE):
        await ctx.send(content=l.get(ctx.locale, "invalid_batch_size", MAX_BATCH_SIZE),ephemeral=True)
        return

    await ctx.send(random.choice(waiting_messages), ephemeral=True)

    if not 0<=denoising<=1:
        await ctx.send("Incorrect denoising",ephemeral=True)
        return
    
    for i in range(batch_size):
        try:
            image = await img2img(ctx.author,image_url,prompt,negative_prompt, denoising)
        except Exception as e:
            await ctx.send(l.get(ctx.locale, "invalid_image"),ephemeral=True)
            return

        embed = Embed(
            title= l.get(ctx.locale, "processing_complete") if batch_size==1 else l.get(ctx.locale, "processing_complete_batch",i+1, batch_size),
            description= l.get(ctx.locale, "description", prompt, negative_prompt) if negative_prompt!="" else l.get(ctx.locale, "description_neg", prompt),
            footer=l.get(ctx.locale, "footer"),
            images=[image_url]
        )
        # Send the response after processing is complete
        await ctx.send(embed=embed, files=[image])
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
        await ctx.send(l.get(ctx.locale, "invalid_image"),ephemeral=True)
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
            await ctx.send(content=random.choice(waiting_messages), ephemeral=True)
            iid, mid = mask.create_image_mask(image_url, int(maskcode_l[1]), int(maskcode_l[2]), int(maskcode_l[0]))
            image = await sd_inpaint(ctx.author,image_url, mid,prompt,negative_prompt)

            embed = Embed(
                title= l.get(ctx.locale, "processing_complete") if batch_size==1 else l.get(ctx.locale, "processing_complete_batch",i+1, batch_size),
                description= l.get(ctx.locale, "description", prompt, negative_prompt) if negative_prompt!="" else l.get(ctx.locale, "description_neg", prompt),
                footer=l.get(ctx.locale, "footer"),
                images=[image_url]
            )

            await ctx.send(embed=embed,files=[image])
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
        await ctx.send(l.get(ctx.locale,"invalid_maskcode",maskcode_text), ephemeral=True)

@slash_command(name="credit", description="See contributors")
async def credit(ctx: SlashContext):
    embed = Embed(
        title="Credit",
        description=l.get(ctx.locale,"credit"),
        color=0xff0000 # RED color
    )
    await ctx.send(embed=embed)

bot.start()