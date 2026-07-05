from datetime import datetime
import pytz

def get_ist_date():
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    return now_ist.strftime('%d-%m-%Y')


def is_time_expired(closing_time_str, opening_date_str):
    """
    Returns True if given time (HH:MM) is expired w.r.t current IST time,
    else False.
    """
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)

    current_date = now_ist.strftime('%d-%m-%Y').split('-')
    parsed_opening_date_str = opening_date_str.split("-")

    if int(current_date[-1]) > int(parsed_opening_date_str[-1]):
        return True
    if int(current_date[1]) > int(parsed_opening_date_str[1]):
        return True
    if int(current_date[0]) > int(parsed_opening_date_str[0]):
        return True
    
    current_time = int(now_ist.strftime('%H%M'))
    parsed_closing_time_int = int("".join(closing_time_str.split(":")))

    return current_time > parsed_closing_time_int

def get_ist_time():
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    return now_ist.strftime('%H:%M:%S')