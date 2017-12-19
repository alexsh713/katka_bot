import datetime
from redmine import Redmine
from auth import redmine_url, redmine_api_key, user_id

redmine = Redmine(redmine_url, key = redmine_api_key)

user = redmine.user.get(user_id)
user_issues = user.issues


def show_recent_cases():
    issue_list = []
    for issue in user_issues:
        #print issue
        issue_up_time = issue.updated_on
        td = datetime.datetime.utcnow() - issue_up_time
        days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60
        if days==hours==0 and minutes < 3:
            issue_list.append(issue.id)
            issue_list.append(issue.subject)
        #print issue_list
    
    if issue_list:
        return issue_list
    else:
        return None




if __name__ == '__main__':
    show_recent_cases()