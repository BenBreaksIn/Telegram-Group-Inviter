# Telegram Group Inviter

The Telegram Group Inviter is a script designed to automate the task of inviting users from one Telegram group to another. It's a robust tool that considers various practical limitations such as rate limiting and user privacy restrictions.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Group IDs](#getting-group-ids)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [Detailed Usage Examples](#detailed-usage-examples)
- [Contributing](#contributing)
- [License](#license)

## Requirements

To use the Telegram Group Inviter, you will need:

- Python 3.6 or later: The script is written in Python. You can download Python from the official website: https://www.python.org/downloads/
- Required Python libraries: The script uses several Python libraries. You can install them using pip. If you don't have pip installed, you can download it from https://pip.pypa.io/en/stable/installing/

The required libraries are:

  - asyncio
  - getpass
  - logging
  - telethon
  - tqdm

You can install these by using the command: `pip install asyncio getpass logging tqdm telethon`.

## Installation

Before running this script, make sure you have the required libraries installed. If you do not, you can install them with pip:

```
pip install asyncio getpass logging tqdm telethon
```

Then, clone this repository to your local machine:

```
git clone https://github.com/yourgithubusername/telegram-group-inviter.git
cd telegram-group-inviter
```

## Getting Group IDs

To use the Telegram Group Inviter, you need the ID of the Telegram group you're inviting from. If you don't know the ID of your group, you can use the `Get-Group-IDs.py` script to obtain it.

Before running `Get-Group-IDs.py`, ensure you have the required Python libraries installed. If you do not, you can install them with pip:

```bash
pip install telethon
```

Then, replace `your_api_id` and `your_api_hash` in the `Get-Group-IDs.py` file with your actual API ID and Hash. Here is the code:

```python
from telethon.sync import TelegramClient

# This is your API ID and API Hash, replace 'your_api_id' and 'your_api_hash'
# with the actual values which you got from Telegram's website when you created your application.
api_id = 'your_api_id' 
api_hash = 'your_api_hash' 

# The 'anon' argument is simply the name of the session file. This file will be created
# when you run the script and stores information about your session, so you won't have to 
# log in every time you run your script.
with TelegramClient('anon', api_id, api_hash) as client:
    
    # iter_dialogs function fetches all the dialogues associated with your account.
    # These dialogues include both private and group chats.
    for dialog in client.iter_dialogs():
        
        # This prints the name and the ID of each chat you are part of.
        print(dialog.name, 'has ID', dialog.id)
```

To run the script, navigate to the directory containing the script in your terminal, and then enter:

```bash
python Get-Group-IDs.py
```

The script will print the name and ID of each chat you're part of. You can use these IDs with the Telegram Group Inviter script.

## Environment Setup

To run the script, you need a Telegram API ID and Hash. Here's how you can obtain them:

1. Go to https://my.telegram.org and log in with your Telegram account.
2. Click on "API Development Tools".
3. Fill the form and click on "Create Application".
4. Your API ID and Hash will be displayed.

Once you have the API ID and Hash, you can set them as environment variables on your system:

For Unix-based systems (like Linux or MacOS), use:

```
export TELEGRAM_API_ID='your_api_id'
export TELEGRAM_API_HASH='your_api_hash'
```

For Windows, use:

```
set TELEGRAM_API_ID='your_api_id'
set TELEGRAM_API_HASH='your_api_hash'
```

Replace 'your_api_id' and 'your_api_hash' with your actual API ID and Hash.

## Usage

To run this script, navigate to the directory containing the script in your terminal, and then enter:

```
python telegram_group_inviter.py
```

You will be prompted to enter several pieces of information:

- Your Telegram phone number
- The link of the new Telegram group
- The ID of the old Telegram group
- The delay between invites (in seconds)
- The number of users to invite in a batch
- The total number of invites
- The start hour of activity (24-hour format)
- The end hour of activity (24-hour format)
- Your Telegram API ID (optional: you can set this as an environment variable `TELEGRAM_API_ID`)
- Your Telegram API HASH (optional: you can set this as an environment variable `TELEGRAM_API_HASH`)
- Your custom message for the invite

Example of input:

```
Enter your Telegram phone number: +1234567890
Enter the link of the new Telegram group: https://t.me/joinchat/XXXXXX
Enter the ID of the old Telegram group: 123456789
Enter the delay between invites (in seconds): 30
Enter the number of users to invite in a batch: 10
Enter the total number of

 invites: 100
Enter the start hour of activity (24-hour format): 8
Enter the end hour of activity (24-hour format): 18
Enter your Telegram API ID: 123456
Enter your Telegram API HASH: XXXXXXXXXXXXXXXXXX
Enter your custom message for the invite: Welcome to our new group!
```

Please note that using this script for spamming or any intrusive activities may violate Telegram's terms of service. Please use it responsibly.

## Detailed Usage Examples

Example 1:

Suppose you want to invite 50 users from an old group with ID '123456' to a new group with link 'https://t.me/joinchat/ABCDEFG'. You want to invite 5 users in each batch, with a delay of 20 seconds between each invite. You want the activity to start at 9 am and end at 6 pm. Here's how you can input these details:

```
Enter your Telegram phone number: +1234567890
Enter the link of the new Telegram group: https://t.me/joinchat/ABCDEFG
Enter the ID of the old Telegram group: 123456
Enter the delay between invites (in seconds): 20
Enter the number of users to invite in a batch: 5
Enter the total number of invites: 50
Enter the start hour of activity (24-hour format): 9
Enter the end hour of activity (24-hour format): 18
Enter your Telegram API ID: your_api_id
Enter your Telegram API HASH: your_api_hash
Enter your custom message for the invite: Welcome to our new group!
```

The script will now run, inviting users from the old group to the new one during the specified hours.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License
