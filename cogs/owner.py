import discord
from discord.ext import commands

from time import sleep

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name = "delete", brief = "Deletes every channel in the server")
    async def deleteCmd(self, ctx):
        print("Deleting channels...")
        guild = ctx.guild
        for category in guild.categories:
            try:
                await category.delete()
            except:
                pass

        for channel in guild.channels:
            try:
                await channel.delete()
            except:
                pass

    @commands.is_owner()
    @commands.command(name = "startup", brief = "creates a bunch of channels")#, give the command the role you want to have the permission to access them")
    async def startupCmd(self, ctx):
        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        for j in range(0, 10):
            try:
                await guild.create_category(name=f"spam {j+1}")
            except Exception as e:
                print(e)
                return
                
            for i in range(1, 51):
                try:
                    channel = await guild.create_text_channel(f"spam-{j+1} - {i}", category=guild.categories[j+2], overwrites=overwrites)
                    print(f"creating channel \"spam-{j+1}-{i}\"")
                    sleep(0.15)
                except Exception as e:
                    print(f"error: {e}\n\nprobably just hit the max channel limit")
                    break


async def setup(bot):
    await bot.add_cog(Owner(bot))
