
# print(os.path.dirname(sys.executable))


from youtube_transcript_api import YouTubeTranscriptApi


import os,sys



from time import sleep


from random import random


# HLPER FUNCTION: Get Time Now:
from datetime import datetime
def time_now():
    '''Get Current Time'''
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    return now


import pandas as pd


import regex as re





#!{sys.executable} -m pip install selenium 


print('Check Selenium Webdriver path exists in the current directory:')
if 'chromedriver.exe' in os.listdir():
    driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
    driver_path = driver_path.replace('\\', '/')
    if os.path.exists(driver_path):
        print('OK!')
    else:
        print('Something is wrong; Chrome Selenium Webdriver doesn\'t exists!')
        sys.exit()
else:
    print('You must enter valid path for Selenium Chrome driver!')
    driver_path = input('Chrome Driver Path: ')
    driver_path = driver_path.replace('\\', '/')
    if os.path.exists(driver_path):
          print('OK, you entered valid path.')
    else:
        print('Something is wrong; Chrome Selenium Webdriver doesn\'t exists!')
        sys.exit()





from itertools import chain
from collections import Counter


from time import sleep


#imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


from selenium.webdriver.chrome.options import Options


from selenium.webdriver.common.keys import Keys


numb_vids = input('Please enter the number of videos in the YouTube channel:')
numb_vids = int(numb_vids)


chrome_options = Options()


chrome_options.add_argument('--headless')
chrome_options.add_argument("--start-maximized")


print('Please Enter the YouTube channel URL: ')
link = input('YouTube URL Channel: ')
# link = 'https://www.youtube.com/c/TechLead/videos'


############
print('Starting...')
start = time_now()
############


#1 opening chrome window
driver = webdriver.Chrome(driver_path, options=chrome_options)


driver.implicitly_wait(10)


#2 go to url
driver.get(link)


container_xpath = '//ytd-grid-renderer[@class="style-scope ytd-item-section-renderer"]' # OK
video_xpath = './/ytd-grid-video-renderer[@class="style-scope ytd-grid-renderer"]' # Notice it's relative! >> First Suspect when script crashes.
title_xpath = './/h3[@class="style-scope ytd-grid-video-renderer"]/a[@id="video-title"]'
link_xpath = './/h3[@class="style-scope ytd-grid-video-renderer"]/a'
duration_xpath = './/h3[@class="style-scope ytd-grid-video-renderer"]/a'
channel_name_xpath = '//div[@id="channel-header"]//yt-formatted-string[@id="text"]'




numb_scrolls = int(round((numb_vids/25), 0))


print(f'Number of videos to be scraped: {numb_vids}')
print(f'Number of scrolls: {numb_scrolls}')
if (numb_scrolls*10) <= 60:
    print(f'Approximate time it will take: {(numb_scrolls*10)} seconds')
else:
    print(f'Approximate time it will take: {(numb_scrolls*10)/60} minutes')


print(f'\t>>>\tThe number of videos to be scraped: {numb_vids} videos')
set_videos = set()
vid_container = driver.find_elements_by_xpath(container_xpath)
channel_name = driver.find_element_by_xpath(channel_name_xpath).text
channel_name = re.sub(r'\s+', '_', channel_name)
os.mkdir(channel_name)

for n in range(numb_scrolls):
    driver.find_element_by_xpath('//body').send_keys(Keys.END)
    sleep(4)
for video_thumb in vid_container:
    if len(set_videos)<= numb_vids:
        video_n = video_thumb.find_elements_by_xpath(video_xpath)
        for vid in video_n:
            video_title = vid.find_element_by_xpath(title_xpath).text
            video_link = vid.find_element_by_xpath(link_xpath).get_attribute('href')
            video_duration = vid.find_element_by_xpath(duration_xpath).get_attribute('aria-label')
            video_details = video_title, video_link, video_duration
            set_videos.add(video_details)

print(f'Number of input videos = {numb_vids}')
print(f'Number of scraped video urls = {len(set_videos)}')


driver.quit() # ALWAYS CLOSE DRIVER AFTER FINISHING! IT RUNS IN THE BACKGROUND!


############
print('Finished...')
end = time_now()
############
duration = end - start
duration_min = round(duration.seconds/60, 3)
if duration_min < 2:
    time_unit = 'minute'
else:
    time_unit = 'minutes'
print(f'Number of videos scraped {len(set_videos)}')
print(f'Total duration of scraping is {duration_min} {time_unit}.')


list_videos = list(set_videos)


df01 = pd.DataFrame(data={
    'TITLE': [i[0] for i in list_videos],
    'LINK': [i[1] for i in list_videos],
    'DURATION': [i[2] for i in list_videos]
})



def get_views_number(x):
    duration = x.split(' ago ')[1]
    pat_views = r'[\d\s,]+views'
    duration = re.findall(pat_views, duration)
    return duration[0]


def get_duration(x):
    duration = x.split(' ago ')[1]
    pat_views = r'[\d\s,]+views'
    duration = re.split(pat_views, duration)
    return duration[0]


df01['VID_LEN'] = df01['DURATION'].apply(get_duration)


df01['VID_VIEWS'] = df01['DURATION'].apply(get_views_number)


df01['VID_VIEWS'] = df01['VID_VIEWS'].apply(lambda x: int(''.join([i for i in x if i.isnumeric()])))





def calculate_duration_seconds(x):
    '''Given a string that may contains hours, minutes or seconds;
    Give the true duration in minutes.'''
    
    if 'hour' in x:
        hours = re.search(r'\d\s(?=(hour))', x)
        hours = hours.group().strip()
        hours = int(hours) * 60
    else:
        hours = 0
    
    if 'minute' in x:
        minutes = re.search(r'\d+\s(?=(minute))', x)
        minutes =  minutes.group().strip()
        minutes = int(minutes)
    else:
        minutes = 0
    
    if 'second' in x:
        seconds = re.search(r'\d+\s(?=(second))', x)
        seconds = seconds.group().strip()
        seconds = int(seconds) / 60
    else:
        seconds = 0
    total_duration = round((hours + minutes + seconds), 2)
    return total_duration


df01['LEN_MIN'] = df01['VID_LEN'].apply(calculate_duration_seconds)


#df01.to_pickle('YT_CH_VID_TECHLEADSHOW_STAGE_01.pkl', protocol=4)


df01['VID_ID'] = df01['LINK'].apply(lambda x :re.sub(r'https://www\.youtube\.com/watch\?v=', '', x))





def save_df_pickle(df, name_url_pickle_file):
    '''
    Given a pandas dataframe; save it with a given name.
    '''
    counter = 0
    if f'{name_url_pickle_file}.pkl' not in os.listdir():
        df.to_pickle(f'{name_url_pickle_file}.pkl', protocol=4)
        print(f'YouTube Video Links were saved to {name_url_pickle_file}.pkl in the current directory.')
    else:
        counter += 1
        pad = str(counter).zfill(2)
        df.to_pickle(f'{name_url_pickle_file}_copy_{pad}.pkl', protocol=4)
        print(f'YouTube Video Links were saved to {name_url_pickle_file}_copy{pad}.pkl in the current directory.')


save_df_pickle(df01, 'youtube_urls')


youtube_vid_ids = list(zip(df01['TITLE'], df01['LINK'], df01['VID_ID']))


def get_english_subs(x_list):
    '''Given a list of video_ids; get auto-generated subtitles using a YouTube api'''
    failed_list = []
    success_list = []
    print(f'Extracting cc will take at least {(len(x_list)*3)/60} minutes.')
    for vid in x_list:
        vid_id = vid[2]
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(vid_id)
            tra = transcript_list.find_transcript(['en'])
            subs = tra.fetch()
            success_list.append((vid_id, subs)) # modified
            sleep(3)

        except:
            failed_list.append(vid)
    if len(failed_list) > 0:
        print('_'*50)
        print(f'{len(failed_list)} transcripts out of {numb_vids} couldn\'t be extracted')
        print('This could be because auto-generated cc wasn\'t enabled,\nOr English couldn\'t be recognized as the language of the video.')
        print('\n')
        print('The following videos couldn\'t be processed:')
        for i in failed_list:
            print(i)
            print('*'*50)
    else:
        print('All videos transcripts were extracted')
    
    print('\n')
    print(f'Only {len(success_list)} transcirpts were extracted.')
    return success_list


list_cc = get_english_subs(youtube_vid_ids)


dict_vid_id_title = dict(df01['VID_ID TITLE'.split()].values.tolist())
dict_vid_id_link = dict(df01['VID_ID LINK'.split()].values.tolist())


new_cc = []
counter = 1
for i in list_cc:
    new_cc.append((counter,i)) # modified
    counter +=1


df_subs = pd.DataFrame(data={'ID': [i[0] for i in new_cc],
                  'DUMMY': [i for i in new_cc]}) # modified


df_subs['VID_ID'] = df_subs['DUMMY'].apply(lambda x: x[1])
df_subs['VID_ID'] = df_subs['VID_ID'].apply(lambda x: x[0])

df_subs['LINK'] = df_subs['VID_ID'].apply(lambda x: dict_vid_id_link[x])
df_subs['TITLE'] = df_subs['VID_ID'].apply(lambda x: dict_vid_id_title[x])

df_subs['DUMMY_2'] = df_subs['DUMMY'].apply(lambda x: x[1])
df_subs['DUMMY_2'] = df_subs['DUMMY_2'].apply(lambda x: x[1])

df_subs = df_subs.explode('DUMMY_2').reset_index(drop=True)
df_subs['TEXT'] = df_subs['DUMMY_2'].apply(lambda x: x['text'])
df_subs['START'] = df_subs['DUMMY_2'].apply(lambda x: x['start'])
df_subs['DURATION'] = df_subs['DUMMY_2'].apply(lambda x: x['duration'])

df_subs = df_subs['ID	TEXT	START	DURATION LINK TITLE VID_ID'.split()]

df_subs['MINUTE'] = df_subs['START'].apply(lambda x: int(x/60))


grp_df_subs = df_subs.groupby(['ID', 'MINUTE', 'LINK', 'TITLE']).agg({'TEXT': lambda x: ' '.join(x)})


grp_df_subs = grp_df_subs.reset_index()


# CREATE A FUNCTION THAT SAVES A PANDAS DATAFRAME! This is double work!
save_df_pickle(grp_df_subs, f'{channel_name}_TRANSCRIPTS')
print('_'*50)
print(f'Save images & excel files to the following folder: {channel_name}')