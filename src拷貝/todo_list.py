# 檔名：todo_list.py
# 功能：TODO list (新增、刪除、顯示)
# TODO：刪除、顯示、排序、清空、儲存記錄至檔案 (HINT: file I/O, pickle)

import discord
from discord.ext import commands
import re
import os

# 一項 Todo 的 class
class Todo:
    # 初始化
    def __init__(self, date, label, item):
        # 判斷是否為合法的日期 (不是很完整的判斷)
        d = re.compile("[0-9]{1,2}/[0-9]{1,2}")
        assert d.match(date)
        self.date = date
        self.label = label
        self.item = item

    # 小於 < (定義兩個 Todo 之間的「小於」，sort 時會用到)
    def __lt__(self, other):
        return self.date<=other.date
        pass
        #################################################################
        # TODO: 實作小於判斷 (__lt__)
        # 分類: 作業 (5 pts)
        # HINT: 參考下方 __eq__
        #################################################################

    # 等於 = (判斷兩個 Todo 是否相等)
    def __eq__(self, other):
        return self.date==other.date and self.label==other.label and self.item==other.item
    # 回傳一個代表這個 Todo 的 string
    def __repr__(self):
        return f"{self.date} {self.label} {self.item}"

# Todo list 相關 commands
class Todo_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 儲存 TODO list
        self.todo_list = []

    # $add date label item
    @commands.command(
        help = '''
        Add TODO.
        For example:
        $add 06/24 Sprout Discord Bot HW
        ''', # 輸入 $help add 時顯示
        brief = "Add TODO." # 輸入 $help 時顯示
    )
    async def add(self, ctx, date, label, *, item):
        try:
            # 依照輸入建立一個 Todo object
            t = Todo(date, label, item)
        except Exception as e:
            # 建立失敗
            print(e)
            await ctx.send("Invalid input ><")
            return
        # 把 Todo 加進 list
        self.todo_list.append(t)
        # 按照日期排序，若實作了 Todo 的 __lt__ 則可以直接用 sort() 排序
        self.todo_list.sort()

        # 印出加入成功的訊息
        await ctx.send('"{}" added to TODO list'.format(item))

    # $done date label item
    @commands.command(
        help = '''
        Done TODO.
        For example:
        $done 6/24 Sprout Discord Bot HW
        ''', # 輸入 $help add 時顯示
        brief = "Done TODO." # 輸入 $help 時顯示
    )

    async def done(self, ctx, date, label, *, item): # * 代表 label 後面所有的字都會放到 item 內
        t = Todo(date, label, item)
        if t in self.todo_list:
            self.todo_list.remove(t)
            await ctx.send('"{}" Done!'.format(item))

        pass
        #################################################################
        # TODO: 實作刪除一項 Todo
        # 分類: 作業 (5 pts)
        # HINT: 參考上方 add，可以直接用 in 判斷一個 Todo 是否在 todo_list 中 (因為有實作 __eq__)
        #################################################################

    # $show [label]
    @commands.command(
        help = '''
        Show all TODO with the label if specified sorted by date.
        For example:
        $show Sprout
        $show
        ''',
        brief = "Show all TODO with the label if specified sorted by date." # 輸入 $help 時顯示
    )
    
    async def show(self, ctx, label=None):
        for i in self.todo_list:
            await ctx.send(i)
        pass
        #################################################################
        # TODO: 實作顯示 Todo，若有輸入 label 則顯示符合該 label 的 Todo，顯示時依日期排序
        # 分類: 作業 (5 pts)
        # HINT: 遍歷 todo_list
        #################################################################

    # $clear
    @commands.command(help = "Clear TODO list.", brief = "Clear TODO list.")
    async def clear(self, ctx):
        self.todo_list=[]
        await ctx.send("Cleared!")
        pass
        #################################################################
        # TODO: 實作清空 TODO list
        # 分類: 作業 (5 pts)
        #################################################################

def setup(bot):
    bot.add_cog(Todo_list(bot))
