token = "8049956611:AAE4C2Gm_OgDwQXJVO4BJwlAAaDOi8tx0wU"
ownerID = int("1965941065")

import asyncio, requests, re, os, time
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, InlineQueryResultCachedAudio, InlineQueryResultCachedVideo
from kvsqlite.sync import Client as DB
from yt_dlp import YoutubeDL
from threading import Thread 
from youtube_search import YoutubeSearch as Y88F8
from datetime import date
from pyrogram.errors import FloodWait 
botdb = DB('botdb.sqlite')

bot = Client(
  'bot'+token.split(":")[0],
  14972930, 
 'afe0af38c207b1ef65fcfe2c57ef79de',
  bot_token=token, in_memory=False
)

bot.start()
botUsername="@"+bot.me.username

STARTTEXT = """⌁︙آهلا بكَِ في بوت تحميل جميع المواقع
⌁︙يمكنك التحميل من ( اليوتيوب ، انستقرام ، تيكتوك ، فيسبوك ، تويتر ، سناب شات ، ساوند كلاود )

 تحمل اي شي يعجبك بسهولة تامة 🔥

"""

STARTKEY = InlineKeyboardMarkup(
       [
         [
           InlineKeyboardButton("≈ إذاعة للمستخدمين ≈", callback_data="broadcast")
         ],
         [
           InlineKeyboardButton("≈ الاحصائيات ≈", callback_data="stats"),
           InlineKeyboardButton("≈ المحظورين ≈", callback_data="bannedstats"),
         ],
         [
           InlineKeyboardButton("≈ كشف مستخدم ≈",callback_data="whois"),
           InlineKeyboardButton("≈ حظر مستخدم ≈",callback_data="ban"),
         ],
         [
           InlineKeyboardButton("≈ الغاء حظر مستخدم ≈",callback_data="unban"),
         ],
       ]
     )
if not botdb.get("db"+token.split(":")[0]):
   data = {
     "users":[],
     "admins":[],
     "banned":[],
   }
   botdb.set("db"+token.split(":")[0], data)

if not ownerID in botdb.get("db"+token.split(":")[0])["admins"]:
   data = botdb.get("db"+token.split(":")[0])
   data["admins"].append(ownerID)
   botdb.set("db"+token.split(":")[0], data)

def Find(text):
  m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
  url = re.findall(m,text)  
  return [x[0] for x in url]

async def pin_it(url,m):
   msg = await m.reply("⌛| يتم قياس حجم التحميل ، انتظر...")
   try:
     vid_data = YoutubeDL({}).extract_info(url, download=False)
     await m.reply_video(vid_data["url"], quote=True, caption=botUsername)
   except:
     try:
       get = requests.get(url).text
       img = re.search(r'name="og:image" content="([^"]+)',get).group(1)
       await m.reply_photo(img, quote=True, caption=botUsername)
     except:
       pass
   return await msg.delete()

async def facebook(url,m):
   msg = await m.reply("⌛| يتم قياس حجم التحميل ، انتظر...")
   try:
     vid_data = YoutubeDL({}).extract_info(url, download=False)
     await m.reply_video(vid_data["requested_formats"][0]["url"], quote=True, caption=botUsername)
   except:
     return await msg.edit("😐| حدث خطأ")
   return await msg.delete()

async def instagram(url,m):
   msg = await m.reply("⌛| يتم قياس حجم التحميل ، انتظر...")
   try:
     vid_data = YoutubeDL({}).extract_info(url, download=False)
     await m.reply_video(vid_data["url"], quote=True, caption=botUsername)
   except:
     return await msg.edit("😐| حدث خطأ")
   return await msg.delete()

async def tiktok(url,m):
   msg = await m.reply("⌛| يتم قياس حجم التحميل ، انتظر...")
   try:
     vid_data = YoutubeDL({}).extract_info(url, download=False)
     await m.reply_video(vid_data["url"], quote=True, caption=botUsername)
   except:
     return await msg.edit("😐| حدث خطأ")
   return await msg.delete()

async def snapchat(url,m):
   msg = await m.reply("⌛| يتم قياس حجم التحميل ، انتظر...")
   try:
     vid_data = YoutubeDL({}).extract_info(url, download=False)
     await m.reply_video(vid_data["url"], quote=True, caption=botUsername)
   except:
     return await msg.edit("😐| حدث خطأ")
   return await msg.delete()

async def soundcloud(url,m):
   msg = await m.reply("⌛| يتم قياس حجم التحميل ، انتظر...")
   with YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=False)
           if int(ytdl_dataa['duration']) > 1205:
              return await msg.edit('مقطع اكثر من ٢٥ دقيقة مقدر انزله')
   with YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=True)
           file_name = ytdl.prepare_filename(ytdl_dataa)
   title = ytdl_dataa['title']
   a=await m.reply_audio(file_name,title=title, performer=title[:10], duration=int(ytdl_dataa['duration']),quote=True)
   await a.edit_reply_markup(
      InlineKeyboardMarkup (
        [[InlineKeyboardButton ("• مشاركة •", switch_inline_query=f"audio={a.audio.file_id}")]]
      )
    )
   os.remove(file_name)
   return await msg.delete()

async def other(url,m):
   msg = await m.reply("⌛| يتم قياس حجم التحميل ، انتظر...")
   async def progress(current, total):
         print(f"- [ {current * 100 / total:.1f}% ]")
   try:
     with YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=True)
           await msg.edit("تم استخراج معلومات الرابط، بتم التحميل")
           file_name = ytdl.prepare_filename(ytdl_dataa)
           await msg.edit("تم التحميل يتم الإرسال")
     try:
       await m.reply_video(file_name,quote=True, progress=progress,thumb="photo.jpg")
     except:
       try:
         await m.reply_audio(file_name,quote=True, progress=progress,thumb="photo.jpg")
       except:
         await m.reply_document(file_name,quote=True, progress=progress)
   except:
      await msg.edit("الموقع غير مدعوم")
   try:
     os.remove(file_name)
   except:
     pass
   return await msg.delete()

async def twitter(url,m):
   msg = await m.reply("⌛| يتم قياس حجم التحميل ، انتظر...")
   try:
     vid_data = YoutubeDL({}).extract_info(url, download=False)
     await m.reply_video(vid_data["url"], quote=True, caption=botUsername)
   except:
     return await msg.edit("😐| حدث خطأ")
   return await msg.delete()

async def youtube(url,m):
   result = Y88F8(url,max_results=1).to_dict()[0]
   thumb = result["thumbnails"][0]
   id = result["id"]
   title=result["title"]
   channel=result["channel"]
   duration=result["duration"]
   views=result["views"]
   caption=f"""
🎬 [{title}](https://youtu.be/{id})
👤 {channel}
🕑 {duration} - 👁 {views}
"""
   reply_markup=InlineKeyboardMarkup (
     [
       [
        InlineKeyboardButton ("🔊 ملف صوتي",callback_data=f"AUDIO:{id}"),
        InlineKeyboardButton ("🎥 ملف فيديو",callback_data=f"VIDEO:{id}"),
       ]
     ]
   )
   return await m.reply_photo(thumb,quote=True,caption=caption,reply_markup=reply_markup)

@bot.on_message(filters.command("start") & filters.private)
async def on_start(c,m):
   getDB = botdb.get("db"+token.split(":")[0])
   if m.from_user.id in getDB["banned"]:
     return await m.reply("🚫 تم حظرك من استخدام البوت",quote=True)
   if m.from_user.id == ownerID or m.from_user.id in getDB["admins"]:
     await m.reply(f"**• أهلاً بك ⌯ {m.from_user.mention}\n• إليك لوحة تحكم الادمن**",reply_markup=STARTKEY,quote=True)
   else:
     await m.reply(STARTTEXT,quote=True)
   if not m.from_user.id in getDB["users"]:
      data = getDB
      data["users"].append(m.from_user.id)
      botdb.set("db"+token.split(":")[0], data)
      for admin in data["admins"]:
         text = f"– New user stats the bot :"
         username = "@"+m.from_user.username if m.from_user.username else "None"
         text += f"\n\n𖡋 𝐔𝐒𝐄 ⌯  {username}"
         text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {m.from_user.mention}"
         text += f"\n𖡋 𝐈𝐃 ⌯  `{m.from_user.id}`"
         text += f"\n𖡋 𝐃𝐀𝐓𝐄 ⌯  **{date.today()}**"
         try: await c.send_message(admin, text, reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton (m.from_user.first_name,user_id=m.from_user.id)]]))
         except: pass
   data = {"name":m.from_user.first_name[:25], "username":m.from_user.username, "mention":m.from_user.mention(m.from_user.first_name[:25]),"id":m.from_user.id}
   botdb.set(f"USER:{m.from_user.id}",data)


@bot.on_message(filters.private & ~filters.service)
async def on_messages(c,m):   
   getDB = botdb.get("db"+token.split(":")[0])
   if m.from_user.id in getDB["banned"]:
     return await m.reply("🚫 تم حظرك من استخدام البوت",quote=True)
   if botdb.get(f"broad:{m.from_user.id}") and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      text = "**— جاري إرسال الإذاعة إلى المستخدمين**\n"
      reply = await m.reply(text,quote=True)
      count=0
      users=botdb.get("db"+token.split(":")[0])["users"]
      for user in users:
        try:
          await m.copy(user)
          count+=1
          await reply.edit(text+f"**— تم ارسال الإذاعة الى [ {count}/{len(users)} ] مستخدم**")
        except FloodWait as x:
          await asyncio.sleep(x.value)
        except Exception:
          pass
      return True

   if m.text and botdb.get(f"whois:{m.from_user.id}") and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      getUser=botdb.get(f"USER:{m.text[:15]}")
      if not getUser:
        return await m.reply("– لا يوجد مستخدم بهذا الآيدي",quote=True)
      else:
         name=getUser["name"]
         id=getUser["id"]
         mention=getUser["mention"]
         username="@"+getUser["username"] if getUser["username"] else "None"
         language=botdb.get(f"LANG:{id}")
         text = f"𖡋 𝐔𝐒𝐄 ⌯  {username}"
         text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {name}"
         text += f"\n𖡋 𝐈𝐃 ⌯  `{id}`"
         text += f"\n𖡋 𝑳𝐀𝐍𝐆 ⌯  {language}"
         text += f"\n𖡋 𝐀𝐂𝐂 𝑳𝐈𝐍𝐊 ⌯  **{mention}**"
         return await m.reply(text,quote=True)

   if m.text and botdb.get(f"ban:{m.from_user.id}") and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      getUser=botdb.get(f"USER:{m.text[:15]}")
      if not getUser:
        return await m.reply("– لا يوجد مستخدم بهذا الآيدي",quote=True)
      else:
        if getUser["id"] in botdb.get("db"+token.split(":")[0])["admins"]:
          return await m.reply(f"– لا يمكنك حظر ⌯ {getUser['mention']} ⌯ لأنه ادمن",quote=True)
        else:
          if getUser["id"] in botdb.get("db"+token.split(":")[0])["banned"]:
            return await m.reply(f"– لا يمكنك حظر ⌯ {getUser['mention']} ⌯ لأنه محظور مسبقاً",quote=True)
          name=getUser["mention"]
          id=getUser["id"]
          username="@"+getUser["username"] if getUser["username"] else "None"
          language=botdb.get(f"LANG:{id}")
          text = f"- This user added to blacklist:\n\n"
          text += f"𖡋 𝐔𝐒𝐄 ⌯  {username}"
          text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {name}"
          text += f"\n𖡋 𝑳𝐀𝐍𝐆 ⌯  {language}"
          text += f"\n𖡋 𝐈𝐃 ⌯  `{id}`"
          data = botdb.get("db"+token.split(":")[0])
          data["banned"].append(id)
          botdb.set("db"+token.split(":")[0],data)
          return await m.reply(text,quote=True)

   if m.text and botdb.get(f"unban:{m.from_user.id}") and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      getUser=botdb.get(f"USER:{m.text[:15]}")
      if not getUser:
        return await m.reply("– لا يوجد مستخدم بهذا الآيدي",quote=True)
      else:
        if getUser["id"] in botdb.get("db"+token.split(":")[0])["admins"]:
          return await m.reply(f"– لا يمكنك الغاء حظر ⌯ {getUser['mention']} ⌯ لأنه ادمن",quote=True)
        else:
          if not getUser["id"] in botdb.get("db"+token.split(":")[0])["banned"]:
            return await m.reply(f"– لا يمكنك الغاء حظر ⌯ {getUser['mention']} ⌯ لأنه غير محظور مسبقاً",quote=True)
          name=getUser["mention"]
          id=getUser["id"]
          username="@"+getUser["username"] if getUser["username"] else "None"
          language=botdb.get(f"LANG:{id}")
          text = f"- This user deleted from blacklist:\n\n"
          text += f"𖡋 𝐔𝐒𝐄 ⌯  {username}"
          text += f"\n𖡋 𝐍𝐀𝐌𝐄 ⌯  {name}"
          text += f"\n𖡋 𝑳𝐀𝐍𝐆 ⌯  {language}"
          text += f"\n𖡋 𝐈𝐃 ⌯  `{id}`"
          data = botdb.get("db"+token.split(":")[0])
          data["banned"].remove(id)
          botdb.set("db"+token.split(":")[0],data)
          return await m.reply(text,quote=True)

   if m.text and Find(m.text):
      url = Find(m.text)[0]
      if "youtu.be/" in url.lower() or "youtube.com/" in url.lower():
         return await youtube(url,m)
      return await other(url,m)
   if m.text:
      query=m.text
      keyboard= []
      results=Y88F8(query,max_results=8).to_dict()
      for res in results:
        title = res['title']
        id = res['id']
        keyboard.append([InlineKeyboardButton (title, callback_data=f'GET:{id}')])     
      return await m.reply(f'- البحث ~ {query}',reply_markup=InlineKeyboardMarkup (keyboard), disable_web_page_preview=True,quote=True)

@bot.on_callback_query(filters.regex("AUDIO"))
async def get_audii(c, query):
    await audio_down(c,query)


async def audio_down(c, query):
    rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/zddda')
     ]]
    )
    vid_id = query.data.split(":")[1]
    url = f'https://youtu.be/{vid_id}'
    await query.edit_message_caption("جاري التحميل ..", reply_markup=rep)    
    #ydl_ops = {"format": "bestaudio[ext=m4a]"}
    ydl_ops = {"format": "bestaudio[ext=m4a]",'forceduration':True}
    with YoutubeDL(ydl_ops) as ydl:
        info = ydl.extract_info(url, download=False)
        if int(info['duration']) > 3605:
          return await query.edit_message_caption("صوت اكثر من ساعة مقدر انزله",reply_markup=rep)
        audio_file = ydl.prepare_filename(info)
        ydl.process_info(info)
    await query.edit_message_caption("✈️✈️✈️✈️✈️", reply_markup=rep)
    duration= int(info['duration'])
    sec = time.strftime('%M:%S', time.gmtime(duration))
    async def progress(current, total):
       try:
         await query.edit_message_caption(f"- [ {current * 100 / total:.1f}% ]",reply_markup=rep)
       except:
         pass
    a = await query.message.reply_audio(
      audio_file,
      title=info['title'],
      duration=int(info['duration']),
      performer=info['channel'],
      caption=f'{botUsername} ~ ⏳ {sec}',
      quote=True,
      progress=progress
    )
    await query.edit_message_caption(f"{botUsername} :)", reply_markup=rep)
    await a.edit_reply_markup(
      InlineKeyboardMarkup (
        [[InlineKeyboardButton ("• مشاركة •", switch_inline_query=f"audio={a.audio.file_id}")]]
      )
    )
    os.remove(audio_file)

@bot.on_callback_query(filters.regex("VIDEO"))
async def get_video(c, query):
    await video_down(c,query)


async def video_down(c, query):
    rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/zddda')
     ]]
    )
    vid_id = query.data.split(":")[1]
    url = f'https://youtu.be/{vid_id}'
    await query.edit_message_caption("جاري التحميل ..", reply_markup=rep)    
    #ydl_ops = {"format": "bestaudio[ext=m4a]"}
    ydl_ops = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    with YoutubeDL(ydl_ops) as ydl:
        info = ydl.extract_info(url, download=False)
        if int(info['duration']) > 3605:
          return await query.edit_message_caption("فيديو اكثر من ساعة دقيقة مقدر انزله",reply_markup=rep)
    with YoutubeDL(ydl_ops) as ytdl:
        ytdl_data = ytdl.extract_info(url, download=True)
        file = ytdl.prepare_filename(ytdl_data)
    await query.edit_message_caption("✈️✈️✈️✈️✈️", reply_markup=rep)
    duration= int(info['duration'])
    sec = time.strftime('%M:%S', time.gmtime(duration))
    async def progress(current, total):
       try:
         await query.edit_message_caption(f"- [ {current * 100 / total:.1f}% ]",reply_markup=rep)
       except:
         pass
    a = await query.message.reply_video(
      file,
      duration=int(info['duration']),
      caption=f'{botUsername} ~ ⏳ {sec}',
      quote=True,
      progress=progress
    )
    await query.edit_message_caption(f"{botUsername} :)", reply_markup=rep)
    await a.edit_reply_markup(
      InlineKeyboardMarkup (
        [[InlineKeyboardButton ("• مشاركة •", switch_inline_query=f"video={a.video.file_id}")]]
      )
    )
    os.remove(file)

@bot.on_callback_query(filters.regex("GET"))
def get_info(c,query):
    Thread(target=getInfo,args=(c,query)).start()

def getInfo(c, query):
    vid_id = query.data.split("GET:")[1]
    query.message.delete()
    yt = Y88F8(f'https://youtu.be/{vid_id}',max_results=1).to_dict()[0]
    photo = yt["thumbnails"][0]
    url = f'https://youtu.be/{vid_id}'
    reply_markup=InlineKeyboardMarkup (
     [
       [
        InlineKeyboardButton ("🔊 ملف صوتي",callback_data=f"AUDIO:{vid_id}"),
        InlineKeyboardButton ("🎥 ملف فيديو",callback_data=f"VIDEO:{vid_id}"),
       ]
     ]
    )
    query.message.reply_to_message.reply_photo(
       photo,
       caption=f'{botUsername} ~ {url}',
       reply_markup=reply_markup, quote=True
    )

@bot.on_inline_query(filters.regex("^audio="))
async def share_audio(c,m):
    audio = m.query.split("audio=")[1]
    rep = InlineKeyboardMarkup (
        [[InlineKeyboardButton ("• مشاركة •", switch_inline_query=f"audio={audio}")]]
      )
    await m.answer(
      results=[
        InlineQueryResultCachedAudio(
          audio, caption=botUsername, reply_markup=rep
        )
      ],
      cache_time=60
    )
@bot.on_inline_query(filters.regex("^video="))
async def share_video(c,m):
    vid = m.query.split("video=")[1]
    rep = InlineKeyboardMarkup (
        [[InlineKeyboardButton ("• مشاركة •", switch_inline_query=f"video={vid}")]]
      )
    await m.answer(
      results=[
        InlineQueryResultCachedVideo(
          vid, title="اضغط لمشاركة الفيديو", caption=botUsername, reply_markup=rep
        )
      ],
      cache_time=60
    )

@bot.on_callback_query()
async def on_Callback(c,m):      
   if m.data == "broadcast" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      await m.edit_message_text("• أرسل الإذاعة الآن ( صورة ، نص ، ملصق ، ملف ، صوت )\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"broad:{m.from_user.id}",True)
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")

   if m.data == "whois" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      await m.edit_message_text("• ارسل الآن ايدي المستخدم للكشف عنه\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"whois:{m.from_user.id}",True)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")

   if m.data == "ban" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      await m.edit_message_text("• ارسل الآن ايدي المستخدم لحظره\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"ban:{m.from_user.id}",True)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")

   if m.data == "unban" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      await m.edit_message_text("• ارسل الآن ايدي المستخدم لرفع حظره\n• للإلغاء ارسل الغاء ",reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("رجوع",callback_data="back")]]))
      botdb.set(f"unban:{m.from_user.id}",True)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")


   if m.data == "back" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      #await m.answer("• تم الرجوع بنجاح والغاء كل شي ",show_alert=True)
      await m.edit_message_text(f"**• أهلاً بك ⌯ {m.from_user.mention}\n• إليك لوحة تحكم الادمن**",reply_markup=STARTKEY)
      botdb.delete(f"broad:{m.from_user.id}")
      botdb.delete(f"whois:{m.from_user.id}")
      botdb.delete(f"ban:{m.from_user.id}")
      botdb.delete(f"add:{m.from_user.id}")
      botdb.delete(f"rem:{m.from_user.id}")
      botdb.delete(f"unban:{m.from_user.id}")

   if m.data == "stats" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      users = len(botdb.get("db"+token.split(":")[0])["users"])
      await m.answer(f"• احصائيات البوت ⌯ {users}", show_alert=True,cache_time=10)


   if m.data == "bannedstats" and (m.from_user.id == ownerID or m.from_user.id in botdb.get("db"+token.split(":")[0])["admins"]):
      bans = botdb.get("db"+token.split(":")[0])["banned"]
      if not bans:  return await m.answer("• لا يوجد محظورين", show_alert=True,cache_time=60)
      await m.answer(f"• احصائيات المحظورين ⌯ {len(bans)}\n• سيتم ارسال بيانات كل المحظورين", show_alert=True,cache_time=60)
      text = "- المحظورين:\n\n"
      count = 1
      for banned in bans:
         if count==101: break
         getUser = botdb.get(f"USER:{banned}")
         mention=getUser["mention"]
         id=getUser["id"]
         text += f"{count}) {mention} ~ (`{id}`)\n"
         count+=1
      text+="\n\n—"
      await m.message.reply(text,quote=True)


print("ur bot started successfully")
idle()
