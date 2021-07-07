# 檔名：guess.py
# 功能：猜數字

#################################################################
# TODO: 實作猜數字
# 分類: 作業 (10 pts)
# HINT: 認真上課
#################################################################
import discord
from discord.ext import commands
import random

class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guess(self, ctx):
        await ctx.send("Guess a 4-digit number that doesn't contain 0")
        ans = "".join(random.sample("123456789", 4))
        print(ans)

        def is_valid(m):
            return m.author == ctx.author

        for _ in range(30):
            guess = await self.bot.wait_for('message', check = is_valid, timeout=300.0)
            if guess.content == "quit":
                await ctx.send(f"The ans is {ans}")
                return
            a = sum([1 for i in range(4) if guess.content[i] == ans[i]])
            b = sum([1 for i in range(4) if guess.content[i] in ans])-a
            if guess.content == ans:
                await ctx.send("Correct!")
                return
            else:
                await ctx.send(f"{a}A{b}B")
        await ctx.send("Guess too many times!")

def setup(bot):
    bot.add_cog(Guess(bot))