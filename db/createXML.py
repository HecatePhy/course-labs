import sys
import xml.etree.ElementTree as ET 
import MySQLdb
import datetime


def get_SQL_data(user_id):
	db = MySQLdb.connect(host="localhost", user="root", passwd="", db="testForum", charset="utf8")
	cursor = db.cursor()

	sql1 = "SELECT user_name FROM users WHERE user_id = " + str(user_id)
	cursor.execute(sql1)
	user_name = cursor.fetchone()
	print(user_name)

	sql2 = "SELECT user_gender FROM users WHERE user_id = " + str(user_id)
	cursor.execute(sql2)
	user_gender = cursor.fetchone()
	print(user_gender)

	sql3 = "SELECT user_level FROM users WHERE user_id = " + str(user_id)
	cursor.execute(sql3)
	user_level = cursor.fetchone()
	print(user_level)

	sql4 = "SELECT user_birthday FROM users WHERE user_id = " + str(user_id)
	cursor.execute(sql4)
	user_birthday = cursor.fetchone()
	print(user_birthday)
	user_age = get_age(user_birthday[0])
	print(user_age)

	sql5 = "SELECT post_id FROM posts WHERE user_id = " + str(user_id)
	cursor.execute(sql5)
	post_id = cursor.fetchall()
	print(post_id)

	post_user = []
	for post in post_id:
		print(post[0])
		sql_temp = "SELECT post_id, board_id, post_title, post_time, post_clickcnt FROM posts WHERE post_id = " + str(post[0])
		cursor.execute(sql_temp)
		post_info = cursor.fetchone()
		post_user.append(post_info)
		print(post_info)
	print(post_user)

	sql6 = "SELECT reply_id FROM reply WHERE user_id = " + str(user_id)
	cursor.execute(sql6)
	reply_id = cursor.fetchall()
	print(reply_id)

	reply_user = []
	for reply in reply_id:
		print(reply[0])
		sql_temp1 = "SELECT reply_mainpostid, reply_layercnt, reply_time, reply_thumbcnt FROM reply WHERE reply_id = " + str(reply[0])
		cursor.execute(sql_temp1)
		reply_info = cursor.fetchone()
		reply_user.append(reply_info)
		print(reply_info)
	print(reply_user)

	return user_name[0], user_gender[0], user_level[0], user_birthday[0], user_age, post_user, reply_user


def wrap_into_XML(user_id):
	user_name, user_gender, user_level, user_birthday, user_age, post_user, reply_user = get_SQL_data(user_id)
	root = ET.Element("Users")
	user = ET.SubElement(root, "User")
	userName = ET.SubElement(user, "UserName")
	userName.text = user_name
	print(user_name)
	# user.attrib = {"UserName":user_name}
	userinfo = ET.SubElement(user, "Info")

	basicinfo = ET.SubElement(userinfo, "BasicInfo")
	# date_repr = reg_date.strftime("%Y-%m-%d-%H:%M:%S")
	# print(date_repr)
	# basicinfo.attrib = {"RegisterDate": date_repr}
	userGender = ET.SubElement(basicinfo, "Gender")
	userGender.text = user_gender
	print(user_gender)
	userAge = ET.SubElement(basicinfo, "Age")
	userAge.text = str(user_age)
	print(user_age)
	userLevel = ET.SubElement(basicinfo, "Level")
	userLevel.text = str(user_level)
	print(user_level)
	userBirth = ET.SubElement(basicinfo, "Birthday")
	birth_form = str(user_birthday.year) + '-' + str(user_birthday.month) + '-' + str(user_birthday.day)
	userBirth.text = birth_form
	print(birth_form)

	otherinfo = ET.SubElement(userinfo, "OtherInfo")
	postsinfo = ET.SubElement(otherinfo, "Posts")
	replyinfo = ET.SubElement(otherinfo, "Replies")
	
	tree = ET.ElementTree(root)
	docu_path = "XMLofUser" + str(user_id) + ".xml"
	print(docu_path)
	tree.write(docu_path)

	for post in post_user:
		updateTree = ET.parse(docu_path)
		root = updateTree.getroot()
		user = root.find("User")
		userinfo = user.find("Info")
		otherinfo = userinfo.find("OtherInfo")
		postsinfo = otherinfo.find("Posts")

		temp_post = ET.Element("Post")
		temp_num = ET.SubElement(temp_post, "No")
		temp_num.text = str(post[0])
		print(post[0])
		temp_block = ET.SubElement(temp_post, "Block")
		temp_block.text = str(post[1])
		print(post[1])
		temp_title = ET.SubElement(temp_post, "Title")
		temp_title.text = post[2]
		print(post[2])
		temp_time = ET.SubElement(temp_post, "Time")
		time_form = post[3].strftime("%Y-%m-%d-%H:%M:%S")
		temp_time.text = time_form
		print(time_form)
		temp_click = ET.SubElement(temp_post, "Clicks")
		temp_click.text = str(post[4])
		print(post[4])
		# temp_post.attrib = {"No": str(post[0]),"Block": str(post[1]),"Title": post[2],"Clicks": str(post[3]),"ReplyNum":str(post[4])}
		postsinfo.append(temp_post)

		updateTree.write(docu_path)

	for reply in reply_user:
		updateTree = ET.parse(docu_path)
		root = updateTree.getroot()
		user = root.find("User")
		userinfo = user.find("Info")
		otherinfo = userinfo.find("OtherInfo")
		replyinfo = otherinfo.find("Replies")

		temp_reply = ET.Element("Reply")
		temp_orinum = ET.SubElement(temp_reply, "OrignalNo")
		temp_orinum.text = str(reply[0])
		print(reply[0])
		temp_floor = ET.SubElement(temp_reply, "Floor")
		temp_floor.text = str(reply[1])
		print(reply[1])
		temp_rtime = ET.SubElement(temp_reply, "ReplyTime")
		rtime_form = reply[2].strftime("%Y-%m-%d-%H:%M:%S")
		temp_rtime.text = rtime_form
		print(rtime_form)
		temp_praise = ET.SubElement(temp_reply, "PraiseNum")
		temp_praise.text = str(reply[3])
		print(reply[3])

		replyinfo.append(temp_reply)

		updateTree.write(docu_path)


def get_age(user_birthday):
	now_time = datetime.date.today()
	now_year = now_time.year
	now_month = now_time.month
	now_date = now_time.day

	birth_year = user_birthday.year
	birth_month = user_birthday.month
	birth_date = user_birthday.day

	user_age = now_year - birth_year
	if now_month < birth_month:
		user_age -= 1
	elif now_month == birth_month:
		if now_date < birth_date:
			user_age -= 1
		else:
			pass
	else:
		pass
	return user_age


if __name__ == "__main__":
	user_id = int(input())
	wrap_into_XML(user_id)