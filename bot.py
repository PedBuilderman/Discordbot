import asyncio
import os
import threading
from flask import Flask
import discord
from discord.ext import commands

# --- Web Server to allow Render's Free Web Service ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Run web server in background
threading.Thread(target=run_web_server, daemon=True).start()

# --- Discord Bot Code ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
active_timers = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Triggers on "gg", "Gg", "gG", "GG"
    if message.content.strip().lower() == "gg":
        user_id = message.author.id

        if user_id in active_timers:
            active_timers[user_id].cancel()

        await message.channel.send(
            f"⏳ {message.author.mention}, 20-minute timer started!"
        )

        async def timer_task():
            try:
                await asyncio.sleep(20 * 60)  # 20 minutes
                await message.channel.send(
                    f"⏰ {message.author.mention}, 20 minutes are up! You can claim/roll your cards again!"
                )
            except asyncio.CancelledError:
                pass
            finally:
                active_timers.pop(user_id, None)

        active_timers[user_id] = asyncio.create_task(timer_task())

    await bot.process_commands(message)

# --- Run Bot ---
# Make sure to set DISCORD_TOKEN in your Render Environment Variables
bot.run("MTU1Mzk5NDg0NjA5ODgxNzIwOA.G-zodC.aqoq2qy-vQEKorECZJsBz7ApR9cN8SKcaz4P1w")
