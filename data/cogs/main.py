import discord
from discord.ext import commands

# наследуем класс commands.Cog, показывая, что этот класс является частью функции бота
class User(commands.Cog):

    def __init__(self, client): # конструктор
        self.client = client

    @commands.Cog.listener() # event
    async def on_ready(self): # выполняется, когда бот готов к работе
        print("bot ready")

    @commands.command(pass_context = True) # command
    async def info(self, ctx): # выполняется при использовании префикса, например !info
        await ctx.send(f"Hello, {ctx.message.author.mention}") # отправляем сообщение пользователю, который активировал команду

    @commands.command(pass_context=True, aliases = ['hugs', 'h']) # command, например !hugs или !h
    async def __hugs(self, ctx, user: discord.Member = None): # команда для обнимашек
        if user is None: # если пользователь не выбрал кого обнимать, то бот обнимает пользователя, отправившего команду
            user = ctx.author
        await ctx.channel.purge(limit = 1)
        await ctx.send(f"hugs {user.mention}")


def setup(client): # загружаем данный класс в бота
    client.add_cog(User(client))