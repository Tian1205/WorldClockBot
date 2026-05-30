import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands, tasks
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1510167619431563355
PORT = int(os.getenv("PORT", 10000))

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"WorldClockBot is running")

def run_web_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthCheckHandler)
    server.serve_forever()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

clock_message = None

weekdays = {
    0: "星期一",
    1: "星期二",
    2: "星期三",
    3: "星期四",
    4: "星期五",
    5: "星期六",
    6: "星期日"
}

def make_clock_text():
    taipei = datetime.now(ZoneInfo("Asia/Taipei"))
    tokyo = datetime.now(ZoneInfo("Asia/Tokyo"))
    vancouver = datetime.now(ZoneInfo("America/Vancouver"))
    europe = datetime.now(ZoneInfo("Europe/Vienna"))

    text = (
        "🌍 **世界時鐘**\n\n"

        f"🇹🇼 台灣 / 🇨🇳 大陸：\n"
        f"`{taipei.strftime('%Y/%m/%d %H:%M:%S')} {weekdays[taipei.weekday()]}`\n\n"

        f"🇯🇵 日本：\n"
        f"`{tokyo.strftime('%Y/%m/%d %H:%M:%S')} {weekdays[tokyo.weekday()]}`\n\n"

        f"🇨🇦 溫哥華：\n"
        f"`{vancouver.strftime('%Y/%m/%d %H:%M:%S')} {weekdays[vancouver.weekday()]}`\n\n"

        f"🇦🇹 維也納 / 🇩🇰 哥本哈根 / 🇩🇪 慕尼黑：\n"
        f"`{europe.strftime('%Y/%m/%d %H:%M:%S')} {weekdays[europe.weekday()]}`\n"

        "\n⏰ 每分鐘自動更新"
    )

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
            clock_message = await channel.send(make_clock_text())
            print("世界時鐘訊息已建立")
        else:
            await clock_message.edit(content=make_clock_text())
            print("世界時鐘已更新")

    except Exception as e:
        print(f"錯誤：{e}")

if TOKEN is None:
    raise ValueError("找不到 DISCORD_TOKEN，請確認 Render Environment Variable 是否有設定。")

threading.Thread(target=run_web_server, daemon=True).start()
bot.run(TOKEN)
