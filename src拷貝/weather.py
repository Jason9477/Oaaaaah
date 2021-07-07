# 檔名：weather.py
# 功能：印出中央氣象局的衛星雲圖

import discord
from discord.ext import commands
# import asyncio
import requests
from bs4 import BeautifulSoup
# import random
from datetime import datetime, timedelta
import io

# 輸入時間，取得 24hr 內的衛星雲圖
# https://www.cwb.gov.tw/V8/C/W/OBS_Sat.html
def get_chart(H=None, M=None):
    now = datetime.now()

    if H is None and M is None:
        r = requests.get(f'https://www.cwb.gov.tw//Data/satellite/LCC_IR1_CR_2750/LCC_IR1_CR_2750.jpg')
        if r.status_code == 200:
            return r.content
        else:
            raise Exception(f'{r.status_code} {r.reason}')
    elif 0 <= int(H) <= 23 and 0 <= int(M) <= 59:
        H, M = int(H), int(M)
        if H*60+M > now.hour*60 + now.minute:
            dt = now - timedelta(days=1)
        else:
            dt = now

        # .zfill(x): 在字串左邊補 0 直到長度為 x
        Y, m, d = dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2)
        # 氣象局只接受以每 10 分鐘整為單位
        H, M = str(H).zfill(2), str(M//10*10).zfill(2)

        r = requests.get(f'https://www.cwb.gov.tw/Data/satellite/LCC_IR1_CR_2750/LCC_IR1_CR_2750-{Y}-{m}-{d}-{H}-{M}.jpg')
        if r.status_code == 200:
            return r.content
        else:
            raise Exception(f'{r.status_code} {r.reason}')
    else:
        raise ValueError('輸入時間錯誤')

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help = '''
            印出中央氣象局的衛星雲圖
            可以用 H 和 M 指定過去24小時內的時間，預設是最新一筆。
         ''',
        brief = "Print satellite cloud chart"
    )
    async def weather(self, ctx, H=None, M=None):
        try:
            chart = io.BytesIO(get_chart(H, M))
            chart = discord.File(chart, filename='chart.png')
            await ctx.send(file = chart)
        except Exception as e:
            await ctx.send('Error: ' + str(e))

def setup(bot):
    bot.add_cog(Weather(bot))
    