import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from zoneinfo import ZoneInfo

# =========================
# Discord Token (Render環境變數)
# =========================
TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# Discord 頻道 ID
# =========================
CHANNEL_ID = 1510167619431563355

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

clock_message = None

timezones = {
    "🇹🇼 台灣": "Asia/Taipei",
    "🇨🇳 大陸": "Asia/Shanghai",
    "🇯🇵 日本": "Asia/Tokyo",
    "🇨🇦 溫哥華": "America/Vancouver",
    "🇦🇹 維也納": "Europe/Vienna",
    "🇩🇰 哥本哈根": "Europe/Copenhagen",
    "🇩🇪 慕尼黑": "Europe/Berlin"
}

def make_clock_text():

    text = "🌍 **世界時鐘**\n\n"

    for city, zone in timezones.items():

        now = datetime.now(
            ZoneInfo(zone)
        )

        text += (
            f"{city}："
            f"`{now.strftime('%Y/%m/%d %H:%M:%S')}`\n"
        )

    text += "\n⏰ 每分鐘自動更新"

    return text


@bot.event
async def on_ready():

    print(f"已登入：{bot.user}")

    if not update_clock.is_running():
        update_clock.start()


@tasks.loop(minutes=1)
async def update_clock():

    global clock_message

    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print(f"找不到頻道：{CHANNEL_ID}")
        return

    try:

        if clock_message is None:

            clock_message = await channel.send(
                make_clock_text()
            )

            print("世界時鐘訊息已建立")

        else:

            await clock_message.edit(
                content=make_clock_text()
            )

    except Exception as e:

        print(f"錯誤：{e}")


bot.run(TOKEN)