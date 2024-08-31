import discord
from discord.ext import commands, tasks
import asyncio

class ChangeStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.first = ""
        self.second = ""
        self.third = ""
        self.status_task = None

    @tasks.loop(seconds=10)
    async def start_the_status(self):
        if not (self.first and self.second and self.third):
            return
        
        await self.bot.change_presence(activity=discord.Game(name=self.first))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Game(name=self.second))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Game(name=self.third))
        await asyncio.sleep(10)

    @commands.group(name="statusy", invoke_without_command=True)
    async def status_group(self, ctx):
        embed = discord.Embed(
            title="Change the Bot's Status!",
            description=(
                "Change the Bot's Status to make it change every 10 seconds!\n\n"
                "Available Commands:\n"
                f"`{self.bot.prefix}statusy start`: Start the status changing process\n"
                f"`{self.bot.prefix}statusy one <status>`: Set the first status of the bot\n"
                f"`{self.bot.prefix}statusy two <status>`: Set the second status of the bot\n"
                f"`{self.bot.prefix}statusy three <status>`: Set the third status of the bot"
            ),
            color=self.bot.main_color
        )
        await ctx.send(embed=embed)

    @status_group.command(name="start")
    async def statusy_start(self, ctx):
        if not (self.first and self.second and self.third):
            await ctx.send("Please set all 3 statuses first!")
            return
        
        if self.status_task is not None and not self.status_task.done():
            await ctx.send("Status changing is already running.")
            return
        
        self.status_task = self.start_the_status.start()
        await ctx.send("Status changing started! If you experience any problems, run this command again.")

    @status_group.command(name="one")
    async def first_set(self, ctx, *, first):
        if not first:
            await ctx.send("Please provide a status to set!")
            return
        
        self.first = first
        await ctx.send(f"Set `{first}` as the first status!")

    @status_group.command(name="two")
    async def second_set(self, ctx, *, two):
        if not two:
            await ctx.send("Please provide a status to set!")
            return
        
        self.second = two
        await ctx.send(f"Set `{two}` as the second status!")

    @status_group.command(name="three")
    async def third_set(self, ctx, *, three):
        if not three:
            await ctx.send("Please provide a status to set!")
            return
        
        self.third = three
        await ctx.send(f"Set `{three}` as the third status!")

async def setup(bot):
    bot.add_cog(ChangeStatus(bot))
