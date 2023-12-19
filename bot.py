import telebot, requests,re
from telebot import types
from telebot.types import InlineKeyboardButton as btn
from telebot.types import InlineKeyboardMarkup as km

from user_agent import generate_user_agent, generate_navigator
from config import TOKEM

bot = telebot.TeleBot(TOKEN)

def search(name):
	db = {}
	movies = []
	results = True
	try:
		headers = {"user-agent": generate_user_agent()}
		info = requests.get(f"https://www.fushaar.info?s={name}",headers=headers).text
		title = re.findall('<a title=”(.*?)” href="(.*?)">',info)
		image = re.findall('class="card_content" style="background: url(.*?) no-repeat left bottom;',info)
		year = re.findall('class="year">(.*?)</li>',info)
		imdb = re.findall('</noscript> (.*?) </span>',info)
		genre = re.findall('itemprop="genre" href="(.*?)">(.*?)</a>',info)
		for i in range(len(year)):
			result = {
				"title": title[i][0].replace("مشاهدة","").replace("مشاهده","").replace("فلم","").replace("فيلم","").replace("تحميل","").replace("وتحميل","").replace("اونلاين","").replace("شاهد","").replace("مشاهد","").replace(" و ",""),
				"genre": genre[i][1],
				"imdb": imdb[i][0],
				"image": image[i],
				"link": title[i][1].replace("مشاهدة","").replace("مشاهده","").replace("فلم","").replace("فيلم","").replace("تحميل","").replace("وتحميل","").replace("اونلاين","").replace("شاهد","").replace("مشاهد","").replace(" و ","")
			}
			movies.append(result)
		db["results"] = results
		db["movies"] = movies
		db["By"] = "Hussein ~ @jj8jjj8"
		return db
	except Exception as error:
		print(error)
		reults = False
		db["results"] = results
		return db
def getMovie(url):
	db = {}
	headers = {"user-agent": generate_user_agent()}
	results = True
	try:
		res = requests.get(url,headers).text
		title = re.findall('<meta property="og:title" content="(.*?)" />',res)[0]
		description = re.findall('<meta property="og:description" content="(.*?)/>',res)[0]
		image = re.findall('<meta property="og:image" content="(.*?)" />',res)[0]
		year = re.findall('<span class="yearz">(.*?)</span>',res)[0]
		genre = re.findall('<div class="gerne"><a itemprop="genre"(.*?)</div>',res)[0]
		genre = "".join(gen+", " for gen in re.findall('>(.*?)</a>',genre))
		rating = re.findall('<div class="imdbratebox">(.*?)</div>',res)[0]
		pp = re.findall('<div class="info-boxy">(.*?)<span',res)
		runtime = pp[0]+" دقيقة."
		quality = pp[2]
		links = [g for g in re.findall('<a class="watch-hd" href="(.*?)" target="_blank"',res) if ".mp4" in g]
		db = {
			"results": results,
			"title": title,
			"description": description,
			"image": image,
			"year": year,
			"genre": genre,
			"rating": rating,
			"runtime": runtime,
			"quality": quality,
			"links": links
		}
		return db
	except Exception as error:
		print(error)
		results = False
		db["results"] = results
		return db

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
			msg = bot.reply_to(message,".")
			bot.edit_message_text("..",message.chat.id,msg.message_id)
			bot.edit_message_text("...",message.chat.id,msg.message_id)
			bot.edit_message_text("""مرحبا بك عزيزي في بوت الافلام
البوت يبحث عن الفيلم ويجيب كل معلوماته ورابط التحميل والمشاهدة
- البوت للافلام فقط وليس المسلسلات
طريقة الاستخدام :

ارسل اسم الفيلم فقط مع التأكد من اسمه مثال:
Fury 
او
spider man

""",message.chat.id,msg.message_id)
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
			url = search(msgs)
			btns = km()
			if not url["results"] or len(url["movies"]) < 1:
				return bot.reply_to(message,"اسم الفيلم خطأ او غير موجود تأكد منه.")
			try:
				title10 = url["movies"][9]["title"]
				link10 = url["moives"][9]["link"]
				btn10 = btn(text=title10,callback_data=link10)
				btns.add(btn10)
			except Exception as error:
				print("1",error)
			try:
				title9 = url["movies"][8]["title"]
				link9 = url["movies"][8]["link"]
				btn9 = btn(text=title9,callback_data=link9)
				btns.add(btn9)
			except Exception as error:
				print("2",error)
			try:
				title8 = url["movies"][7]["title"]
				link8 = url["movies"][7]["link"]
				btn8 = btn(text=title8,callback_data=link8)
				btns.add(btn8)
			except Exception as error:
				print("3",error)
			try:
				title7 = url["movies"][6]["title"]
				link7 = url["movies"][6]["link"]
				btn7 = btn(text=title7,callback_data=link7)
				btns.add(btn7)
			except Exception as error:
				print("4",error)
			try:
				title6 = url["movies"][5]["title"]
				link6 = url["movies"][5]["link"]
				btn6 = btn(text=title6,callback_data=link6)
				btns.add(btn6)
			except Exception as error:
				print("5",error)
			try:
				title5 = url["movies"][4]["title"]
				link5 = url["movies"][4]["link"]
				btn5 = btn(text=title5,callback_data=link5)
				btns.add(btn5)
			except Exception as error:
				print("6",error)
			try:
				title4 = url["movies"][3]["title"]
				link4 = url["movies"][3]["link"]
				btn4 = btn(text=title4,callback_data=link4)
				btns.add(btn4)
			except Exception as error:
				print("7",error)
			try:
				title3 = url["movies"][2]["title"]
				link3 = url["movies"][2]["link"]
				btn3 = btn(text=title3,callback_data=link3)
				btns.add(btn3)
			except Exception as error:
				print("8",error)
			try:
				title2 = url["movies"][1]["title"]
				link2 = url["movies"][1]["link"]
				btn2 = btn(text=title2,callback_data=link2)
				btns.add(btn2)
			except Exception as error:
				print("9",error)
			try:
				title1 = url["movies"][0]["title"]
				link1 = url["movies"][0]["link"]
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
		url = getMovie(call.data)
		print(url)
		title = url["title"]
		photo = url["image"]
		
		links = url["links"]
		q240 = links[0]
		q480 = links[1]
		q1080 = links[2]
		
		#info = url["information"]
		description = url["description"]
		date = url["year"]
		rate = url["rating"]
		runtime = url["runtime"]
		genre = url["genre"]
		quality = url["quality"]
		
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
المدة: {runtime}
التصنيف: {genre}

القصة: {description}

@cn_world"""
		
		bot.send_photo(call.message.chat.id,photo,caption=msg,reply_markup=btns)
		#print(q240)
bot.infinity_polling()