import asyncio
import os
import typing
import discord
from pathlib import Path
from discord.ext import commands

# наследуем класс commands.Cog, показывая, что этот класс является частью функции бота
# не закончено
class History(commands.Cog):

    def __init__(self, client):
        self.client = client
        HERE = Path(__file__).parent.resolve()
        CONFIG_PATH = HERE / "../files"
        self.txt_filex = CONFIG_PATH

    # простой класс для записи из файла в чат дискорда
    @commands.command(pass_context = True, aliases = ['write', 'w', 'wr'])  # command, например !write, или !w, или !wr
    async def __write(self, ctx, what: str = None, who: typing.Union[discord.Member, discord.User, str] = None, which: str = None, where: typing.Union[int, str] = None):
        # из выше: "what: str = None" - что делать, принимает только строку, по умолчанию ничего
        # из выше: "who: typing.Union[discord.Member, discord.User, str] = None" - с кем делать, принимает роль, пользователя или строку, по умолчание ничего
        # из выше: "which: str = None" - выбирается файл, который будет читаться ботом и писать в дискорд, по умолчание ничего
        # из выше: "where: typing.Union[int, str] = None" - выбирается канал, в котором будет писать бот, по умолчание ничего

        # думаю следующее будет понятно, т.к. написано приблизительно к чтению обычной книги
        if what is None:
            await ctx.send("I do not know what to do")
            return

        if who is None:
            await ctx.send("who should I {0}?".format(what))
            return

        if what == "history":
            answer: str = ""
            if who == 'me':
                who = ctx.message.author
                answer += f"I'll write {who.mention}"
            elif type(who) is discord.Member:
                answer += f"I'll write {who.mention}"
            else:
                answer += f"I don't know"

            if which is None:
                for d, dirs, files in os.walk(f"data/files"):
                    file = ""
                    for f in files:
                        file += f[:-4] + '\n'
                await ctx.send(f"there are following \n{file}")
                return
            elif os.path.isfile(f"{self.txt_filex / which}.txt"): # если файл формата txt существует
                which += ".txt" # модифицирует переменную, добавляя строку, например, было "name" стало "name.txt"
            else:
                await ctx.send(f"I'm sorry, I don't know this {which}")
                for d, dirs, files in os.walk(f"data/files"): # получение списка названия всех файлов в папке data/files
                    file = ""
                    for f in files:
                        file += f[:-4] + '\n'
                await ctx.send(f"there are following \n{file}")
                return

            channels = None
            if where is None:
                answer += f" in dms"
            elif type(where) is str:
                channels = self.client.get_channel(int(where[2:-1]))
                answer += f" in {where}"
            else:
                answer += f" in {where}"


            await ctx.send(answer)
            if channels is not None:
                await channels.send(f"{who.mention} come here, I'll tell you a story")
                await asyncio.sleep(3)
                await channels.send(f"I start")
                await asyncio.sleep(3)
                dictionary:dict = self.starter(which)

                for key in dictionary:
                    # из массива бота записывает в чат содержимое строки, а затем останавливается на определённое время
                    # остановить невозможно, пока что, не создан метод остановки
                    await channels.send(dictionary[key][0])
                    await asyncio.sleep(int(dictionary[key][1]))
            else:
                pass
        else:
            await ctx.send("I know only story")

    @commands.command(pass_context=True, aliases=['read', 'r'])
    async def __read(self, ctx):
        # сохраняет вкладываемый файл
        try:
            filename:str = ""
            for attach in ctx.message.attachments: # смотрит содержимое сообщения пользователя
                if ".txt" not in attach.filename: # если в содержимом нет файла формата txt
                    filename += attach.filename + ","
                    continue # переходит в начало цикла, игнорируя ниже
                if os.path.isfile(f"{self.txt_filex / attach.filename}"): # проверяет, существует похожий файл в /data/files
                    await ctx.send(f"I already know this file {attach.filename}, you can update it with another command (not created)")
                else:
                    await attach.save(f"{self.txt_filex / attach.filename}") # сохраняет файл в data/files
            if "," in filename:
                await ctx.send(f"the following files have not been examined by me: {filename} I can only examine files with .txt format")
        except Exception as e:
            print(e)

    @commands.command(pass_context=True, aliases=['delete', 'del', 'uninstall'])
    async def __deleter(self, ctx, filenames:str = None):
        # удаляет файл
        if filenames is None:
            await ctx.send(f"please tell me the name of the story so I can delete it")
            return
        else:
            if os.path.isfile(f"{self.txt_filex / filenames}.txt"): # проверяет, существует ли файл в data/files
                os.remove(f"{self.txt_filex / filenames}.txt") # удаляет файл
            await ctx.send(f"this story {filenames} has been deleted")

    def starter(self, filenames):
        # метод, который читает файл и записывает в массив
        dictionary: dict = {}
        if os.path.isfile(f"{self.txt_filex / filenames}"):
            file1 = open(f"{self.txt_filex / filenames}","r")
            i = 0
            while True:
                line = file1.readline()
                if not line:
                    break
                dictionary[i] = line.split("@")
                i += 1
            file1.close()
        return dictionary


def setup(client): # загружаем данный класс в бота
    client.add_cog(History(client))