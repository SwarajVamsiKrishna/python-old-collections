import pymsgbox
import beepy
import schedule
import time


def alert():

	beepy.beep(sound=2)
	but = pymsgbox.alert('Do Something','Warning',timeout=5000,button='Ok')
	
	if(but=='Ok'):
		return
	else:
		alert()
	
	
schedule.every(8).minutes.do(alert)

while True:
	schedule.run_pending()
	time.sleep(1)
	
	
