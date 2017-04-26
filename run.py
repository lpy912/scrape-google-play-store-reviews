import json
from urllib import request, parse
from bs4 import BeautifulSoup
import sqlite3
import re
import time
import datetime
conn = sqlite3.connect('local.db')


head = '<head><link rel="stylesheet" media="screen" href="style.css"></head>'
#head= '<head><style>.current-rating{height: 10px;background-color:green; background:url(star.png)}.tiny-star.star-rating-non-editable-container{background:url(star_clean.png);width:69px}.single-review{background: #dedede;padding: 15px;margin: 15px;}</style></head>"'
#file = open("testfile.html","a") 
#file.write(str(head)) 


appid = "com.strafe.android"
app_token = "ahKDYzrwhw7Byc57NQWTzzDDv6g:1493204003886"

reviewcounter = 0

for pageNumerCounter in range(0,80):
    conditionsSetURL = 'https://play.google.com/store/getreviews'
    newConditions = {"reviewType":0, "pageNum":pageNumerCounter, "id":appid, "reviewSortOrder":4,"xhr":1,"token": app_token,"hl":"en"} 


    data = parse.urlencode(newConditions).encode()
    req =  request.Request(conditionsSetURL, data=data) # this will make the method "POST"
    resp = request.urlopen(req)

    print("Page: " + str(pageNumerCounter))
    #print(resp.read())

    cleaned = resp.read()
    #print(cleaned)
    cleaned= cleaned.decode("unicode-escape")
    #print(cleaned)

    soup = BeautifulSoup(cleaned, "html.parser")
    
    for review in soup.findAll('div',attrs={'class':'single-review'}):
        #print(review)
        if review:
            # print(review)
            reviewcounter = reviewcounter + 1
            print("Review: " + str(reviewcounter))
            score = review.find('div',attrs={'class':'current-rating'})['style']
            score = score[:-2] #remove last 2 chars
            score = score.replace("width: ", "")
            body = review.find('div',attrs={'class':'review-body'})
            body = body.text.replace("Full Review", "")
            reviewdate = review.find('span',attrs={'class':'review-date'})
            reviewdate = str(reviewdate.text)
            reviewdate = datetime.datetime.strptime(reviewdate, "%B %d, %Y")

            d = datetime.date(reviewdate.year,reviewdate.month,reviewdate.day)
            unixtime = time.mktime(d.timetuple())
            #print(body)
            c = conn.cursor()
            c.execute("INSERT INTO reviews (app_source, content, score, time_date) VALUES (?,?,?,?)", [5, str(body), score, unixtime])
            conn.commit()
            
        #file.write(str(review.encode("utf-8"))) 

conn.close()
