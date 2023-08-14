from pyrogram import Client, filters, raw
from pyrogram.types import Message, ChatPermissions
import os, jdatetime
from os.path import join, getsize
from time import time, sleep, ctime
from jdatetime import datetime as dt
from googlesearch import search
from requests import get
from googletrans import Translator
from yandex.Translater import Translater
import time



translator = Translator()
weather_api = 'enter weather api here'

bot = Client(
	name="self_bot",
	api_id=2421227,
	api_hash="5cfbdb99e4477b828bf06a9cd1efeead",
	#proxy={"scheme":"socks5", "hostname":"127.0.0.1", "port":1080},
	hide_password=True
)

@bot.on_message(filters.me & filters.command(["r"]))
def raw(Client, Message):
    Message.delete()
    try:
        if len(str(Message)) <= 4090:
            bot.send_message("me", str(Message))
        elif len(str(Message)) > 4090:
            bot.send_message("me", str(Message)[0:4090])
            bot.send_message("me", str(Message)[4089:])
    except:
        Message.reply('Error Code 01')


@bot.on_message(filters.me & filters.command(["uid"]))
def user_id(Client, Message):
    if len(Message.command) == 2:
        try:
            if str(Message.entities[1].type) == 'MessageEntityType.TEXT_MENTION':
                Message.edit_text(f'{Message.text}\n{Message.entities[1].user.id}')
            elif str(Message.entities[1].type) == 'MessageEntityType.MENTION':
                Message.edit_text(f'{Message.text}\n{bot.get_users(str(Message.command[1])).id}')
        except:
            print("Error Code 02")
    elif hasattr(Message, 'reply_to_message'):
        if hasattr(Message.reply_to_message, 'from_user'):
            Message.edit(f'{Message.text}\n{str(Message.reply_to_message.from_user.id)}')

@bot.on_message(filters.me & filters.command(["info"]))
def info(Client, Message):
    try:
        Message.edit_text(f"""Firstname : {Message.reply_to_message.from_user.first_name}
Last name : {Message.reply_to_message.from_user.last_name}
Username : {Message.reply_to_message.from_user.username}
user id : {Message.reply_to_message.from_user.id}
online status : {Message.reply_to_message.from_user.status}
bot : {Message.reply_to_message.from_user.is_bot}
scam : {Message.reply_to_message.from_user.is_scam}""")
    except:
        Message.edit_text("The replied message is either removed or you forgot to reply .\nError Code 03")

@bot.on_message(filters.me & filters.command(["idpv"]))
def idpv(Client, Message):
    try:
        try:
            Message.delete()
            bot.send_message("me",f"user id : {Message.reply_to_message.from_user.id}")
        except:
            bot.send_message("me",f"You either replied on a channel or a didn\'t even reply to any message'\nuser id : {Message.chat.id}")
    except:
        print("Error Code 04")

@bot.on_message(filters.me & filters.command(["time"]))
def send_time(Client, Message):
    try:
        Message.edit(f'Time: {dt.now().strftime("%Y-%m-%d %H:%M:%S")}')
    except:
        print("Error Code 05")

@bot.on_message(filters.me & filters.command(["gstat"]))
def group_stat(Client, Message):
    try:
        if str(Message.chat.type) == 'ChatType.SUPERGROUP' or str(Message.chat.type) == 'ChatType.group':
            pers = [str(Message.chat.permissions.can_send_messages),str(Message.chat.permissions.can_send_media_messages),		  str(Message.chat.permissions.can_send_other_messages),str(Message.chat.permissions.can_send_polls),str(Message.chat.permissions.can_add_web_page_previews),str(Message.chat.permissions.can_change_info),str(Message.chat.permissions.can_invite_users),str(Message.chat.permissions.can_pin_messages)]
            bot.send_message("me",f"""{Message.text}\nGroup name : {Message.chat.title}
Group type : {Message.chat.type}
Group id : {Message.chat.id}
Group permissions :
    Sending messages: {pers[0]}
    Sending media: {pers[1]}
    Sending other messages: {pers[2]}
    Sending polls: {pers[3]}
    Web previews: {pers[4]}
    Changing group info: {pers[5]}
    Inviting users: {pers[6]}
    Pin message: {pers[7]}""")
    except:
        print("Error Code 06")





@bot.on_message(filters.me & filters.command(["dl_media"]))
def name(Client, Message):
    bot.delete_messages(Message.chat.id, Message.id)
    if len(Message.command) > 1:
        try:
            bot.download_media(Message.command[1])
            try:
                for root, dirs, files in os.walk('./downloads'):
                    for i in files:
                        bot.send_photo("me", './downloads/' + i)
                        os.remove('./downloads/' +  i)
            except:
                Message.edit("me", "Error Code 07.2")
        except:
            Message.edit("me", "Error occured whem downloading/uploading/removing image\nError Code 07.3")

@bot.on_message(filters.me & filters.command(["udel"]))
def user_del(Client, Message):
    bot.delete_messages(Message.chat.id, Message.id)
    if str(Message.chat.type) == 'ChatType.SUPERGROUP':
        if bool(Message.reply_to_message) == True:
            if 1 == len(Message.command):
                try:
                    bot.delete_user_history(Message.chat.id, int(Message.reply_to_message.from_user.id))
                except:
                    print("Error Code 08")
                    
        elif 2 == len(Message.command):
            print('started\n')
            try:
                bot.delete_user_history(Message.chat.id, int(Message.command[1]))
            except:
                print("Error Code 08.1")

    elif str(Message.chat.type) == 'ChatType.GROUP':
        if bool(Message.reply_to_message) == True:
            if 1 == len(Message.command):
                try:
                    print(Message.reply_to_message.from_user.id)
                    for message in bot.search_messages(Message.chat.id, int(Message.reply_to_message.from_user.id)):
                        bot.delete_messages(Message.chat.id, message.id)
                except:
                    print("Error Code 09")

            elif 2 == len(Message.command):
                try:
                    for message in bot.search_messages(Message.chat.id, int(Message.command[1])):
                        bot.delete_messages(Message.chat.id, message.id)
                except:
                    print("Error Code 09.1")

@bot.on_message(filters.me & filters.command(["gem"]))
def gem(Client, Message):
    bot.delete_messages(Message.chat.id, Message.id)
    try:
        bg_id = str(bot.create_supergroup(f'{Message.chat.title} Report').id)
        bot.send_message(bg_id, Message.chat.title)
        for member in bot.get_chat_members(Message.chat.id):
            fo = bot.get_chat_member(Message.chat.id, member.user.id)
            chat_info = eval(str(fo).replace('false', 'False').replace('true', 'True'))
            bot.send_message(bg_id, f"""First name : {member.user.first_name}
Last name : {member.user.last_name}
username : {member.user.username}
user id : {member.user.id}
status : {member.status}
bot : {member.user.is_bot}
scam : {member.user.is_scam}
Join date: {chat_info.get("joined_date")}""")
    except Exception as e:
        print(e)
        Message.reply('Error Code 10')

@bot.on_message(filters.me & filters.command(["cg"]))
def create_grp(Client, Message):
    try:
        if 2 <= len(Message.command):
            if 3 <= len(Message.command):
                bot.create_supergroup(Message.command[1], Message.command[2])
            else:
                bot.create_supergroup(Message.command[1])
            bot.edit_message_text(Message.chat.id, Message.id, f'{Message.command[1]} group created successfully !')
        else:
            return false
    except:
        print("Error Code 11")

@bot.on_message(filters.me & filters.command(["del"]))
def delete_msg(Client, Message):
    try:
        delndx = int(Message.command[1])+1
        i = []
        cnt = 1
        for message in bot.get_chat_history(chat_id = Message.chat.id, limit = delndx):
            if len(i) == 1:
                pass
            if cnt == 200:
                bot.delete_messages(Message.chat.id, i)
                i = []
                sleep(1)
            else:
                if delndx <= 101:
                    i.append(message.id)
                else:
                    i.append(message.id)
        if len(i) != 0:
            bot.delete_messages(Message.chat.id, i)
            i = []
        bot.send_message(Message.chat.id,f"Deleted {delndx} messages")
    except:
        print("Error Code 12")

@bot.on_message(filters.me & filters.command(["clean"]))
def full_cleanup(Client, Message):
    try:
        if str(Message.chat.type) != "ChatType.SUPERGROUP":
            bot.send_message(Message.chat.id, "You can only execute this command in Supergroups.")
            pass
        else:
            for message in bot.get_chat_history(chat_id=Message.chat.id):
                bot.delete_user_history(Message.chat.id, message.from_user.id)
    except:
        print("Error Code 13")

@bot.on_message(filters.me & filters.command(["mute"]))
def mute(Client, Message):
    if (1 == len(Message.command)) & hasattr(Message, 'reply_to_message'):
        print(10)
        if hasattr(Message.reply_to_message, 'from_user'):
            print(11)
            bot.restrict_chat_member(Message.chat.id, Message.reply_to_message.from_user.id, ChatPermissions(can_send_messages = False))
    elif (2 == len(Message.command)) & hasattr(Message, 'entities'):
        print(20)
        if Message.command[1].isnumeric:
            try:
                print(25)
                bot.restrict_chat_member(Message.chat.id, user_id, ChatPermissions(), datetime.now() + timedelta(minutes = Message.command[1]))
            except Exception as e:
                print(e)
                #Message.edit_text('Error occured muting user.\nError code: 14')
        elif len(Message.entities) == 2:
            print(21)
            if str(Message.entities[1].type) == 'MessageEntityType.TEXT_MENTION':
                print(22)
                try:
                    print(23)
                    bot.restrict_chat_member(Message.chat.id, Message.reply_to_message.from_user.id, ChatPermissions(can_send_messages = False))
                except:
                    Message.edit_text('Error occured muting user.\nError code: 14.1')

@bot.on_message(filters.me & filters.command(["unmute"]))
def unmute(Client, Message):
    if (1 == len(Message.command)) & hasattr(Message, 'reply_to_message'):
        if hasattr(Message.reply_to_message, 'from_user'):
            bot.restrict_chat_member(Message.chat.id, Message.reply_to_message.from_user.id, ChatPermissions(can_send_messages = True))
    elif 2 == len(Message.command):
        try:
            bot.restrict_chat_member(Message.chat.id, Message.command[1], ChatPermissions(can_send_messages = True))
            Message.edit_text(f'{Message.text} unmuted')
        except:
            Message.edit_text(f'{Message.text}\nError occured unmuting user.\nError code: 15')

@bot.on_message(filters.me & filters.command(["ban"]))
def ban(Client, Message):
    if (1 == len(Message.command)) & hasattr(Message, 'reply_to_message'):
        if hasattr(Message.reply_to_message, 'from_user'):
            bot.ban_chat_member(Message.chat.id, Message.reply_to_message.from_user.id)
    elif (2 == len(Message.command)) & hasattr(Message, 'entities'):
        if len(Message.entities) == 2:
            if str(Message.entities[1].type) == 'MessageEntityType.TEXT_MENTION':
                try:
                    bot.ban_chat_member(Message.chat.id, Message.reply_to_message.from_user.id)
                except:
                    Message.edit_text('Error occured banning user.\nError code: 16')
            else:
                try:
                    bot.ban_chat_member(Message.chat.id, user_id, datetime.now() + timedelta(days = int(Message.command[1])))
                except:
                    Message.edit_text('Error occured banning user.\nError code: 17')

@bot.on_message(filters.me & filters.command(["unban"]))
def unban(Client, Message):
    if (1 == len(Message.command)) & hasattr(Message, 'reply_to_message'):
        if hasattr(Message.reply_to_message, 'from_user'):
            bot.unban_chat_member(Message.chat.id, Message.reply_to_message.from_user.id)
    elif (2 == len(Message.command)) & hasattr(Message, 'entities'):
        if len(Message.entities) == 2:
            if str(Message.entities[1].type) == 'MessageEntityType.TEXT_MENTION':
                try:
                    bot.unban_chat_member(Message.chat.id, Message.reply_to_message.from_user.id)
                except:
                    Message.edit_text('Error occured banning user.\nError code: 18')
            else:
                try:
                    bot.unban_chat_member(Message.chat.id, Message.command[1])
                except:
                    Message.edit_text('Error occured banning user.\nError code: 19')
    bot.unban_chat_member(Message.chat.id, Message.command[1])


@bot.on_message(filters.me & filters.command(["boom"]))
def boom(Client, Message):
    list_boom = ["🧨🌲🌲🌲🌲🌲🌲🌲🚜","🧨🌲🌲🌲🌲🌲🌲🚜","🧨🌲🌲🌲🌲🌲🚜","🧨🌲🌲🌲🌲🚜","🧨🌲🌲🌲🚜","🧨🌲🌲🚜","🧨🌲🚜","🧨🚜","💥вσσσм💥"]
    try:
        for i in list_boom:
            Message.edit(i)
            time.sleep(1)
    except:
        bot.send_message(Message.chat.id, 'تموم شد')

@bot.on_message(filters.me & filters.command(["pashm"]))
def boom(Client, Message):
    list_boom = ['🍂🍂🍂🍂🍂🍂🍂🍂🍂🍂🍂🍂🍂🍂🍂', '🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁', '🍃🍃🍃🍃🍃🍃🍃🍃🍃🍃🍃🍃🍃🍃🍃', '🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱', '☘️☘️☘️☘️☘️☘️☘️☘️☘️☘️☘️☘️☘️☘️☘️',
                 'پشم دیگه ندارم ولی برگام ریخت بمولا', '🍃🍂🍁🌱🌿☘️🍀🍃🍁🍂🌿🌱☘️🍀🍃', '🍂🍁🌱🌿🍂🍁🌱🌿🍂🍁🌱🌿🍂🍁🌱🌿', 'دیگه برگی برام نمونده ']
    try:
        for i in list_boom:
            Message.edit(i)
            time.sleep(1)
    except:
        bot.send_message(Message.chat.id, 'تموم شد')

@bot.on_message(filters.me & filters.command(["colors"]))
def boom(Client, Message):
    list_boom = ["🟧🟨🟩🟦🟪", "🟫🟨🟩🟦🟪", "🟦🟫🟥🟦🟩", "🟧🟪🟩⬜️⬛️", "🟧🟨🟩🟦🟪🔳", "🟧🟨🟩🟦🔳🟪",
                 "🟧🟨🟩🔳🟦🟪", "🟧🟨🔳🟩🟦🟪", "🟧🔳🟨🟩🟦🟪", "🔳🟧🟨🟩🟦🟪", "🔳🔳🟨🟩🟦🟪", "🔳🔳🔳🟩🟦🟪",
                 "🔳🔳🔳🔳🔳🔳", "🔲🔲🔲🔲🔲🔲", "🔳🔳🔳🔳🔳🔳", "FINISH 🟡🟠🔴🟢🔵🟣⚫️⚪️🟤", "FINISH 🟡⚫️⚪️🟤🟢🔵🟣🟠🔴"]
    try:
        for i in list_boom:
            Message.edit(i)
            time.sleep(1)
    except:
        bot.send_message(Message.chat.id, 'تموم شد')

@bot.on_message(filters.me & filters.command(["fuck_you"]))
def boom(Client, Message):
    list_boom = ["*fuck you*🖕🏿🖕🏾🖕🏽🖕🏼🖕🏻🖕", "🖕🏿", "*Fuck you*🖕🖕🏻🖕🏼🖕🏽🖕🏾🖕🏿""🖕", "*FUck you*🖕🏿🖕🖕🏾🖕🏻🖕🏽🖕🏼", "🖕🏻",
                 "*FUCk you*🖕🏼🖕🖕🏻🖕🏽🖕🏾🖕🏿", "🖕🏾", "*FUCK You*🖕🏼🦶🏻👊👺", "🖕", "🖕🏻", "🖕🏾", "🖕🖕🏻", "🖕🏿🖕🏿🖕🏿", "🖕🏼🖕🏼🖕🏼", "🖕🏼"]
    try:
        for i in list_boom:
            Message.edit(i)
            time.sleep(1)
    except:
        bot.send_message(Message.chat.id, 'تموم شد')


@bot.on_message(filters.me & filters.command(["smail"]))
def boom(Client, Message):
    list_boom =["😀", "😃", "😄", "😁", "😆", "😂", "🤣"]
    try:
        for i in list_boom:
            Message.edit(i)
            time.sleep(2)
    except:
        bot.send_message(Message.chat.id, 'تموم شد')

@bot.on_message(filters.me & filters.command(["hack_nasa"]))
def boom(Client, Message):
    list_boom =["HACKING 🕸NASA🕸...\n<[##        ]> 20%", "HACKING 🕸NASA🕸..\n<[###       ]> 30%",
                 "HACKING 🕸NASA🕸...\n<[####      ]> 40%", "HACKING 🕸NASA🕸..\n<[#####     ]> 50%", "HACKING 🕸NASA🕸...\n<[######    ]> 60%",
                 "HACKING 🕸NASA🕸..\n<[#######   ]> 70%", "HACKING 🕸NASA🕸...\n<[########  ]> 80%", "HACKING 🕸NASA🕸..\n<[######### ]> 90%",
                 "HACKING 🕸NASA🕸...\n<[##########]> 100%", "nasa hacked 😐🕷", "*fuck you*🖕🏿🖕🏾🖕🏽🖕🏼🖕🏻🖕"]
    try:
        for i in list_boom:
            Message.edit(i)
            time.sleep(2)
    except:
        bot.send_message(Message.chat.id, 'تموم شد')


@bot.on_message(filters.me & filters.command(["mah"]))
def boom(Client, Message):
    list_boom =["🌑🌑", "🌘🌘", "🌗🌗", "🌖🌖", "🌕🌕", "🌔🌔", "🌓🌓",
                 "🌒🌒", "🌑🌑", "🌑🌑🌑", "🌘🌘🌘", "🌗🌗🌗", "🌖🌖🌖", "🌕🌕🌕", "🌔🌔🌔", "🌓🌓🌓",
                 "🌒🌒🌒", "🌑🌑🌑", "🌑🌑🌑🌑", "🌘🌘🌘🌘", "🌗🌗🌗🌗", "🌖🌖🌖🌖", "🌕🌕🌕🌕", "🌔🌔🌔🌔", "🌓🌓🌓🌓",
                 "🌒🌒🌒🌒", "🌑🌑🌑🌑", "🌑"]
    try:
        for i in list_boom:
            Message.edit(i)
            time.sleep(2)
    except:
        bot.send_message(Message.chat.id, 'تموم شد')


@bot.on_message(filters.me & filters.command(["love"]))
def boom(Client, Message):
    list_boom =["❤️", "💛", "🧡", "💚", "💙", "💜", "🖤", "💜", "💙", "💚", "💛", "🧡", "❤️", "🧡", "💛",
                 "💚", "💙", "💜", "🖤", "❤️🖤", "🖤❤️", "🖤❤️❤️🖤", "🖤❤️❤️🖤🖤❤️❤️🖤", "❤️🖤🖤❤️❤️🖤🖤❤️",
                 "🖤❤️❤️🖤🖤❤️❤️🖤", "❤️🖤🖤❤️❤️🖤🖤❤️", "🖤❤️❤️🖤🖤❤️❤️🖤", "❤️🖤🖤❤️❤️🖤🖤❤️"
                 "❤️I LOVE YOU ❤️", "I LOVE YOU", "❤️I LOVE YOU❤️", "I LOVE YOU", "❤️I LOVE YOU❤️"]
    try:
        for i in list_boom:
            Message.edit(i)
            time.sleep(2)
    except:
        bot.send_message(Message.chat.id, 'تموم شد')

@bot.on_message(filters.me & filters.command(["get_photo"]))
def boom(Client, Message):
    list_boom =["واستا میخام ازت عکس بگیرم 😆📷",
                 "آها گرفتم 📸", "بیا اینم عکست | 🐒|     😁🖖"]
    try:
        for i in list_boom:
            Message.edit(i)
            time.sleep(2)
    except:
        bot.send_message(Message.chat.id, 'تموم شد')


@bot.on_message(filters.me & filters.command(["get_id"]))
def get_id(Client, Message):
    try:
        Message.edit_text(f'{Message.text}\n{bot.get_users(Message.command[1]).id}')
    except:
        bot.send_message(Message.chat.id, 'Error Code 23')

@bot.on_message(filters.me & filters.command(["google"]))
def search_query(Client, Message):
    try:
        if len(Message.command) > 1:
            query = " ".join(Message.command[1:])
            results = search(query, num=5, pause=2, user_agent="Mozilla/5.0", api_key=google_search_api_key)

            response = "Search Results:\n\n"
            for idx, result in enumerate(results, start=1):
                response += f"{idx}. {result}\n"

            bot.edit_message_text(
                chat_id=Message.chat.id,
                message_id=Message.message_id,
                text=response
            )
        else:
            bot.edit_message_text(
                chat_id=Message.chat.id,
                message_id=Message.message_id,
                text=f"{Message.text}\nEnter a query to search."
            )
    except Exception as e:
        print('Error during search:', e)

        
@bot.on_message(filters.me & filters.command(["weather"]))
def get_weather(Client, Message):
    test = '123'
    if len(Message.command) == 2:
        try:
            URL = "https://api.openweathermap.org/data/2.5/weather"
            PARAMS = {'q' : Message.command[1] ,'appid' : weather_api }
            r = get(url = URL, params = PARAMS).json()
            r = {
                "city" : r['name'],
                "datetime" : ctime(int(r['dt'])),
                "temp" : r['main']['temp'],
                "humidity" : r['main']['humidity']
                }
            output = f'''{Message.text}
City: {r.get('city')}
DateTime: {r.get('datetime')}
Temp: {r.get('temp')}
Humidity: {r.get('humidity')}'''
            Message.edit(output)
        except Exception as e:
            print(e)
    elif len(Message.command) == 1:
        Message.edit(f'{Message.text}\nEnter a city to search :/')
    else:
        Message.edit(f'{Message.text}\nEnter the city name properly.')


@bot.on_message(filters.me & filters.command(["translate"]))
def translate_text(client, message):
    try:
        if len(message.command) > 1:
            text = message.text[11:]  # Remove the "/translate " part
            message.edit_text(f'{message.text}\nTranslating...')

            translations = {
                'English': translator.translate(text, src='auto', dest='en').text,
                'Arabic': translator.translate(text, src='auto', dest='ar').text,
                'Persian': translator.translate(text, src='auto', dest='fa').text,
                'Italian': translator.translate(text, src='auto', dest='it').text,
                'Russian': translator.translate(text, src='auto', dest='ru').text
            }

            translation_result = '\n'.join(f'{lang}: {trans}' for lang, trans in translations.items())
            message.edit_text(f'{message.text}\n\n{translation_result}')
        elif len(message.command) == 1:
            message.edit_text(f'{message.text}\nEnter a text to translate :/')
        else:
            message.edit_text(f'{message.text}\nError code 25')
    except Exception as e:
        print("Error:", e)



bot.run()
