#importovanje potrebnih biblioteka:
import RPi.GPIO as GPIO
import time
import os
import smtplib

#dodeljivanje pinova
pin_switch = 36
pin_led_crvena = 13
pin_led_zelena = 8
pin_senzor = 7
pin_buzzer = 11

#inicijalizacija pinova
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_switch, GPIO.IN) # pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_led_crvena, GPIO.OUT)
GPIO.setup(pin_led_zelena, GPIO.OUT)
GPIO.setup(pin_senzor, GPIO.IN)
GPIO.setup(pin_buzzer, GPIO.OUT)

def senzor_pokreta():
	print("SENZOR POKRETA: "+str(GPIO.input(pin_senzor)))
	if GPIO.input(pin_senzor):
		print("POKRET DETEKTOVAN")
		GPIO.output(pin_buzzer, GPIO.HIGH) #slanje signala pistaljki
		time.sleep(1)
		GPIO.output(pin_buzzer, GPIO.LOW)
		time.sleep(1)
		fromaddr='jovana2709@gmail.com' #podaci za slanje email-a
		toaddr= 'ivicj123@gmail.com'
		msg="Alarm je detektovao pokret."
		username='jovana2709@gmail.com'
		password='tresnjica18'
		#pravimo SMTP objekat koji koristimo da se konektujemo na server:
		server = smtplib.SMTP('smtp.gmail.com:587')
		#inicira konokciju na server:
		server.ehlo()
		#enkriptovanje poruke za bezbedno slanje email-a preko interneta:
		server.starttls()
		#logovanje na server:
		server.login(username, password)
		#slanje mejla
		server.sendmail(fromaddr,toaddr,msg)
		#zavrsavamo sesiju:
		server.quit()
		print("MAIL POSLAT")

try:
	while True:
		switch_status = not bool(GPIO.input(pin_switch)) #prekidač
		print("SWITCH: "+str(switch_status))
		time.sleep(1)
		if switch_status:
		print("Alarmni sistem aktiviran")
		GPIO.output(pin_led_zelena, GPIO.HIGH) #ukljucivanje zelene diode
		GPIO.output(pin_led_crvena, GPIO.LOW) #iskljucivanje crvene diode
		senzor_pokreta() #pozivanje metode
	else:
		print("Alarmni sistem deaktiviran, cekam sekund da proverim ponovo")
		GPIO.output(pin_led_zelena, GPIO.LOW) #isklucivanje zelene diode
		GPIO.output(pin_led_crvena, GPIO.HIGH) #ukljucivanje crvene diode
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
finally:
	GPIO.cleanup() #resetovanje GPIO podesavanja