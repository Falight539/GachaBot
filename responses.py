import discord
import Gacha

from sklearn.preprocessing import StandardScaler
import numpy as np
from keras.models import Sequential
import pandas as pd

from datetime import datetime, timedelta

users = {}

cheapest_c = 0

def forecast(model: Sequential, start: str, end: str):
    data = {"Date": []}
    time = []

    start_y, start_m, start_d = start.split('-')
    end_y, end_m, end_d = end.split('-')

    date = datetime(int(start_y), int(start_m), int(start_d), 0, 0, 0)
    stop = datetime(int(end_y), int(end_m), int(end_d), 0, 0, 0)

    del start_y, start_m, start_d, end_y, end_m, end_d

    for i in range(30):
        data['Date'].append(pd.Timestamp(date))
        time.append(date)
        if date == stop:
            break
        date += timedelta(days=1)
    
    x_new = pd.DataFrame(data)

    del date

    x_new = StandardScaler().fit_transform(x_new)
    result = model.predict(x_new[:, :, np.newaxis])

    del x_new

    return time, result

def package_cal(req: int, package: list):

    if req <= 0:
        return None

    temp = None
    packs = []
    total = 0
    limit = req
    last = True

    for i, d in enumerate(package):
        c, p = d[0], d[1]
        if req >= c:
            if last and i != 0 and package[i-1][0] > limit:
                temp = (package[i-1][0], package[i-1][1])
                last = False
            n = req//c
            req = req%c
            if c == 60 and req < 60:
                packs.append([c, n+1])
                total += (n+1) * p
            else:
                packs.append([c, n])
                total += (n) * p
        elif i == (len(package)-2) and limit != req:
            next_c = package[i+1][0]
            margin = 5
            if int(next_c*margin) < req:
                packs.append([c, 1])
                total += p
                break
        elif req <= 60:
            packs.append([60, 1])
            total += 27.3
            break
    
    if temp is None:
        return packs
    
    if temp[1] <= total and not last:
        return temp
    
    return packs
        
def create_str(c, n):
    return f"**`Purchase package {c} gems (included bonus), {n} package(s)`**"
        
async def handle_respose(message, user_message, is_private, bot: discord.Client, model: Sequential) -> str:
    p_message = user_message.lower()

    def check(m):
        return m.channel == message.channel and m.author == message.author

    if p_message == '!hello':

        em = discord.Embed()
        em.title = "Welcome to Genshin Impact gacha planner!"
        em.description = "I'm your assistant helping you to plan your next move!!"
        em.color = 1146986
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

        return

    elif p_message == '!tutorial':

        em = discord.Embed()
        pass

    # Initializing user's account
    elif p_message == '!init':

        em = discord.Embed()
        em.title = "Initialize your account (Reset everyday!)"
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

        return
    
    # Planing for 100 % chance wining this banner
    elif p_message == '!start':

        em = discord.Embed()
        em.title = "Let me help you plan your next move!!"
        em.description = "Please enter Start date, End date, and your current Crystal + Pimogem"
        em.color = 10181046
        await message.author.send(embed=em) if is_private else await message.channel.send(embed=em)
        msg = "**`1. Start date (yyyy-mm-dd): `**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        start = await bot.wait_for('message', check=check)
        msg = "**`2. End date (yyyy-mm-dd): `**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        end = await bot.wait_for('message', check=check)
        msg = "**`3. total Crystal + Pimogem: `**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        current = await bot.wait_for('message', check=check)
        current = int(current.content)

        name = str(message.author)
        pulls = users[name].wished()

        if pulls == -1:
            msg = "**`Error to fetch your wishes data, please do initialization again`**"
            await message.author.send(msg) if is_private else await message.channel.send(msg)
            return
        
        msg = f"**`Your current wishes is '{pulls}' with no 5 stars character`**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        msg = f"**`You need more '{90-pulls}' wishes to obtain next 5 stars character`**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)

        gem = users[name].free_possible(str(start.content), str(end.content), current)

        msg = f"**`You will have approximately '{gem} gems' at the end of your determined date`**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)

        ## Consider which pack you should buy in order to win the banner
        item = [[8080, 2519.3], [3880, 1259.3], [2240, 706.3], [1090, 384.3], [330 ,125.3], [60 ,27.3]]
        required = int((90-pulls) * 160)
        confirm = int(90 * 160)
        abs_req = (required + confirm) - gem
        
        msg = f"**`You need {required} more gems to obtain the next SSR character (not include free gems yet)`**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        msg = f"**`You need {abs_req+gem} more gems for 100% winning this banner (not include free gems yet)`**"
        await message.  author.send(msg) if is_private else await message.channel.send(msg)

        ssr_plan = package_cal((required-gem), item)
        abs_plan = package_cal(abs_req, item)

        if required < gem:
            msg = "**`Just collect every free gem will give you 50% Chance to win this banner \n(100% | if your last SSR is not the promotion character)`**"
            await message.author.send(msg) if is_private else await message.channel.send(msg)
            if abs_req <= 0:
                msg = "**`Anyway, you are going to win this banner without any purchase from your ton of available gems`**"
                await message.author.send(msg) if is_private else await message.channel.send(msg)
            else:
                if type(abs_plan) == tuple:
                    msg = f"**`For 100%, from the power of the darkside, I would reccomend you to buy {abs_plan[0]} gems (included bonus) package`**"
                    await message.author.send(msg) if is_private else await message.channel.send(msg)
                else:
                    msg = "**`From the power of the darkside, I would reccomend you to follow this plan in order to 100% win this banner`**"
                    await message.author.send(msg) if is_private else await message.channel.send(msg)

                    for c, n in abs_plan:
                        msg = create_str(c, n)
                        await message.author.send(msg) if is_private else await message.channel.send(msg)
        else:
            msg = "**`From the order of the god, I would reccomend you to follow this plan for 50% Chance winning this banner \n(100% | if your last SSR is not the promotion character)`**"
            await message.author.send(msg) if is_private else await message.channel.send(msg)

            if type(ssr_plan) == tuple:
                msg = f"**`Purchase {ssr_plan[0]} gems (included bonus) package`**"
                await message.author.send(msg) if is_private else await message.channel.send(msg)
            else:
                for c, n in ssr_plan:
                    msg = create_str(c, n)
                    await message.author.send(msg) if is_private else await message.channel.send(msg)
            
            msg = "**`Also I would reccomend you to follow this plan for 100% Chance winning this banner`**"
            await message.author.send(msg) if is_private else await message.channel.send(msg)

            if type(abs_plan) == tuple:
                msg = f"**`Purchase {abs_plan[0]} gems (included bonus) package`**"
                await message.author.send(msg) if is_private else await message.channel.send(msg)
            else:
                for c, n in abs_plan:
                    msg = create_str(c, n)
                    await message.author.send(msg) if is_private else await message.channel.send(msg)
        
        ## USE AI to predict the most possibily cheapest exchange
        time, result = forecast(model, str(start.content), str(end.content))

        index, mx = 0, -1e9
        for i, d in enumerate(result):
            d = d[0]
            if d > mx:
                index = i
                mx = d
        
        msg = f'**`{str(time[index]).split(" ")[0]} is the best day to follow the bless of godness (Buy in UAH currency)`**'
        await message.author.send(msg) if is_private else await message.channel.send(msg)
    
    # Find best possible way to deal with this banner under the budget
    elif p_message == '!budget':

        name = str(message.author)

        if users[name].roll_count == -1:
            msg = f"**`Please use !start first before use this command`**"
            await message.author.send(msg) if is_private else await message.channel.send(msg)
            return
        
        msg = "**`Please enter you budget in USD currency`**"
        await message.author.send(msg) if is_private else await message.channel.send(msg)
        budget = await bot.wait_for('message', check=check)

        wishes_budget = int(budget * cheapest_c)
        crystal = 0

        item = [[8080, 2519], [3880, 1259], [2240, 706], [1090, 384], [330 ,125], [60 ,27]]

        for c, p in item:
            if p > wishes_budget:
                continue
            
            crystal += int(wishes_budget//p) * c
            wishes_budget = wishes_budget%p

        pulls = (crystal + users[name].current)//160

        users[name].add_rolls(pulls)

        users[name].simulate()


        



        
        