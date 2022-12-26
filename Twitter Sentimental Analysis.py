#!/usr/bin/env python
# coding: utf-8

# <h1>Library<h1>

# In[6]:


from tkinter import *
import numpy as np
import tweepy
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re


# -------------------------------------------------------------------------------------------------------------------------------

# In[7]:


root = Tk()
root.title("Twitter Sentiment Analysis (minor project)")


# <h4>Gui Size<h4>

# In[8]:


width=600
height=400

root.geometry(F"{width}x{height}")
root.minsize(width,height)
root.maxsize(width,height)


# <h4>Banner Part<h4>

# In[9]:


banner=Frame(root,padx=15,pady=14,bg="Red")
banner.pack()

heading=Label(banner,text="Twitter Sentiment Analysis",font="comicsans 20 bold")
heading.pack()


# <h4>User Input Part<h4>

# In[10]:


input_frame = Frame(root,padx=0,pady=30)
input_frame.pack(anchor="w")

input_frame1 = Frame(root,padx=0,pady=0)
input_frame1.pack()

username = Label(input_frame, text="Enter UserID without @ :- ",justify=LEFT,font="comicsansms 10 bold", padx=60)
username.grid(row=2, column=2)

user_value = StringVar()
hash_value = StringVar()

userinput = Entry(input_frame, textvariable=user_value)
userinput.grid(row=2, column=4)

blank2 = Label(input_frame, text="OR")
blank2.grid(row=3, column=4)

hashtag = Label(input_frame, text="Enter Hash Tag without # :- ",font="comicsansms 10 bold", padx=60)
hashtag.grid(row=4, column=2)

hashinput = Entry(input_frame, textvariable=hash_value)
hashinput.grid(row=4, column=4)


# <h4>Sentiment Part<h4>

# In[11]:


f1 = Frame(root,padx=15,pady=14)
f1.pack()

f2 = Frame(root,padx=15,pady=14)
f2.pack(anchor="w")
error = Label(f1, text="Please enter any one", fg="red")
error2 = Label(f1, text="Both entry not valid", fg="red")


# In[12]:


po = Label(f2, text="Positive:-",padx=15)
na = Label(f2, text="Negative:-",pady=5,padx=15)
nt = Label(f2, text="Neutral:-",padx=15)

def click():
    global positive_per
    global negative_per
    global neutral_per
    user_name = user_value.get()
    hash_name = hash_value.get()
    #################################################################
    consumerKey = "k4eGcidYdu7mOGxgoFBsT987E"
    consumerSecret = "IOTkMKO54tvYEfxzsDptbU5J67e9XIJu5ZENe8K9CDxt8BG0YI"
    accessToken = "800656855898783744-KwxRt17dgvst5gUzcv6TKUebbnrRKx4"
    accessTokenSecret = "ripEleHwDeIfuwxgTbBLDT3FvA4Dc0nbsjzr7eWRMB3xJ"
    ##################################################################
    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
    authenticate.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(authenticate, wait_on_rate_limit = True) # api object
    
    if user_name == "" and hash_name == "":
        error.grid()
    elif hash_name == "":
        error.grid_remove()
        global number
        if number > 1:
            po.grid_remove()
            na.grid_remove()
            nt.grid_remove()
        
        post = api.user_timeline(screen_name=user_name, count = 500, lang ="en", tweet_mode="extended")
        twitter = pd.DataFrame([tweet.full_text for tweet in post], columns=['Tweets'])
        def cleanTxt(text):
            text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
            text = re.sub('#', '', text) # Removing '#' hash tag
            text = re.sub('RT[\s]+', '', text) # Removing RT
            text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
            return text
        twitter['Tweets'] = twitter['Tweets'].apply(cleanTxt)
        def getSubjectivity(text):
            return TextBlob(text).sentiment.subjectivity
        def getPolarity(text):
            return TextBlob(text).sentiment.polarity
        twitter['Subjectivity'] = twitter['Tweets'].apply(getSubjectivity)
        twitter['Polarity'] = twitter['Tweets'].apply(getPolarity)
        ##########
        def getAnalysis(score):
            if score < 0:
                return 'Negative'
            elif score == 0:
                return 'Neutral'
            else:
                return 'Positive'
        ###############
        twitter['Analysis'] = twitter['Polarity'].apply(getAnalysis)
        positive = twitter.loc[twitter['Analysis'].str.contains('Positive')]
        negative = twitter.loc[twitter['Analysis'].str.contains('Negative')]
        neutral = twitter.loc[twitter['Analysis'].str.contains('Neutral')]
        
        positive_per = round((positive.shape[0]/twitter.shape[0])*100, 1)
        negative_per = round((negative.shape[0]/twitter.shape[0])*100, 1)
        neutral_per = round((neutral.shape[0]/twitter.shape[0])*100, 1)
        
        po = Label(f2, text=f"Positive:- {positive_per}%",padx=15).grid(row=1, column=8)
        na = Label(f2, text=f"Negative:- {negative_per}%",pady=5,padx=15).grid(row=2, column=8)
        nt = Label(f2, text=f"Neutral:- {neutral_per}%",padx=15).grid(row=3, column=8)
        
        number += 1
        
    elif user_name == "":
        error.grid_remove()
        if number > 1:
            po.grid_remove()
            na.grid_remove()
            nt.grid_remove()
        
        msgs = []
        msg =[]
        for tweet in tweepy.Cursor(api.search_tweets, q=hash_name).items(500):
            msg = [tweet.text] 
            msg = tuple(msg)                    
            msgs.append(msg)
        def cleanTxt(text):
            text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
            text = re.sub('#', '', text) # Removing '#' hash tag
            text = re.sub('RT[\s]+', '', text) # Removing RT
            text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
            return text
        df = pd.DataFrame(msgs)
        dfpr = Label(f2, text=f"First 5 tweets :-  \n {df.head().to_string(index=False,header=False,line_width=30)}%",padx=10).grid(row=1, column=1)
        #########################################################################################
        df['Tweets'] = df[0].apply(cleanTxt)
        df.drop(0, axis=1, inplace=True)
        def getSubjectivity(text):
            return TextBlob(text).sentiment.subjectivity
        def getPolarity(text):
            return TextBlob(text).sentiment.polarity
        df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
        df['Polarity'] = df['Tweets'].apply(getPolarity)
        def getAnalysis(score):
            if score < 0:
                return 'Negative'
            elif score == 0:
                return 'Neutral'
            else:
                return 'Positive'
        df['Analysis'] = df['Polarity'].apply(getAnalysis)
        positive = df.loc[df['Analysis'].str.contains('Positive')]
        negative = df.loc[df['Analysis'].str.contains('Negative')]
        neutral = df.loc[df['Analysis'].str.contains('Neutral')]
        
        positive_per = round((positive.shape[0]/df.shape[0])*100, 1) #p
        negative_per = round((negative.shape[0]/df.shape[0])*100, 1) #n
        neutral_per = round((neutral.shape[0]/df.shape[0])*100, 1)  #neutral
        
        po = Label(f2, text=f"Positive:- {positive_per}%",padx=15).grid(row=2, column=1)
        na = Label(f2, text=f"Negative:- {negative_per}%",pady=5,padx=15).grid(row=3, column=1)
        nt = Label(f2, text=f"Neutral:- {neutral_per}%",padx=15).grid(row=4, column=1)

        number +=1
    else:
        error2.grid()


# In[ ]:


def create_charts():
    global pie2
    global count
    if count==1:
        return None
    count=1
    figure2 = Figure(figsize=(4,3), dpi=100) 
    subplot2 = figure2.add_subplot(111) 
    labels2 = 'Positive', 'Negative', 'Neutral' 
    pieSizes = [float(positive_per),float(negative_per),float(neutral_per)]
    my_colors2 = ['lightGreen','Red','Blue']
    explode2 = (0.5, 0.3, 0.3)  
    subplot2.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=True, startangle=90) 
    subplot2.axis('equal')
    pie2 = FigureCanvasTkAgg(figure2, root)
    pie2.get_tk_widget().pack()
    
def clear_charts():
    global pie2
    global count
    count=0
    pie2.get_tk_widget().pack_forget()
count=0
number=0

button = Button(input_frame1,text="Get Analysis", command=click, fg="blue",height = 1, width = 15)
button.grid(row=1, column=1)
button1 =Button(input_frame1, text='  Show Charts  ', command=create_charts, fg='green', height=1, width = 15)
button1.grid(row=1,column=3)
button2 =Button (input_frame1, text='  Clear Charts  ', command=clear_charts, fg='Red', height=1,width=15)
button2.grid(row=1,column=5)
button3=Button(input_frame1, text ='Exit application', command=root.destroy, fg='Red', height=1,width=30)
button3.grid(row=30,column=3)
root.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




