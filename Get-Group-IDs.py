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
