from dotenv import load_dotenv
import os

load_dotenv()
import json
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

DATA_FILE = "exchange_data.json"

# Initialize empty data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"clients": {}, "staff": {}}, f)

def update_exchange(user_id, amount, is_staff=False):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    category = "staff" if is_staff else "clients"
    user_data = data[category].get(str(user_id), {"amount": 0.0, "deals": 0})

    user_data["amount"] += amount
    user_data["deals"] += 1

    data[category][str(user_id)] = user_data

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_summary(user_id, is_staff=False):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    category = "staff" if is_staff else "clients"
    user_data = data[category].get(str(user_id), {"amount": 0.0, "deals": 0})
    return user_data

# 📿 CALCULATOR
@bot.command(name='calc')
async def calculate(ctx, *, expression: str):
    try:
        result = eval(expression)
        embed = discord.Embed(
            title=" CALCULATOR",
            color=discord.Color.green()
        )
        embed.set_author(name="COSMIC EXCHANGE", icon_url="https://cdn.discordapp.com/attachments/1402241162177282098/1402270889713864815/ChatGPT_Image_Aug_5_2025_03_37_25_PM.png?ex=6895f109&is=68949f89&hm=f8b6fc715f03add64e7dc55e7066f7e04dd2f3cadb6b43f0a0ccf272ef6bce68&")
        embed.add_field(name="**Expression**", value=f"```{expression}```", inline=False)
        embed.add_field(name="**Result**", value=f"```{result}```", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error: `{str(e)}`")

# 📦 CLIENT SUMMARY
@bot.command(name='e')
async def exchange_summary(ctx):
    summary = get_summary(ctx.author.id, is_staff=False)
    embed = discord.Embed(
        title="📦 Exchange Summary (Client)",
        color=discord.Color.blue()
    )
    embed.set_author(name="COSMIC EXCHANGE", icon_url="https://cdn.discordapp.com/attachments/1402241162177282098/1402270889713864815/ChatGPT_Image_Aug_5_2025_03_37_25_PM.png?ex=6895")
    embed.add_field(name="👤 User", value=ctx.author.mention, inline=True)
    embed.add_field(name="💸 Total Exchanged", value=f"${summary['amount']:.2f}", inline=True)
    embed.add_field(name="📊 Total Deals", value=str(summary['deals']), inline=True)
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# 🤝 STAFF SUMMARY
@bot.command(name='d')
async def deal_summary(ctx):
    summary = get_summary(ctx.author.id, is_staff=True)
    embed = discord.Embed(
        title="🤝 Deal Summary (Staff)",
        color=discord.Color.blue()
    )
    embed.set_author(name="COSMIC EXCHANGE", icon_url="https://cdn.discordapp.com/attachments/1402241162177282098/1402270889713864815/ChatGPT_Image_Aug_5_2025_03_37_25_PM.png?ex=6895")
    embed.add_field(name="🧑‍💼 Staff", value=ctx.author.mention, inline=True)
    embed.add_field(name="💸 Total Amount Dealt", value=f"${summary['amount']:.2f}", inline=True)
    embed.add_field(name="📊 Total Deals", value=str(summary['deals']), inline=True)
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# ✅ RECORD DEAL MANUALLY
@bot.command(name='recorddeal')
async def record_deal(ctx, client: discord.Member, amount: float):
    staff_id = ctx.author.id
    client_id = client.id

    update_exchange(client_id, amount, is_staff=False)
    update_exchange(staff_id, amount, is_staff=True)

    await ctx.send(
        f"✅ Recorded deal of `${amount}` between client {client.mention} and staff {ctx.author.mention}."
    )


bot.run(os.getenv("DISCORD_BOT_TOKEN"))

