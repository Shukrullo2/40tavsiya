import asyncio
import logging
from telegram import Bot
from telegram.error import TimedOut, NetworkError, BadRequest
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
API_TOKEN = '7585635572:AAEvBlilffRYBgr_crQDyhsiU_5OFL93OQA'
CHAT_ID = '-1002327096485'  # Replace this with your actual chat ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_message():
    bot = Bot(token=API_TOKEN)

    text = f"40tavsiya platformasiga o'tish"
    retry_attempts = 3
    
    # Create the button
    button = [[InlineKeyboardButton("O'tish", url="https://40tavsiya.uz/")]]
    reply_markup = InlineKeyboardMarkup(button)
   
    for attempt in range(retry_attempts):
        try:
            await bot.send_message(
                CHAT_ID, 
                text=text, 
                parse_mode='MarkdownV2', 
                reply_markup=reply_markup  # Attach the button
            )
            logger.info("Message sent successfully with a button!")
            break
        except TimedOut:
            logger.error(f"Attempt {attempt + 1} failed due to timeout. Retrying...")
            await asyncio.sleep(2)  # Wait for 2 seconds before retrying
        except NetworkError as e:
            logger.error(f"Network error: {e}")
            await asyncio.sleep(2)  # Wait for 2 seconds before retrying
        except BadRequest as e:
            logger.error(f"Bad request error: {e}")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            break
    else:
        logger.error("Failed to send message after several attempts.")

if __name__ == "__main__":
    asyncio.run(send_message())


