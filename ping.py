#Ping Function
#Pings API and gathers information and brings it back 

#important packages to import
import requests
import csv
from datetime import *

#test dates: 2022-03-01 -> 2022-03-31

#func is an integer that will represent what type of function is being called
#symbol is a string for the stock symbol we are looking for
#lowerDateStr is the string for the start date
#upperDateStr is the string for end date
def pingAPI(func, symbol, lowerDate, upperDate):
#MUQCQXXUYY3U4KUE -> my API key
    #the if statement will pick a URL based on what the func is. The only thing changing in each URL is the "function" parameter
    if(func == 1):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=30min&apikey=MUQCQXXUYY3U4KUE&datatype=csv".format(symbol)
        #This is how you change the date strings into a date time object
        #FUNCTION 1 NEEDS A TIME TO WORK THE OTHERS CANNOT HAVE A TIME
        # lowerDate = datetime.strptime(lowerDateStr, "%Y-%m-%d %H:%M:%S") 
        # upperDate = datetime.strptime(upperDateStr, "%Y-%m-%d %H:%M:%S")
    elif(func == 2):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey=MUQCQXXUYY3U4KUE&datatype=csv".format(symbol)
        # lowerDate = datetime.strptime(lowerDateStr, "%Y-%m-%d")
        # upperDate = datetime.strptime(upperDateStr, "%Y-%m-%d")
    elif(func == 3):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={}&apikey=MUQCQXXUYY3U4KUE&datatype=csv".format(symbol)
        # lowerDate = datetime.strptime(lowerDateStr, "%Y-%m-%d")
        # upperDate = datetime.strptime(upperDateStr, "%Y-%m-%d")
    elif(func == 4):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={}&apikey=MUQCQXXUYY3U4KUE&datatype=csv".format(symbol)
        # lowerDate = datetime.strptime(lowerDateStr, "%Y-%m-%d")
        # upperDate = datetime.strptime(upperDateStr, "%Y-%m-%d")

    #getting the info form the API and turns into a CSV file
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        results = list(cr)
        data = [] 
        for row in results:
            #skips the header
            if(row[0] == "timestamp"):
                data.append(row)
                continue
            if(func == 1): #if the function is 1 we need a time as well
                try:
                    apiDate = datetime.stroptime(row[0], "%Y-%m-%d")
                except:
                    continue
            else:
                try:
                    apiDate = datetime.strptime(row[0], "%Y-%m-%d")
                except:
                    continue
            #compares the current date to make sure it is within our bounds
            if(apiDate >= lowerDate and apiDate <= upperDate):
                data.append(row)
    
    return data