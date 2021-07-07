# 檔名：currency.py
# 功能：從銀行(玉山銀行網頁)印出貨幣和匯率的相關資訊

import discord
from discord.ext import commands
# import asyncio
import requests
from bs4 import BeautifulSoup
# import random
from datetime import datetime, timedelta
import re

class Rates:
    def __init__(self):
        self.dict = {}
        self.names = {}
        self.upd_time = None
        self.upd_time_text = None
        self.update()

    def update(self):
        def getTime(s):
            time_text = s.find(id='LbQuoteTime').text # 更新時間
            d = time_text.replace('日 ', 'T')
            for x in "年月":
                d = d.replace(x, '-')

            return (time_text, datetime.fromisoformat(d))

        r = requests.get('https://www.esunbank.com.tw/bank/personal/deposit/rate/forex/foreign-exchange-rates')
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
        else:
            raise Exception(f'{r.status_code} {r.reason}')

        self.upd_time_text, self.upd_time = getTime(soup)
        s = (soup.find(id='inteTable1').find_all('td', {'data-name': '外幣類型'}))

        self.dict = {}
        for c in s:
            curr_text = c.a.text.strip()
            # print(c.a.text.strip())
            curr = re.search('\((.*)\)', curr_text)[1]
            p_tags = c.parent.find_all('td', {'data-name': True})
            pdata = {}
            for p in p_tags[1:]:
                if p.text:
                    pdata[p.attrs['data-name']] = float(p.text)

            # print(curr)
            self.dict[curr] = pdata
            self.names[curr] = curr_text

        print('Updated currency data.')

    def check(self):
        if datetime.now() - self.upd_time > timedelta(minutes=3):
            self.update()

    def format_one(self, cur):
        self.check()
        curr_data = '\n'.join(f'{k}: {v}' for k, v in self.dict[cur].items())
        return f'{self.names[cur]}:\n{curr_data}'

    def get_dict(self):
        self.check()
        return self.dict

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rate = Rates()

    @commands.command(
        help = '''
        從銀行(玉山銀行網頁)印出所選貨幣的匯率資訊
        可以使用 $curr_list 來獲取貨幣代碼的清單
         ''',
        brief = "Print rate for the selected currency"
    )
    async def rates(self, ctx, cur):
        try:
            text = self.rate.format_one(cur)
        except:
            return await ctx.send("Invalid currency! Valid: " + ', '.join(self.rate.dict.keys()))
        await ctx.send(f'更新時間: {self.rate.upd_time_text}')
        await ctx.send(text)

    @commands.command(
        help = "從銀行(玉山銀行網頁)印出全部貨幣的匯率資訊",
        brief = "List rates of all currencies"
    )
    async def all_rates(self, ctx):
        cdict = self.rate.get_dict()
        for k in cdict.keys():
            await ctx.send(self.rate.format_one(k))

    @commands.command(
        help = "印出銀行提供資料的貨幣",
        brief = "List available currencies"
    )
    async def curr_list(self, ctx):
        await ctx.send("Valid currencies: " + ', '.join(self.rate.names.values()))


def setup(bot):
    bot.add_cog(Currency(bot))
