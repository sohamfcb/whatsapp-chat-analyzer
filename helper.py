from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import re
import emoji

# Initialize URL extractor
extractor = URLExtract()

def fetch_stats(selected_user, df):
    """
    Fetches statistics related to messages, words, media, and links from the DataFrame for the selected user.

    Parameters:
    - selected_user (str): The user for whom statistics are fetched. 'Overall' includes all users.
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - num_messages (int): Total number of messages for the selected user.
    - words (int): Total number of words in messages for the selected user.
    - num_media_messages (int): Total number of media messages (images, etc.) for the selected user.
    - len(links) (int): Total number of unique links shared in messages for the selected user.
    """
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        num_messages = df.shape[0]
        words = sum(len(message.split()) for message in df['message'])

        # num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
        # if num_media_messages == 0:
        num_media_messages = df[df['message'] == '\u200eimage omitted\n'].shape[0]

        links = []
        for message in df['message']:
            links.extend(extractor.find_urls(message))
        

        return num_messages, words, num_media_messages, len(set(links))

    except Exception as e:
        print(f"Error in fetch_stats: {e}")
        return 0, 0, 0, 0


def most_active_users(df):
    """
    Computes the most active users based on message count and their percentage contribution.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - x (pd.Series): Series with counts of messages per user.
    - df (pd.DataFrame): DataFrame with percentage contribution of messages per user.
    """
    try:
        x = df['user'].value_counts().head()
        df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
            columns={'index': 'name', 'user': 'percent'})
        return x, df

    except Exception as e:
        print(f"Error in most_active_users: {e}")
        return pd.Series(), pd.DataFrame()


def create_wordcloud(selected_user, df):
    """
    Creates a WordCloud based on messages for the selected user.

    Parameters:
    - selected_user (str): The user for whom the WordCloud is generated. 'Overall' includes all users.
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - wc (WordCloud): WordCloud object generated based on the messages.
    """
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        # Filter out non-relevant messages
        temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]

        # Generate WordCloud
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        df_wc = wc.generate(temp['message'].str.cat(sep=' '))

        return df_wc

    except Exception as e:
        print(f"Error in create_wordcloud: {e}")
        return None


def most_common_words(selected_user, df):
    """
    Finds the most common words used by the selected user in their messages.

    Parameters:
    - selected_user (str): The user for whom common words are identified. 'Overall' includes all users.
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - most_common_df (pd.DataFrame): DataFrame with the most common words and their frequencies.
    """
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        # Filter out non-relevant messages
        temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]

        # Define stop words to exclude from analysis
        stop_words = ['ha', 'haa', 'haan', 'na', 'naa', 'nhi', 'keno', 'kyano', 'kano', 'bhai', 'vai', 'ei', 'e', 'ki',
                      're', 'ami', 'tui', 'tumi', 'amay', 'amake', 'toke', 'amake', 'kor', 'korte', 'hobe', 'acha',
                      'accha', 'achha', 'achchha', 'khub', 'aage', 'aaj', 'aj', 'kal', 'kaal', 'kya', 'kyu', 'kyun',
                      'tu', 'tereko', 'ko', 'hi', 'se', 'to', 'toh', 'hoga', 'the', 'is', 'hai', 'of', 'you', 'hum',
                      'main', 'and', 'bhi','theke','bol','ja','ta','er','o','kore','ar','aar','eta','ota','tai','kichu','ohh','uff','sob','shob','son','shon','kichhu','abar','ebar','but','te','amar','amr','sathe','shathe','bole','hobe','hbe','tho','tor','nei','ekta','thik','hoy','hoye','jani','oi','tr','r','or','kono','tao','ache','de','ke','ache','message','deleted','bhalo','this','that','niye','de','noy','was','ekhon','akhon','gulo','<omitted>','edited>','a','image','sticker','for','on','you','your','me','my','mine','him','her','his','in','to','all','with','are','we','will','from','have','it','at','as','our','not','be','is','so','no','please','have','has','had','been','so','no','yes','if','up','can','who','by','whose','whom','an','i','also','any','&','pm','am','hello','get','us','will','cannot','vlo','valo','bhalo','here','there','their','them','k','image','omitted','<sticker>','<edited>','j','je','keu','mone','kotha','kore','korbe','kor','dekh','dakh','vai','hm','hmm','ja','dekha','<this','diye','akta','ekta','jabe','din','jaabe','eto','gulo','naki','debo','na','naa','haan','haaaa','?','ami','tui','sticker omitted','hoe','hoye','jbe','of','\n']

        # Initialize list to store words
        words = []

        # Iterate through messages to extract words
        for message in temp['message']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)

        # Create DataFrame of most common words
        most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])

        return most_common_df

    except Exception as e:
        print(f"Error in most_common_words: {e}")
        return pd.DataFrame()


def monthly_timeline(selected_user, df):
    """
    Generates a monthly timeline of messages for the selected user.

    Parameters:
    - selected_user (str): The user for whom the timeline is generated. 'Overall' includes all users.
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - timeline (pd.DataFrame): DataFrame with monthly timeline of messages.
    """
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        # Group messages by year and month to count messages
        timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

        # Create time column combining month and year
        timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)

        return timeline

    except Exception as e:
        print(f"Error in monthly_timeline: {e}")
        return pd.DataFrame()


def daily_timeline(selected_user, df):
    """
    Generates a daily timeline of messages for the selected user.

    Parameters:
    - selected_user (str): The user for whom the timeline is generated. 'Overall' includes all users.
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - daily_timeline (pd.DataFrame): DataFrame with daily timeline of messages.
    """
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        # Group messages by date to count messages
        daily_timeline = df.groupby('date').count()['message'].reset_index()

        return daily_timeline

    except Exception as e:
        print(f"Error in daily_timeline: {e}")
        return pd.DataFrame()


def week_activity_map(selected_user, df):
    """
    Generates a weekly activity map (message count per day) for the selected user.

    Parameters:
    - selected_user (str): The user for whom the activity map is generated. 'Overall' includes all users.
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - pd.Series: Series with counts of messages per day.
    """
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        # Count messages per day of the week
        return df['day_name'].value_counts()

    except Exception as e:
        print(f"Error in week_activity_map: {e}")
        return pd.Series()


def monthly_activity_map(selected_user, df):
    """
    Generates a monthly activity map (message count per month) for the selected user.

    Parameters:
    - selected_user (str): The user for whom the activity map is generated. 'Overall' includes all users.
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - pd.Series: Series with counts of messages per month.
    """
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        # Count messages per month
        return df['month'].value_counts()

    except Exception as e:
        print(f"Error in monthly_activity_map: {e}")
        return pd.Series()


def activity_heatmap(selected_user, df):
    """
    Generates an activity heatmap (message count per hour per day) for the selected user.

    Parameters:
    - selected_user (str): The user for whom the heatmap is generated. 'Overall' includes all users.
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - pd.DataFrame: DataFrame with message counts organized by hour and day.
    """
    try:
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        # Create a pivot table for message counts per hour per day
        user_heatmap = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)

        return user_heatmap

    except Exception as e:
        print(f"Error in activity_heatmap: {e}")
        return pd.DataFrame()


def emoji_analyzer(given_user, df):
    """
    Analyzes the usage of emojis by the selected user.

    Parameters:
    - given_user (str): The user for whom emoji usage is analyzed. 'Overall' includes all users.
    - df (pd.DataFrame): The DataFrame containing WhatsApp chat data.

    Returns:
    - emojis_df (pd.DataFrame): DataFrame with emojis and their counts.
    """
    try:
        if given_user != 'Overall':
            df = df[df['user'] == given_user]

        emojis = []
        emoji_pattern = re.compile(r'\p{Emoji}')

        for message in df['message']:
            emojis.extend(emoji_pattern.findall(message))

        emojis_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])

        return emojis_df

    except Exception as e:
        print(f"Error in emoji_analyzer: {e}")
        return pd.DataFrame()
