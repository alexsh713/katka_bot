import datetime
from redmine import Redmine
from auth import redmine_url, redmine_api_key, user_id
from requests.exceptions import ConnectionError

redmine = Redmine(redmine_url, key = redmine_api_key)

#dt = datetime.datetime.strptime


def get_last_note(issue):
    note_idx = []
    for note_id in issue.journals:
        note_idx.append(note_id)
    #print note_idx
    last_note = note_idx[len(note_idx)-1]
    #print last_note
    last_note_text = issue.journals.get(last_note.id)
    try:
        text = last_note_text.notes
        #print text
        return text
    except AttributeError:
        return 'no notes'
    





def show_recent_cases():
    try:
        user = redmine.user.get(user_id)
    except:
        return False
    user_issues = user.issues
    issue_list = {}
    for issue in user_issues:
        #print issue
        issue_up_time = issue.updated_on
        #td = datetime.datetime.utcnow() - dt(issue_up_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        td = datetime.datetime.utcnow() - issue_up_time
        days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60
        if days==hours==0 and minutes < 1:
            issue_list.update({str(issue.id): {str(issue.id): issue.subject, 'update': get_last_note(issue)}})
            #issue_list.update({issue.id: issue.subject})
            #issue_list.update({'notes': get_last_note(issue)})
            # issue_list.append(issue.subject)
        #print issue_list
    
    if issue_list:
        return issue_list
    else:
        return None




if __name__ == '__main__':
    print show_recent_cases()