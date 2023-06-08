import os
import asyncio
import getpass
import logging
from random import randint, uniform
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from tqdm import tqdm

log_file = 'telegram_inviter.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

pbar = None  # Initialize pbar at the module level


def validate_activity_hours(start, end):
    if not (0 <= start <= 24 and 0 <= end <= 24):
        raise ValueError("Activity hours should be in 0-24 range")


def get_inputs():
    phone = input("Enter your Telegram phone number: ")
    new_group_link = input("Enter the link of the new Telegram group: ")
    old_group_id = int(input("Enter the ID of the old Telegram group: "))  # Converting to int
    delay = int(input("Enter the delay between invites (in seconds): "))
    batch_size = int(input("Enter the number of users to invite in a batch: "))
    total_invites = int(input("Enter the total number of invites: "))
    activity_start_hour = int(input("Enter the start hour of activity (24-hour format): "))
    activity_end_hour = int(input("Enter the end hour of activity (24-hour format): "))
    validate_activity_hours(activity_start_hour, activity_end_hour)
    api_id = os.environ.get('TELEGRAM_API_ID', input("Enter your Telegram API ID: "))
    api_hash = os.environ.get('TELEGRAM_API_HASH', input("Enter your Telegram API HASH: "))

    return phone, new_group_link, old_group_id, delay, batch_size, total_invites, activity_start_hour, activity_end_hour, api_id, api_hash


invites = 0


async def connect_and_authorize(phone, api_id, api_hash):
    client = TelegramClient('session_name', api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, getpass.getpass('Enter the code: '))

    return client


async def invite_users(client, new_group, users, delay, total_invites, activity_start_hour, activity_end_hour):
    global invites
    global pbar
    for user in users:
        for attempt in range(3):
            try:
                current_hour = datetime.now().hour
                if activity_start_hour <= current_hour < activity_end_hour:
                    if invites < total_invites:
                        await client(InviteToChannelRequest(new_group, [user.id]))
                        logging.info(f"Invited {user.id} at {datetime.now()}")
                        invites += 1
                        if pbar:
                            pbar.update(1)
                        await asyncio.sleep(randint(delay, delay + 20))
                    else:
                        print("Invitation limit reached.")
                        if pbar:
                            pbar.close()
                        return
                else:
                    logging.info("Sleeping till activity hours.")
                    sleep_time = 60 * ((activity_start_hour - current_hour) % 24)
                    await asyncio.sleep(sleep_time)  # Sleep till the start of activity hours
                break
            except FloodWaitError as e:
                logging.warning(f"Rate limit exceeded while trying to invite {user.id} at {datetime.now()}: {e}")
                await asyncio.sleep(e.seconds + uniform(1.5, 3))
            except UserPrivacyRestrictedError:
                logging.warning(f"Couldn't invite user {user.id} due to privacy settings at {datetime.now()}")
                break
            except Exception as e:
                if attempt < 2:
                    logging.error(
                        f"Error while trying to invite {user.id} at {datetime.now()}: {e}. Retrying in 5 seconds.")
                    await asyncio.sleep(5)
                else:
                    logging.error(
                        f"Error while trying to invite {user.id} at {datetime.now()}: {e}. Moving on to next user.")
                continue


async def main():
    phone, new_group_link, old_group_id, delay, batch_size, total_invites, activity_start_hour, activity_end_hour, api_id, api_hash = get_inputs()
    global pbar
    pbar = tqdm(total=total_invites)  # Move progress bar initialization here after total_invites is defined
    client = await connect_and_authorize(phone, api_id, api_hash)

    new_group = await client.get_entity(new_group_link)
    old_group = await client(GetFullChatRequest(old_group_id))

    async for user in client.iter_participants(old_group, limit=batch_size):
        await invite_users(client, new_group, [user], delay, total_invites, activity_start_hour, activity_end_hour)
    if pbar:
        pbar.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script was interrupted. Total invites: " + str(invites))
        print("Script was interrupted. Total invites: " + str(invites))
        if pbar:
            pbar.close()
