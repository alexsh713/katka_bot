import datetime
from redmine import Redmine
from auth import *
from requests.exceptions import ConnectionError





def spent_time():
    try:
        redmine = Redmine(redmine_url, key = redmine_api_key)
    except ConnectionError:
        return False
    user = redmine.user.get(user_id)
    spent_time = user.time_entries
    total_spent_time = []


    for entry in spent_time:
        if entry.created_on.date() == datetime.date.today():
            total_spent_time.append(entry.hours)

    return sum(total_spent_time)



