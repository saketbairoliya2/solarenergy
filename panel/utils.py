import datetime
from .models import Performance, Units
from django.db.models import Q
import logging
import simplejson as json

# Get an instance of a logger
logger = logging.getLogger(__name__)
 

def validate(date_text):
    try:
    	datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
    	raise ValueError("Incorrect data format, should be DD-MM-YYYY")

def string_json_mapper(data):
	json_dec = json.decoder.JSONDecoder()
	list_data = json_dec.decode(data)
	return list_data