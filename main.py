import os
import asyncio
import logging
from random import randint
from datetime import datetime
from telethon import TelegramClient, errors
from tqdm import tqdm

log_file = 'telegram_inviter.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)

pbar = None  # Initialize pbar at the module level


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def validate_activity_hours(start, end):
    if not (0 <= start <= 24 and 0 <= end <= 24):
        raise ValueError("Activity hours should be in 0-24 range")


async def get_inputs():
    print("Getting user inputs...")
    logging.info("Getting user inputs...")
    phone = input("Enter your Telegram phone number: ")

    print("Connecting and authorizing...")
    logging.info("Connecting and authorizing...")
    api_id = os.environ.get('TELEGRAM_API_ID', input("Enter your Telegram API ID: "))
    api_hash = os.environ.get('TELEGRAM_API_HASH', input("Enter your Telegram API HASH: "))
    client = TelegramClient('session_name', api_id, api_hash)
    print("Client created.")
    logging.info("Client created.")
    await client.connect()
    print("Client connected.")
    logging.info("Client connected.")

    if not await client.is_user_authorized():
        print("Client not authorized. Sending code request...")
        logging.info("Client not authorized. Sending code request...")
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: '))
    print("Connected and authorized.")
    logging.info("Connected and authorized.")

    new_group_link = input("Enter the link of the new Telegram group: ")
    old_group_id = int(input("Enter the ID of the old Telegram group: "))  # Converting to int
    delay = int(input("Enter the delay between invites (in seconds): "))
    batch_size = int(input("Enter the number of users to invite in a batch: "))
    total_invites = int(input("Enter the total number of invites: "))
    activity_start_hour = int(input("Enter the start hour of activity (24-hour format): "))
    activity_end_hour = int(input("Enter the end hour of activity (24-hour format): "))
    validate_activity_hours(activity_start_hour, activity_end_hour)
    custom_message = input("Enter your custom message for invite: ")
    print("Finished getting user inputs.")
    logging.info("Finished getting user inputs.")

    return (
        client, phone, new_group_link, old_group_id, delay, batch_size,
        total_invites, activity_start_hour, activity_end_hour,
        api_id, api_hash, custom_message
    )


invites = 0


async def invite_users(
        client, new_group_link, users, delay, total_invites,
        activity_start_hour, activity_end_hour, custom_message
):
    global invites
    global pbar

    # Load list of already invited users from a file
    try:
        with open('invited_users.txt', 'r') as f:
            invited_users = f.read().splitlines()
    except FileNotFoundError:
        invited_users = []

    for user in users:
        # Skip this user if they have already been invited
        if str(user.id) in invited_users:
            continue

        logging.info(f"Starting user {user.id} invitations...")
        for attempt in range(3):
            try:
                current_hour = datetime.now().hour
                if activity_start_hour <= current_hour < activity_end_hour:
                    if invites < total_invites:
                        message = (
                            f"Hello {user.first_name}, {custom_message} Here is the link: "
                            f"{new_group_link}. Feel free to join."
                        )
                        await client.send_message(user.id, message)

                        # Record this user as invited
                        with open('invited_users.txt', 'a') as f:
                            f.write(str(user.id) + '\n')

                        logging.info(f"Invited {user.id} at {datetime.now()}")
                        invites += 1
                        if pbar:
                            pbar.update(1)
                        await asyncio.sleep(randint(delay, delay + 20))
                    else:
                        print("Invitation limit reached.")
                        logging.info("Invitation limit reached.")
                        if pbar:
                            pbar.close()
                        return
                else:
                    logging.info("Sleeping till activity hours.")
                    sleep_time = 60 * ((activity_start_hour - current_hour) % 24)
                    await asyncio.sleep(sleep_time)  # Sleep till the start of activity hours
                break
            except errors.FloodWaitError as e:
                logging.warning(
                    f"Rate limit exceeded while trying to invite {user.id} at {datetime.now()}: {e}"
                )
                await asyncio.sleep(e.seconds + 20)
            except errors.UserPrivacyRestrictedError:
                logging.warning(
                    f"Couldn't invite user {user.id} due to privacy settings at {datetime.now()}"
                )
                break
            except Exception as e:
                logging.error(
                    f"Error while trying to invite {user.id} at {datetime.now()}: {e}. Moving on to next user."
                )
                continue
        logging.info(f"Finished user {user.id} invitations.")


async def main():
    (
        client, phone, new_group_link, old_group_id, delay, batch_size,
        total_invites, activity_start_hour, activity_end_hour,
        api_id, api_hash, custom_message
    ) = await get_inputs()

    global pbar
    pbar = tqdm(total=total_invites)  # Move progress bar initialization here after total_invites is defined

    try:
        old_group = await client.get_entity(old_group_id)
    except ValueError:
        print("The provided group ID is invalid.")
        return

    users = await client.get_participants(old_group, aggressive=True)

    for user_chunk in chunks(users, batch_size):
        await invite_users(
            client, new_group_link, user_chunk, delay, total_invites,
            activity_start_hour, activity_end_hour, custom_message
        )

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
