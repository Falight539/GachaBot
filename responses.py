import discord
import Gacha

users = {}

async def handle_respose(message, user_message, is_private, bot: discord.Client) -> str:
    p_message = user_message.lower()

    def check(m):
        return m.channel == message.channel and m.author == message.author

    if p_message == '!hello':
        em = discord.Embed()
        em.title = "Welcome to Genshin Impact gacha planner!"
        em.description = "I'm your assistant helping you to plan your next move!!"
        em.color = 1752220
        em.add_field(
            name="All commands ", 
            value="""
            `!tutorial`: If you need some help \n
            `!init`: Setting up your account \n
            `!start`: Find the best solution to win this banner \n
            `!budget`: Find your probability to win this banner under the budget
            """, 
            inline=True
            )
        await message.author.send(embed=em) if is_private else await message.channel.send(embed=em)

        del em

    elif p_message == '!tutorial':
        em = discord.Embed()
        pass
    
    elif p_message == '!init':

        em = discord.Embed()
        em.title = "Initialize your account"
        em.description = "In order to plan your next move, please fill up 4 important informations ~"
        em.color = 16705372
        await message.author.send(embed=em) if is_private else await message.channel.send(embed=em)
        msg = "**`1. Your uid: `**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        uid = await bot.wait_for('message', check=check)
        msg = "**`2. Your ltuid or account_id: `**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        account_id = await bot.wait_for('message', check=check)
        msg = "**`3. Your ltken or cookie_token: `**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        account_token = await bot.wait_for('message', check=check)
        msg = "**`4. Your authURL: `**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        AuthURL = await bot.wait_for('message', check=check)
        msg = "**`Initialization Successful...`**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        msg = "**`Long time to figured this out, wasn't it? :-) -- from devs`**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)

        users[str(message.author)] = Gacha.planer(int(uid.content), int(account_id.content), str(account_token.content), str(AuthURL.content))

        del em, uid, account_id, account_token, AuthURL

        me = users[str(message.author)]
        user_data = me.see_stat()

        msg = f"**`Please check below stats wheater they match with your stats or not?`** \n ``` achievements = {user_data['achievements']} \n characters = {user_data['characters']}```"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
    
    elif p_message == '!start':
        pass



        