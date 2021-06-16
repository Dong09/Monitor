

def time_operate_db(check_time):

    year = check_time.year
    month = check_time.month if check_time.month>=10 else str(check_time.month).zfill(2)
    day = check_time.day if check_time.day>=10 else str(check_time.day).zfill(2)
    hour = check_time.hour if check_time.hour>=10 else str(check_time.hour).zfill(2)
    minute = check_time.minute if check_time.minute>=10 else str(check_time.minute).zfill(2)
    # second = check_time.second
    check_time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) 
    # + ':' + str(minute) 
    return check_time


def time_operate_poor(check_time):

    year = check_time.year
    month = check_time.month if check_time.month>=10 else str(check_time.month).zfill(2)
    day = check_time.day if check_time.day>=10 else str(check_time.day).zfill(2)
    hour = check_time.hour if check_time.hour>=10 else str(check_time.hour).zfill(2)
    minute = check_time.minute if check_time.minute>=10 else str(check_time.minute).zfill(2)
    second = check_time.second if check_time.second>=10 else str(check_time.second).zfill(2)

    check_time = str(year)+ str(month) + str(day) + str(hour) + str(minute) +str(second)
    return check_time




if __name__ == '__main__':
    import datetime
    check_time = datetime.datetime.now()
    check_time = time_operate_poor(check_time)
    print(check_time)