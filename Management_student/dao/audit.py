import datetime

def check_age(birthdate, age_min, age_max):
    today = datetime.date.today()
    birthdate=datetime.datetime.strptime(birthdate,'%Y-%m-%d')
    age = today.year - birthdate.year
    if age >= age_min and age <= age_max:
        return True
    else:
        return False