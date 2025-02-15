import logging
import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message

# --- CONFIG ---
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TERABOX_DOWNLOAD_API = "https://api.terabox.com/link-to-file"  # Example API endpoint

# --- SETUP ---
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

def download_from_terabox(url):
    """Downloads file from Terabox and returns the local file path"""
    response = requests.get(url, stream=True)
    filename = url.split("/")[-1]
    filepath = os.path.join("downloads", filename)
    os.makedirs("downloads", exist_ok=True)
    
    with open(filepath, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    return filepath

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    await message.reply("🤖 Halo! Kirimkan link Terabox dan saya akan mengunduhnya untuk Anda.")

@dp.message_handler()
async def handle_terabox_link(message: Message):
    url = message.text.strip()
    if "terabox.com" in url:
        await message.reply("🔄 Mengunduh file dari Terabox...")
        file_path = download_from_terabox(url)
        await message.reply_document(types.InputFile(file_path), caption="📂 Berikut file Anda!")
        os.remove(file_path)  # Hapus file setelah dikirim
    else:
        await message.reply("⚠️ Harap kirimkan link Terabox yang valid!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
