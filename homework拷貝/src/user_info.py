import discord
from discord.ext import commands


class User_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
    @commands.command(
        help = '''
        Get the delay value.
        ''', # 輸入 $help add 時顯示
        brief = "Get the delay value." # 輸入 $help 時顯示
    )
    async def ping(self, ctx):
        await ctx.send(f':hourglass:{round(self.bot.latency*1000)} (ms)')
    @commands.command(
        help = '''
        Get the user's ID.
        ''', # 輸入 $help add 時顯示
        brief = "Get the user's ID." # 輸入 $help 時顯示
    )
    async def myid(selF, ctx):
        await ctx.send(ctx.message.author.id)
def setup(bot):
    bot.add_cog(User_info(bot))