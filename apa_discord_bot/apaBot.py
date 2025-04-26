from dotenv import load_dotenv, dotenv_values
import os
import discord
from discord.ext import commands
from update import main
from screenshot import take_screenshot

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("APA Bot is now ready...")

@bot.command(name='update')
async def update(ctx):
    ud = main()
    ss = take_screenshot()
    await ctx.send("Doing an APA scrape. This will take awhile... I'll let you know when I'm done.")
    await ud
    await ctx.send("Generating snapshots of updated APA scrape...")
    await ss
    await ctx.send("Done! Go ahead and use the '!matchup' command to post screenshots in a channel.")
    
@bot.command(name='matchup')
async def matchup(ctx, channel_id: int):
    ss8 = os.path.abspath('8ball_ss.png')
    ss9 = os.path.abspath('9ball_ss.png')
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("That channel ID doesn't exist, try again...")
        return

    await channel.send(file=discord.File(ss8))
    await channel.send(file=discord.File(ss9))

@matchup.error
async def matchup_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide valid channel ID...")

if __name__ == "__main__":    
    bot.run(os.getenv("bot_token"))