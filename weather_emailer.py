# -*- coding: utf-8 -*-
import codecs
import requests
import smtplib

def get_emails():
    emails={}
    try:
        email_file = codecs.open('emails.txt', 'r', "utf-8-sig" )
        for line in email_file:
            (email, name) = line.strip().split(',')
            emails[email] = name

    except FileNotFoundError as err:
        print(err)

    return(emails)

def get_shedule():

    try:
        schedule_file = codecs.open('schedule.txt', 'r', "utf-8-sig" )
        schedule = schedule_file.read()
    except FileNotFoundError as err:
        print(err)

    return(schedule)

def get_weather_forecast():
    # define ID key first
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Poznan,pl&units=metric&appid=' + key
    weather_request = requests.get(url)
    weather_json = weather_request.json()

    description = weather_json['weather'][0]['description'].capitalize()
    temp_min =  weather_json['main']['temp_min']
    temp_max =  weather_json['main']['temp_max']

    forecast = "Dzisiejsza pogoda w Poznaniu to: "
    forecast += description + '\nNajwyższa temeratura: ' + str(int(temp_max)) +'.'
    forecast += '\nNajniższa temperatura: ' + str(int(temp_min)) +'.'

    return forecast

def send_emails(emails, schedule, forecast):
    # Connect to SMTP server
    server = smtplib.SMTP('smtp.gmail.com', '587')

    # Start TLS encription
    server.starttls()

    # Login
    password = input("What's your password? ")
    from_email = 'sample_mail@gmail.com'
    server.login(from_email, password)

    # Send to entire email list
    for to_email, name in emails.items():
        message = 'Subject: Dzisiejsza prognoza pogody\n'
        message += 'Cześć ' + name + '!'
        message += '\n'
        message += forecast + '\n\n'
        message += schedule + '\n\n'
        message += 'Miłego dnia :)\n'

        server.sendmail(from_email, to_email, message.encode('utf-8-sig'))

    server.quit()

def main():
    emails = get_emails()
    schedule = get_shedule()

    forecast = get_weather_forecast()
    print(forecast)

    send_emails(emails, schedule, forecast)

main()