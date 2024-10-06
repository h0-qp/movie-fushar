import telebot, requests,re
from telebot import types
from telebot.types import InlineKeyboardButton as btn
from telebot.types import InlineKeyboardMarkup as km
#from config import movie_token
from user_agent import generate_user_agent, generate_navigator

def search(name):
	db = {}
	movies = []
	results = True
	try:
		headers = {"user-agent": generate_user_agent()}
		info = requests.get(f"https://www.fushaar.com?s={name.replace(' ','+')}",headers=headers).text
		#print(info)
		title = re.findall('<a title=”(.*?)” href="(.*?)">',info)
		image = re.findall('class="card_content" style="background: url(.*?) no-repeat left bottom;',info)
		year = re.findall('class="year">(.*?)</li>',info)
		imdb = re.findall('</noscript> (.*?) </span>',info)
		genre = re.findall('itemprop="genre" href="(.*?)">(.*?)</a>',info)
		for i in range(len(title)):
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
		title = re.findall('<meta property="og:title" content="(.*?)" />',res)[0].replace("مشاهدة","").replace("وتحميل","").replace("فيلم","").replace("مجانا","").replace("  ","")
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

try:
	open("members_movies.txt","r")
except:
	open("members_movies.txt","a").write("1160471152\n")

bot = telebot.TeleBot("2085301389:AAFoXf1NqaiqUnew_bFRhEFHGHNVN0PjbWY")
# 5578804926:AAGNxODMKLiLy94OwkTyljGLXfYxk_CucvQ
#btns = []

@bot.message_handler(commands=['start'])
def start(message):
	id = message.from_user.id
	name = message.from_user.first_name
	username = message.from_user.username
	mention = "["+name+"](tg://user?id="+str(id)+")"
	users = [int(u) for u in open("members_movies.txt","r").readlines()]
	if not id in users:
		open("members_movies.txt","a").write(f"{id}\n")
		count = len(open("members_movies.txt","r").readlines())
		bot.send_message(1160471152,
		f"دخل شخص جديد للبوت: اسمه {name}\nايديه {id}\n يوزره @{username}\n عدد الاعضاء اصبح {count}")
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
			#bot.edit_message_text("..",message.chat.id,msg.message_id)
			#bot.edit_message_text("...",message.chat.id,msg.message_id)
			bot.reply_to(message,"""مرحبا بك عزيزي في بوت الافلام
البوت يبحث عن الفيلم ويجيب كل معلوماته ورابط التحميل والمشاهدة
- البوت للافلام فقط وليس المسلسلات
طريقة الاستخدام :

ارسل اسم الفيلم فقط مع التأكد من اسمه مثال:
Fury 
او
spider man

""")

@bot.message_handler(commands=["database"])
def database(message):
	id = message.from_user.id
	if id != 1160471152: return
	file = open("members_movies.txt","rb")
	num = len(open("members_movies.txt","r").readlines())
	bot.send_document(id,file,caption=f"Memebers: {num}")
@bot.message_handler(func = lambda message:True)
def movie(message):
	id = message.from_user.id
	ms = message.text
	start_text = message.text.startswith
	useragent = generate_user_agent()
	headers = {}
	old_message = bot.reply_to(message,"جاري البحث عن الفيلم...")
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
			ten = 10
			if not url["results"] or len(url["movies"]) < 1:
				return bot.edit_message_text("اسم الفيلم خطأ او غير موجود تأكد منه.",message.chat.id,old_message.message_id)
			for i in range(len(url["movies"])):
				if i >= 10:
					break
				
				title = url["movies"][i]["title"]
				link = url["movies"][i]["link"].replace("https://www.fushaar.com/movie/","")
				btns.add(btn(text=title,callback_data=link))
			photo = "https://telegra.ph/file/d2b379fb1b05cfdff2e60.jpg"
			bot.delete_message(message.chat.id,old_message.message_id)
			try:
				bot.send_photo(message.chat.id,photo,caption="نتائج بحثك أختر أحداها.",reply_to_message_id=message.message_id,reply_markup=btns)
			except Exception as error:
				#print(title,link)
				print(error)
				bot.reply_to(message,"اسم الفيلم خطأ عاود المحاولة")
			#headers=headers

@bot.callback_query_handler(func=lambda call: True)
def call(call):
	headers = {}
	if call.data:
		useragent = generate_user_agent()
		headers.update({"User-Agent": useragent})
		bot.delete_message(call.message.chat.id,call.message.message_id)
		url = getMovie("https://www.fushaar.com/movie/"+call.data)
		title = url["title"]
		photo = url["image"]
		
		links = url["links"]
		try:
			q240 = links[0]
			q480 = links[1]
			q1080 = links[2]
		except:
			q240 = "لا يوجد"
			q480 = "لا يوجد"
			q1080 = "لا يوجد"
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
		if (q240 and q480 and q1080) == "لا يوجد":
			btn1 = btn(text="لا يوجد رابط مشاهدة",url="https://t.me/cn_world")
			btn2 = btn(text="لا يوجد رابط مشاهدة",url="https://t.me/cn_world")
			btn3 = btn(text="لا يوجد رابط مشاهدة",url="https://t.me/cn_world")
		else:
			# WebApp #
			viewr = "https://h0-qp.github.io/StreamVideo?video="
			q1080 = types.WebAppInfo(viewr+q1080)
			q480 = types.WebAppInfo(viewr+q480)
			q240 = types.WebAppInfo(viewr+q240)
			#########
			
			btn1 = btn(text="مشاهدة بدقة 1080p",web_app=q1080)
			btn2 = btn(text="مشاهدة بدقة 480p",web_app=q480)
			btn3 = btn(text="مشاهدة بدقة 240p",web_app=q240)
		echo = btn(text="المطور.",url=f"https://t.me/{my_user}")
		btns.add(btn1)
		btns.add(btn2)
		btns.add(btn3)
		btns.add(echo)
		
		msg = f"""
🎥 اسم الفيلم: <strong>{title}</strong>

⭐ التقييم: {rate}
🗓 تأريخ الاصدار:  {date}
⏱ المدة: {runtime}
🖼 التصنيف: {genre}

القصة: {description}

@cn_world"""
		
		bot.send_photo(call.message.chat.id,photo,caption=msg,reply_markup=btns,parse_mode="html")
		#print(q240)
bot.infinity_polling()