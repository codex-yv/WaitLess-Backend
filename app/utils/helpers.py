from datetime import datetime
import pytz

def get_ist_date():
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    return now_ist.strftime('%d-%m-%Y')


def is_time_expired(input_time_str):
    """
    Returns True if given time (HH:MM) is expired w.r.t current IST time,
    else False.
    """
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)

    # Parse input time
    input_time = datetime.strptime(input_time_str, "%H:%M").time()

    # Combine today's date with input time in IST
    input_datetime = ist.localize(datetime.combine(now_ist.date(), input_time))

    return now_ist > input_datetime

def get_ist_time():
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    return now_ist.strftime('%H:%M:%S')