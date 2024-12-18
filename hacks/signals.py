from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

#telegram imports
import asyncio
import logging
from telegram import Bot
from telegram.error import TimedOut, NetworkError, BadRequest

@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def update_hack_votes(sender, instance, **kwargs):
    try:
        # Ensure the related comment exists before proceeding
        hack = instance.hack
        if hack:
            # Update the reply_count field manually
            hack.reply_count = hack.countComments
            hack.save()  # Save the updated reply_count field
    except Hack.DoesNotExist:
        pass  # Safely handle the case where the related comment does not exist


@receiver(post_save, sender=Reply)
@receiver(post_delete, sender=Reply)
def update_hack_votes(sender, instance, **kwargs):
    try:
        # Ensure the related comment exists before proceeding
        comment = instance.comment
        if comment:
            # Update the reply_count field manually
            comment.reply_count = comment.countReplies
            comment.save()  # Save the updated reply_count field
    except Comment.DoesNotExist:
        pass  # Safely handle the case where the related comment does not exist

    

# def createWriter(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         Writer.objects.create(
#             user=user,
#         )
# post_save.connect(createWriter, sender=User)



API_TOKEN = '7481624614:AAG7plQdEe75J-prcIEmNfYF8AVFoSfW-hU'
CHAT_ID = '-1002181674693'  # Replace this with your actual chat ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_message(sender, instance, created, **kwargs):
    bot = Bot(token=API_TOKEN)
    report_id = str(instance.hack.id)
    text = f"Someone reported [this](https://40tavsiya.uz/hacks/{report_id}) hack"
    retry_attempts = 3
   
    for attempt in range(retry_attempts):
        try:
            await bot.send_message(CHAT_ID, text=text, parse_mode='MarkdownV2')
            logger.info("Message sent successfully!")
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

post_save.connect(send_message, sender=Report)