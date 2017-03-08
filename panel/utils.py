import datetime

def validate(date_text):
    try:
    	datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
    	raise ValueError("Incorrect data format, should be DD-MM-YYYY")


