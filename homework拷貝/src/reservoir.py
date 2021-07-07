import requests
from bs4 import BeautifulSoup
import json
import discord
from discord.ext import commands
url = 'https://www.taiwanstat.com/waters/latest'
html = requests.get(url).text
data = json.loads(html)

class reservoir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help = '''Get each reservoir's percentage
                                ex.$res_per'''
                    , brief = "Get each reservoir's percentage")
    async def res_per(self, ctx):
        for i in range(21):
            name = list(data[0].values())[i]["name"]
            percentage = list(data[0].values())[i]["percentage"]
            await ctx.send(str(name)+":"+str(percentage)+"%")
    
    @commands.command(help = '''Get each reservoir's volumn
                                ex.$res_vol'''
                    , brief = "Get each reservoir's volumn")
    async def res_vol(self, ctx):
        for i in range(21):
            name = list(data[0].values())[i]["name"]
            volumn = list(data[0].values())[i]["volumn"]
            await ctx.send(str(name)+":"+str(volumn)+"(萬立方公尺)")
    @commands.command(help = "Get each reservoir\'s effective storage capacity"
                    , brief = "Get each reservoir's effective storage capacity")
    async def res_ava(self, ctx):
        for i in range(21):
            name = list(data[0].values())[i]["name"]
            baseAvailable = list(data[0].values())[i]["baseAvailable"]
            await ctx.send(str(name)+":"+str(baseAvailable)+"(萬立方公尺)")
def setup(bot):
    bot.add_cog(reservoir(bot))
