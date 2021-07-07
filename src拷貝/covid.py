# 檔名：covid.py
# 功能：印出疾管署提供台灣疫情的統計數字

import discord
from discord.ext import commands
# import asyncio
import requests
from bs4 import BeautifulSoup
# import random
from datetime import datetime, timedelta
import csv

# 取得最新的疾管署資料
def get_covid_data():
    # https://data.cdc.gov.tw/dataset/covid19_tw__stats/resource/52eb9a7d-813d-48b1-b462-384a7c84a746
    r = requests.get('https://od.cdc.gov.tw/eic/covid19/covid19_tw_stats.csv')
    r.encoding = 'utf-8'
    if r.status_code == 200:
        data = csv.DictReader(r.text.split('\n'))
    else:
        raise Exception(f'{r.status_code} {r.reason}')

    data = list(data)[0]
    for key, value in data.items():
        data[key] = int(value.replace(',',''))

    return data

class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help = '''
            印出疾管署提供台灣疫情的統計數字
         ''',
        brief = "Print Taiwan's COVID statistics"
    )
    async def covid(self, ctx):
        try:
            covid_data = get_covid_data()
        except Exception as e:
            await ctx.send('Query error: ' + str(e))

        text = []
        for k, v in covid_data.items():
            text.append(f'{k}: {v}人')

        await ctx.send('\n'.join(text))


def setup(bot):
    bot.add_cog(Covid(bot))
