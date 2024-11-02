from utils.news_parser import get_news_analysis
import pandas as pd
import matplotlib.pyplot as plt


#date/sentiment.polarity/sentiment.subjectivity
bbc_data=[]
cnbc=[]
yahoo_data=[]

#get_news_analysis('BBC','"Nvidia"',news_data)
get_news_analysis('CNBC','Nvidia',cnbc)


#BBC Data
#df = pd.DataFrame(bbc_data, columns=['Timestamp', 'polarity', 'subjectivity'])
#df['Timestamp'] = pd.to_datetime(df['Timestamp'])
#df=df.sort_values(by='Timestamp')
#df.to_csv('BBC.csv', index=False)
#print(df)

#CNBC Data
df = pd.DataFrame(cnbc, columns=['Timestamp', 'polarity', 'subjectivity'])
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df=df.sort_values(by='Timestamp')
df.to_csv('CNBC.csv', index=False)
print(df)
