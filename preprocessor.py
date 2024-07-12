import re
import pandas as pd

def preprocess(data):
    # messages = re.split(r'\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s', data)[1:]
    # dates = re.findall(r'\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s', data)


    messages=re.split('\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[AaPp][Mm]\s-\s',data)[1:]
    # dates = re.findall(r'\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s', data)
    dates=re.findall('\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[AaPp][Mm]\s-\s',data)

    # messages=re.split('\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[AaPp][Mm]\s-\s',data)[1:]
    # dates=re.findall('\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[AaPp][Mm]\s-\s',data)

    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M %p - ')

    if messages==[] or dates==[]:

        messages=re.split(r'\[\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}:\d{2}\s[AaPp][Mm]\]\s',data)[1:]
        # dates = re.findall(r'\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s', data)
        dates=re.findall(r'\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}:\d{2}\s[AaPp][Mm]',data)
    # df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        # df2['message_date'] = pd.to_datetime(df2['message_date'], format='%d/%m/%Y, %H:%M - ')
        df['message_date']=pd.to_datetime(df['message_date'])

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)


    df['year']=df['message_date'].dt.year
    df['month']=df['message_date'].dt.month_name()
    df['day']=df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour']=df['message_date'].dt.hour
    df['minute']=df['message_date'].dt.minute
    df['month_num'] = df['message_date'].dt.month
    df['date'] = df['message_date'].dt.date

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period']=period

    return df
