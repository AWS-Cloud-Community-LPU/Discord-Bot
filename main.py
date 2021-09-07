import discord
from discord.ext import commands
import random
import os
import wikipedia
import asyncio
import aiohttp
import string
import secrets
import requests
from bs4 import BeautifulSoup
from keep_alive import keep_alive
client = commands.Bot(command_prefix='.')

client.remove_command('help')

# Things to be added
#I'm adding a random meme from reddit


@client.command(brief="For Funny Memes")
async def meme(ctx):
    embed = discord.Embed(title="Meme", description="Meme")
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
           res = await r.json()
           embed.set_image(url=res['data']['children'] [random.randint(0, 30)]['data']['url'])
           await ctx.send(embed=embed)

@client.command()
async def av(ctx, *, member: discord.Member): # set the member object to None
    show_avatar = discord.Embed(
        title=f"{member}",
        description="Avatar",
        color = discord.Color.dark_blue()
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)


keep_alive()
client.run('API_TOKEN')
