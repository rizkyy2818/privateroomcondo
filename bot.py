import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("❌ Token Discord tidak ditemukan! Set DISCORD_TOKEN di environment variables.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} aktif dan siap digunakan!")

@bot.command()
@commands.has_permissions(administrator=True)
async def dmall(ctx, *, message):
    status_msg = await ctx.send(f"🔄 Mengirim DM ke {len(ctx.guild.members)} member...")
    success_count = 0
    fail_count = 0
    for member in ctx.guild.members:
        if member.bot:
            continue
        try:
            await member.send(message)
            success_count += 1
            await asyncio.sleep(0.5)
        except:
            fail_count += 1
    await status_msg.edit(
        content=f"✅ **DM Massal Selesai!**\n"
                f"📤 Berhasil: {success_count}\n📤 Gagal: {fail_count}"
    )

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latensi: {round(bot.latency * 1000)}ms")

@dmall.error
async def dmall_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Kamu butuh izin **Administrator**!")
    else:
        await ctx.send(f"⚠️ Error: {error}")

# ===== IMPORTANT: KEEP BOT ALIVE =====
import keep_alive
keep_alive.run()

bot.run(TOKEN)
