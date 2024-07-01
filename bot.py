import os
import data.Config.config as conf
import discord
from discord.ext import commands

settings = conf.configs(section="bot", filename="config.ini") # получение настроек для бота

# задаём префикс для бота и присваиваем полученного бота для дальнейших манипуляций
client = commands.Bot(command_prefix = settings['prefix'])
client.remove_command("help")

@client.command()
async def load(ctx, extension): # загружаем все файлы/классы в папке data/cogs
    client.load_extension(f"data.cogs.{extension}")
    await ctx.send("Cogs is loaded...")


@client.command()
async def unload(ctx, extension): # выгружаем все файлы/классы в папке data/cogs
    client.unload_extension(f"data.cogs.{extension}")
    await ctx.send("Cogs is unloaded...")

@client.command()
async def reload(ctx, extension): # заново загружаем все файлы/классы в папке data/cogs
    client.unload_extension(f"data.cogs.{extension}")
    client.load_extension(f"data.cogs.{extension}")
    await ctx.send("Cogs is loaded...")


for filename in os.listdir("./data/cogs"): # чтение всех файлов типа .py для их добавления в функции бота
    if filename.endswith(".py"):
        client.load_extension(f"data.cogs.{filename[:-3]}")


client.run(settings['token']) # запускаем бота