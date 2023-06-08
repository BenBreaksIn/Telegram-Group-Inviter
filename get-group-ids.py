import configparser
import logging
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Setting up logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


def get_config():
    """Reads API config from a file."""
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config['Telegram']['api_id'], config['Telegram']['api_hash']


def main():
    api_id, api_hash = get_config()
    # We are using try-except block to handle potential errors
    try:
        with TelegramClient('anon', api_id, api_hash) as client:
            # Fetch all the dialogues associated with your account
            for dialog in client.iter_dialogs():
                # Log the name and the ID of each chat
                logging.info(f"{dialog.name} has ID {dialog.id}")
    except SessionPasswordNeededError:
        logging.error('Password needed for this session. Please provide it.')
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')


if __name__ == '__main__':
    main()
