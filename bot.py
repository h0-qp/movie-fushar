import telebot, requests
from telebot import types
from telebot.types import InlineKeyboardButton as btn
from telebot.types import InlineKeyboardMarkup as km

from user_agent import generate_user_agent, generate_navigator
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

#btns = []

@bot.message_handler(commands=['start'])
def start(message):
	id = message.from_user.id
	ms = message.text
	headers = {}
	useragent = generate_user_agent()
	headers.update({"User-Agent": useragent})
	if message.chat.type == "private":
		join = requests.get(f"https://api.telegram.org/bot1656247558:AAG9DvSqxfmrtg9ke7uZ9fwE2aqVNjwbj00/getChatMember?chat_id=-1001335124395&user_id={id}",headers=headers).text
		#headers.clear()
		if "left" in join:
			bot.reply_to(message,"""عذرا عزيزي
عليك الاشتراك في قناة البوت لتتمكن من استخدامه.
@cn_world""")
		else:
			#msg = bot.reply_to(message,".")
			bot.reply_to(message,"""مرحبا بك عزيزي في بوت الافلام
البوت يبحث عن الفيلم ويجيب كل معلوماته ورابط التحميل والمشاهدة
- البوت للافلام فقط وليس المسلسلات
طريقة الاستخدام :

ارسل اسم الفيلم فقط مع التأكد من اسمه مثال:
Fury 
او
spider man

""")
@bot.message_handler(func = lambda message:True)
def movie(message):
	id = message.from_user.id
	ms = message.text
	start_text = message.text.startswith
	useragent = generate_user_agent()
	headers = {}
	headers.update({"User-Agent": useragent})
	if message.chat.type == "private":
		join = requests.get(f"https://api.telegram.org/bot1656247558:AAG9DvSqxfmrtg9ke7uZ9fwE2aqVNjwbj00/getChatMember?chat_id=-1001335124395&user_id={id}",headers=headers).text
		if "left" in join:
			bot.reply_to(message,"""عذرا عزيزي
عليك الاشتراك في قناة البوت لتتمكن من استخدامه.
@cn_world """)
		else:
			msgs = ms.replace(".....","").replace(".......","").replace("....","").replace("A","a").replace("S","s").replace("Q","q").replace("W","w").replace("E","e").replace("R","r").replace("T","t").replace("Y","y").replace("U","u").replace("I","i").replace("O","o").replace("P","p").replace("D","d").replace("F","f").replace("G","g").replace("H","h").replace("J","j").replace("K","k").replace("L","l").replace("Z","z").replace("X","x").replace("C","c").replace("V","v").replace("B","b").replace("N","n").replace("M","m")
			bot.send_chat_action(message.chat.id, "upload_photo")
			url = requests.get(f"https://apimovie.hsynlaarqy7.repl.co/?q={msgs}",headers=headers).json()
			btns = km()
			if not url["results"]:
				return bot.reply_to(message,"اسم الفيلم خطأ او غير موجود تأكد منه.")
			try:
				title10 = url["results"][9]["title"]
				link10 = url["results"][9]["link"]
				btn10 = btn(text=title10,callback_data=link10)
				btns.add(btn10)
			except Exception as error:
				print("1",error)
			try:
				title9 = url["results"][8]["title"]
				link9 = url["results"][8]["link"]
				btn9 = btn(text=title9,callback_data=link9)
				btns.add(btn9)
			except Exception as error:
				print("2",error)
			try:
				title8 = url["results"][7]["title"]
				link8 = url["results"][7]["link"]
				btn8 = btn(text=title8,callback_data=link8)
				btns.add(btn8)
			except Exception as error:
				print("3",error)
			try:
				title7 = url["results"][6]["title"]
				link7 = url["results"][6]["link"]
				btn7 = btn(text=title7,callback_data=link7)
				btns.add(btn7)
			except Exception as error:
				print("4",error)
			try:
				title6 = url["results"][5]["title"]
				link6 = url["results"][5]["link"]
				btn6 = btn(text=title6,callback_data=link6)
				btns.add(btn6)
			except Exception as error:
				print("5",error)
			try:
				title5 = url["results"][4]["title"]
				link5 = url["results"][4]["link"]
				btn5 = btn(text=title5,callback_data=link5)
				btns.add(btn5)
			except Exception as error:
				print("6",error)
			try:
				title4 = url["results"][3]["title"]
				link4 = url["results"][3]["link"]
				btn4 = btn(text=title4,callback_data=link4)
				btns.add(btn4)
			except Exception as error:
				print("7",error)
			try:
				title3 = url["results"][2]["title"]
				link3 = url["results"][2]["link"]
				btn3 = btn(text=title3,callback_data=link3)
				btns.add(btn3)
			except Exception as error:
				print("8",error)
			try:
				title2 = url["results"][1]["title"]
				link2 = url["results"][1]["link"]
				btn2 = btn(text=title2,callback_data=link2)
				btns.add(btn2)
			except Exception as error:
				print("9",error)
			try:
				title1 = url["results"][0]["title"]
				link1 = url["results"][0]["link"]
				btn1 = btn(text=title1,callback_data=link1)
				btns.add(btn1)
			except Exception as error:
				print("10",error)
			#print(url["results"][4]["title"])
			photo = "https://t.me/myphotoj8/2"
			try:
				bot.send_photo(message.chat.id,photo,caption="نتائج بحثك أختر أحداها.",reply_to_message_id=message.message_id,reply_markup=btns)
			except:
				bot.reply_to(message,"اسم الفيلم خطأ عاود المحاولة")
			#headers=headers
@bot.callback_query_handler(func=lambda call: True)
def call(call):
	headers = {}
	if call.data:
		useragent = generate_user_agent()
		headers.update({"User-Agent": useragent})
		bot.delete_message(call.message.chat.id,call.message.message_id)
		url = requests.get(f"https://apimovie.hsynlaarqy7.repl.co/?movie={call.data}",headers=headers).json()
		#print(url)
		title = url["title"]
		photo = url["image"]
		
		links = url["links"]
		q240 = links[0]["mp4"]
		q480 = links[1]["mp4"]
		q1080 = links[2]["mp4"]
		
		info = url["information"]
		description = info["description"]
		date = info["release_date"]
		rate = info["rating"]
		my_user = "jj8jjj8"
		#headers.clear()
		
		btns = km()
		btn1 = btn(text="مشاهدة بدقة 1080p",url=q1080)
		btn2 = btn(text="مشاهدة بدقة 480p",url=q480)
		btn3 = btn(text="مشاهدة بدقة 240p",url=q240)
		echo = btn(text="المطور.",url=f"https://t.me/{my_user}")
		btns.add(btn1)
		btns.add(btn2)
		btns.add(btn3)
		btns.add(echo)
		
		msg = f"""
اسم الفيلم: {title}

التقييم: {rate}
تأريخ الاصدار: {date}

القصة: {description}

@cn_world"""
		
		bot.send_photo(call.message.chat.id,photo,caption=msg,reply_markup=btns)
		#print(q240)
bot.infinity_polling()
