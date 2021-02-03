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
import schedule
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException   
import discord_webhook     
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
	print("Class Joined")
	discord_webhook.send_msg(class_name=class_name,status="running",start_time=start_time,end_time=end_time)
	#now schedule leaving class
	tmp = "%H:%M"
	class_running_time = datetime.strptime(end_time,tmp) - datetime.strptime(start_time,tmp)
	time.sleep(class_running_time.seconds)
	print("Class left")
	discord_webhook.send_msg(class_name=class_name,status="ended",start_time=start_time,end_time=end_time)

def sched():
	conn = sqlite3.connect('my_database.db')
	c=conn.cursor()
	for row in c.execute('SELECT * FROM timetable'):
		#schedule all classes
		name = row[0]
		start_time = row[1]
		end_time = row[2]
		day = row[3]

		if day.lower()=="monday":
			schedule.every().monday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="tuesday":
			schedule.every().tuesday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="wednesday":
			schedule.every().wednesday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="thursday":
			schedule.every().thursday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="friday":
			schedule.every().friday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="saturday":
			schedule.every().saturday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="sunday":
			schedule.every().sunday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))


	while True:
		schedule.run_pending()
		time.sleep(1)


if __name__=="__main__":
	op = int(input(("1. Modify Timetable\n2. View Timetable\n3. Start Bot\nEnter option : ")))
	
	if(op==1):
		add_timetable()
	if(op==2):
		view_timetable()
	if(op==3):
		sched()

