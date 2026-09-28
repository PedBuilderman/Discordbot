import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Required to read "gg" in chat

bot = commands.Bot(command_prefix="!", intents=intents)

# Track active timers per channel/user so multiple triggers don't stack
active_timers = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore messages sent by bots
    if message.author.bot:
        return

    # Check if the message is "gg" (case-insensitive: "gg", "Gg", "gG", "GG")
    if message.content.strip().lower() == "gg":
        user_id = message.author.id

        # Cancel existing countdown for this user if they drop another "gg"
        if user_id in active_timers:
            active_timers[user_id].cancel()

        await message.channel.send(
            f"⏳ {message.author.mention}, timer set! I'll remind you in **20 minutes** when your card claim is ready."
        )

        # Create background timer task
        async def timer_task():
            try:
                await asyncio.sleep(20 * 60)  # Wait 20 minutes (1200 seconds)
                await message.channel.send(
                    f"⏰ {message.author.mention}, 20 minutes are up! You can claim/roll your cards again!"
                )
            except asyncio.CancelledError:
                pass  # Timer was reset by a new "gg"
            finally:
                active_timers.pop(user_id, None)

        active_timers[user_id] = asyncio.create_task(timer_task())

    # Ensure other commands still process if you add any later
    await bot.process_commands(message)

# Replace with your actual Bot Token from Discord Developer Portal
bot.run("MTU1Mzk5NDg0NjA5ODgxNzIwOA.G-zodC.aqoq2qy-vQEKorECZJsBz7ApR9cN8SKcaz4P1w")
