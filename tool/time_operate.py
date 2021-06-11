

def time_operate(check_time):

    year = check_time.year
    month = check_time.month
    day = check_time.day
    hour = check_time.hour
    minute = check_time.min
    second = check_time.second
    check_time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(second)
    return check_time