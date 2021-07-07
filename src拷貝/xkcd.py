# 檔名：picture.py
# 功能：上傳、發送照片（簡單示範和照片有關的用法）

import discord
from discord.ext import commands
import os
import requests as re
from bs4 import BeautifulSoup
from attr import attrs

s = 'https://xkcd.com/'
m = 2471
n_max = 0
while True:
    m+=1
    r = str(re.get(s+str(m)))
    if '200' in r:
        n_max = m
    else:
        n_max = m-1
        break
class xkcd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 上傳照片
    # 使用者輸入  $xkcd_num 時會觸發
    @commands.command(help = '''Download the comic you want. 
                                ex.xkcd_num 1'''
                    , brief = "Download the comic you want.")
    async def xkcd_num(self, ctx,num):
        # 取得照片
        try:
            response = re.get('https://xkcd.com/'+str(num))
            soup = BeautifulSoup(response.text,"html.parser")
            img = soup.find_all('img')[2].attrs['src']
        except IndexError:
            return await ctx.send('Image invalid!')
        # 開檔，把照片寫入
        res = re.get('https:'+str(img))
        file = open(os.path.join("..", "storage", str(num)+".png"), "wb")
        file.write(res.content)
        file.close()
        await ctx.send('Ok')

    # bot 傳送照片
    # 使用者輸入 $xkcd1_show 時會觸發
    @commands.command(help = '''Show the comic.
                                ex.xkcd_show 1''', brief = "Show the comic.")
    async def xkcd_show(self, ctx, num):
        # 開檔讀取照片
        try:
            with open(os.path.join("..", "storage", str(num)+".png"), "rb") as f:
                picture = discord.File(f) # 把檔案內容轉成 discord 上可以傳送的格式
                await ctx.send(file = picture) # Bot 傳送圖片
        except FileNotFoundError:
            await ctx.send('Saved image not found!')
    @commands.command(help = '''Show the amount of the comic
                                ex.xkcd_amo'''
                    , brief = "The amount of the comic")
    async def xkcd_amo(self, ctx):
        await ctx.send(n_max)
        

# 從主程式加入此功能需要用到的函數
def setup(bot):
    bot.add_cog(xkcd(bot))
