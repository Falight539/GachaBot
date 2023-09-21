import discord
import responses

async def send_message(message, user_message, is_private, bot):
    try:
        await responses.handle_respose(message, user_message, is_private, bot)
    except Exception as e:
        print(e)

def run_bot():
    TOKEN = r'MTE1Mzk2NDc5ODM4ODczMTk0NQ.GZX_Bb.Y0Ox-APkQVeDX-M7LQfi5XHzpn8tlqoOuscALg'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"username: {username} message: {user_message} channel: {channel}")

        if "Unknown User" in channel:
            await send_message(message, user_message, is_private=True, bot=client)
        else:
            await send_message(message, user_message, is_private=False, bot=client)

    client.run(TOKEN)

if __name__ == '__main__':
    run_bot()