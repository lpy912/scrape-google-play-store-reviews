import json
from urllib import request, parse
from bs4 import BeautifulSoup


head = '<head><link rel="stylesheet" media="screen" href="style.css"></head>'
#head= '<head><style>.current-rating{height: 10px;background-color:green; background:url(star.png)}.tiny-star.star-rating-non-editable-container{background:url(star_clean.png);width:69px}.single-review{background: #dedede;padding: 15px;margin: 15px;}</style></head>"'
file = open("testfile.html","a") 
file.write(str(head)) 
for pageNumerCounter in range(0,50):
    conditionsSetURL = 'https://play.google.com/store/getreviews'
    newConditions = {"reviewType":0, "pageNum":pageNumerCounter, "id":"com.mobilesrepublic.appygamer", "reviewSortOrder":4,"xhr":1,"token":"EVBGc4h1YKT2ctafDdTtyGveTmI:1492760927435","hl":"en"} 


    data = parse.urlencode(newConditions).encode()
    req =  request.Request(conditionsSetURL, data=data) # this will make the method "POST"
    resp = request.urlopen(req)

    #print(resp.read())

    cleaned = resp.read()
    #print(cleaned)
    cleaned= cleaned.decode("unicode-escape")
    #print(cleaned)

    soup = BeautifulSoup(cleaned, "html.parser")

    
    
    for review in soup.findAll('div',attrs={'class':'single-review'}):
        #print(review)

        
        file.write(str(review.encode("utf-8"))) 

file.close() 
