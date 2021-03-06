from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import re
import os.path
from os import path
import sqlite3
import calendar
import schedule
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException   
import discord_webhook    
from datetime import timedelta 
#gourav:p
# LEARNIG SELENIUM
# driver= webdriver.Chrome(executable_path="./chromedriver")
# driver.set_window_size(900,900)
# driver.set_window_position(0,0)
# driver.get("https://teams.microsoft.com")
# sleep(2)
# driver.find_element_by_link_text('Enter').click()
# sleep(2)
# driver.find_element_by_id('handleOrEmail').send_keys("tourist")
# driver.find_element_by_class_name('submit').click()

def Create_DB():
	con=sqlite3.connect('my_database.db')
	c=con.cursor()
	cmd="""CREATE TABLE IF NOT EXISTS timetable(class TEXT,start_time TEXT,end_time TEXT,day TEXT)"""
	c.execute(cmd)
	con.commit()
	con.close()
	print('CREATED DATABASE')


def validate_input(regex,inp):
	if not re.match(regex,inp):
		return False
	return True

def validate_day(inp):
	days = ["monday","tuesday","wednesday","thursday","friday"]#change accordingly

	if inp.lower() in days:
		return True
	else:
		return False

#Create TimeTable
def add_timetable():
	if(not(path.exists("my_database.db"))):
			Create_DB()
	op = int(input("1. Add class\n2. Done adding\nEnter option : "))
	while(op==1):
		name = input("Enter class name : ")
		start_time = input("Enter class start time in 24 hour format: (HH:MM) ")
		while not(validate_input("\d\d:\d\d",start_time)):
			print("Invalid input, try again")
			start_time = input("Enter class start time in 24 hour format: (HH:MM) ")

		end_time = input("Enter class end time in 24 hour format: (HH:MM) ")
		while not(validate_input("\d\d:\d\d",end_time)):
			print("Invalid input, try again")
			end_time = input("Enter class end time in 24 hour format: (HH:MM) ")

		day = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")
		while not(validate_day(day.strip())):
			print("Invalid input, try again")
			end_time = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")


		conn = sqlite3.connect('my_database.db')
		c=conn.cursor()

		# Insert a row of data
		c.execute("INSERT INTO timetable VALUES (?,?,?,?)",(name,start_time,end_time,day))

		conn.commit()
		conn.close()

		print("Class added to database\n")

		op = int(input("1. Add class\n2. Done adding\nEnter option : "))



def view_timetable():
	conn = sqlite3.connect('my_database.db')
	c=conn.cursor()
	for row in c.execute('SELECT * FROM timetable'):
		print(row)
	conn.close()
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True



def joinclass(class_name,start_time,end_time):

	try_time = int(start_time.split(":")[1]) + 15
	try_time = start_time.split(":")[0] + ":" + str(try_time)

	now=datetime.now()
	cur_time=now.strftime("%H:%M")
	print(cur_time)
	if(cur_time>=start_time and cur_time<end_time):
		print("Class Joined")
		discord_webhook.send_msg(class_name=class_name,status="running",start_time=start_time,end_time=end_time)
		#now schedule leaving class
		tmp = "%H:%M"
		class_running_time = datetime.strptime(end_time,tmp) - datetime.strptime(cur_time,tmp)
		print(class_running_time)
		time.sleep(class_running_time.seconds)
		print("Class left")
		discord_webhook.send_msg(class_name=class_name,status="ended",start_time=start_time,end_time=end_time)


def sched():
	#class start time 09:00
	tmp="%H:%M"
	#cur_day
	cur_day=calendar.day_name[datetime.today().weekday()]
	if(cur_day=="Sunday" or cur_day=="Saturday"):
		print("To day is", cur_day,"no class today")
		discord_webhook.send_msg(class_name=cur_day,status="ended",start_time="No class",end_time="No class")
		cls_st="09:00"
		cur_time=datetime.now().strftime("%H:%M")
		class_running_time = datetime.strptime(cls_st,tmp) - datetime.strptime(cur_time,tmp)
		time.sleep(abs(class_running_time).total_seconds())
		sched()
	
	#connect to sql
	conn = sqlite3.connect('my_database.db')
	c=conn.cursor()
	while True:
		time.sleep(1)
		cur_time=datetime.now().strftime("%H:%M")
		print(cur_time)
		min_time='20:00'
		flg=0
		for row in c.execute('SELECT * FROM timetable where day =?',(cur_day,)):
			#schedule all classes
			name = row[0]
			start_time = row[1]
			end_time = row[2]
			day = row[3]
			print(start_time)
			if(cur_time>=start_time and cur_time<=end_time):
				joinclass(name,start_time,end_time)
				cur_time=datetime.now().strftime("%H:%M")
			if(end_time>cur_time):
				flg=1
				min_time=min(start_time,min_time)
		if(flg==0):
			print(cur_time)
			print("All classes done for today")
			break
		else:
			print(min_time)
			class_running_time = datetime.strptime(min_time,tmp) - datetime.strptime(cur_time,tmp)
			print(abs(class_running_time).total_seconds())
			time.sleep(abs(class_running_time).total_seconds())
			sched()
	
	cur_time=datetime.now().strftime("%H:%M")
	cls_st="09:00"
	class_running_time = datetime.strptime(cls_st,tmp) - datetime.strptime(cur_time,tmp)
	time.sleep(abs(class_running_time).total_seconds())
	sched()

	

			

		

		


if __name__=="__main__":
	# joinclass("Test","16:07","20:10")
	op = int(input(("1. Modify Timetable\n2. View Timetable\n3. Start Bot\nEnter option : ")))
	
	if(op==1):
		add_timetable()
	if(op==2):
		view_timetable()
	if(op==3):
		sched()

