# 檔名：picture.py
# 功能：上傳、發送照片（簡單示範和照片有關的用法）

import discord
from discord.ext import commands
import os
import requests

class Picture(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 上傳照片
    # 使用者輸入 $upload 時會觸發
    @commands.command(help = "Upload a picture.", brief = "Upload a picture.")
    async def upload(self, ctx):
        # 取得照片
        try:
            response = requests.get(ctx.message.attachments[0].url)
        except IndexError:
            return await ctx.send('Image invalid!')
        # 開檔，把照片寫入
        file = open(os.path.join("..", "storage", "sample_image.png"), "wb")
        file.write(response.content)
        file.close()

    # bot 傳送照片
    # 使用者輸入 $show_pic 時會觸發
    @commands.command(help = "Show a picture.", brief = "Show a picture.")
    async def show_pic(self, ctx):
        # 開檔讀取照片
        try:
            with open(os.path.join("..", "storage", "sample_image.png"), "rb") as f:
                picture = discord.File(f) # 把檔案內容轉成 discord 上可以傳送的格式
                await ctx.send(file = picture) # Bot 傳送圖片
        except FileNotFoundError:
            await ctx.send('Saved image not found!')

# 從主程式加入此功能需要用到的函數
def setup(bot):
    bot.add_cog(Picture(bot))
