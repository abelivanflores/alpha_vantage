import alpha_vantage
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
import pandas
import mysql.connector
import numpy
import requests

db = mysql.connector.connect(
    host="cis3368-db-abelflores.cb6hsg0d78b1.us-east-1.rds.amazonaws.com",
    user="admin",
    passwd="admin123" #DB is closed, you can use your own db and insert credentials here
)
mycursor=db.cursor()

API_key = '' #API Key Generated from Alpha Vantage, place your key here

ts = TimeSeries(key = API_key,output_format='pandas') # reviewed basic How To Use Alpha Vantage API Python video https://www.youtube.com/watch?v=PytQROAncxg, this allows us to use 'TS' to call TimeSeries function
ce = CryptoCurrencies(key = API_key,output_format='pandas') #this allows us to call information on Crypto Currency

#we are setting this variable to 1 to prepare for our while loop
x = 1
#created a function to showcase a menu for our loop function
#https://extr3metech.wordpress.com/2014/09/14/simple-text-menu-in-python/ used this resource to create menu
def print_menu():
    print ("MAIN MENU")
    print ("****************")       
    print ("a. View Daily Adjusted Stock Information")
    print ("b. View Monthly Adjusted Stock Information")
    print ("c. View Daily Adjusted Crypto Overview")
    print ("d. View Exchange Rate of Crypto to USD")
    print ("e. View Fundamental Crypto Asset Score")
    print ("f. Save Fundamental Crypto Asset Score Results in DB") 
    print ("g. View Fundamnetal Crypto Asset Score Saved Results")
    print ("h. View Fundamnetal Crypto Asset Score Saved Results FROM BEST TO WORST")
    print ("i. Delete Fundamnetal Crypto Asset Score Data IF Utility Score is less than 800 ") #This should delete XRP from our DB
    print ("j. Exit Program")
    print ("****************\n")
    
  
#while loop will be needed for the main menu code below
while x == 1:          ## While loop which will keep going until x = 2
    print('\n')
    print_menu()    ## Displays menu
    userInput = input('What would you like to do?\n')
    if userInput == 'a':
        stock_name = input("What is the stock's Acronym?: \n") 
        print ("***********************")
        print ("DAILY STOCK INFORMATION") #the code to the left is to better present and title the data retrieved
        print ("***********************")
        print('\n')
        print(ts.get_daily_adjusted(stock_name))                #this code will print the daily adjusted results requested by the user to the stock of their input     
        print('Daily Results from '+ stock_name + ' shown!')    #this code will serve as a confirmation of what stock they selected 
    elif userInput == 'b':
        stock_name = input("What is the stock's Acronym?: \n")
        print ("***********************")
        print ("MONTHLY STOCK INFORMATION") #the code to the left is to better present and title the data retrieved
        print ("***********************")
        print('\n')
        print(ts.get_monthly_adjusted(stock_name))              #this code will print the daily adjusted results requested by the user to the stock of their input
        print('Monthly Results from '+ stock_name + ' shown!')  #this code will serve as a confirmation of what stock they selected
    elif userInput == 'c':
        crypto_name = input("What is the crypto's Acronym?: \n")
        print ("************************")
        print ("DAILY CRYPTO INFORMATION") #the code to the left is to better present and title the data retrieved
        print ("************************")
        print(ce.get_digital_currency_daily(crypto_name,"USD"))             #this code will print the ________ requested by the user to the crypto of their input
        print('Daily Results from '+ crypto_name + ' shown!')   #this code will serve as a confirmation of what crypto they selected
    elif userInput == 'd':
        crypto_name = input("What is the crypto's Acronym?: \n")
        print ("************************")
        print ("CRYPTO TO USD RATE") #the code to the left is to better present and title the data retrieved
        print ("************************")
        print(ce.get_digital_currency_exchange_rate(crypto_name,"USD"))       #this code will print the ________ requested by the user to the crypto of their input
        print('Exchange Rate of '+ crypto_name + ' shown!') #this code will serve as a confirmation of what crypto they selected           
    elif userInput == 'e':
        cryptos_name = input("What is the crypto's Acronym?: \n")
        response = requests.get("https://www.alphavantage.co/query?function=CRYPTO_RATING&symbol="+cryptos_name+"&apikey="+API_key) #we'll inject the user's crypto choice in our url to fecth specified data
        json_out = response.json()
        print(json_out)
        print('Daily Results from '+ cryptos_name+ ' shown!') 
    elif userInput == 'f':
        cryptos_name = input("What is the crypto's Acronym?: \n") #this is how we'll acquire the user's crypto selection
        response = requests.get("https://www.alphavantage.co/query?function=CRYPTO_RATING&symbol="+cryptos_name+"&apikey="+API_key) #we'll inject the user's crypto choice in our url to fecth specified data
        json_out = response.json()
        json_name =  json_out['Crypto Rating (FCAS)']['2. name']       #this command will extract the name from the json output we recieved
        json_fr = json_out['Crypto Rating (FCAS)']['3. fcas rating']   #this command will extract the FCAS Rating from the json output we recieved
        json_fs = json_out['Crypto Rating (FCAS)']['4. fcas score']    #this command will extract the FCAS Score from the json output we recieved
        json_ds =  json_out['Crypto Rating (FCAS)']['5. developer score'] #this command will extract the Developer Score from the json output we recieved
        json_ma = json_out['Crypto Rating (FCAS)']['6. market maturity score']  #this command will extract the Market Maturity Score from the json output we recieved
        json_us = json_out['Crypto Rating (FCAS)']['7. utility score'] #this command will extract the Utility Score from the json output we recieved
        json_re = json_out['Crypto Rating (FCAS)']['8. last refreshed']#this command will extract the Date Last Updated from the json output we recieved
        json_tz = json_out['Crypto Rating (FCAS)']['9. timezone']      #this command will extract the Timezone from the json output we recieved
        #this command will save data from our json output into the table stock2.results
        mycursor.execute("INSERT INTO stock2.results (cr_name, fcas_rating, fcas_score, developer_score, market_maturity_score, utility_score, last_updated, update_timezone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",(json_name,json_fr,json_fs,json_ds,json_ma,json_us,json_re,json_tz))
        db.commit()
        print("Data Saved!")
    elif userInput == 'g':
        #if the user selects g) then we will display all our data saved sorted by the primary key of stock2.results
        print('All Contacts Presented\n') #code added 02/18/21 5:15pm
        mycursor.execute("select cr_name, fcas_rating, fcas_score, developer_score, market_maturity_score, utility_score, last_updated FROM stock2.results;") 
        #the following code will show all our data saved in the stock2.results database along with a header & legend for the user to understand what the numbers mean
        print("Legend")
        print("1. name")
        print("2. fcas rating")
        print("3. fcas score")
        print("4. developer score")
        print("5. market maturity score")
        print("6. utility score")
        print("7. last refreshed(YYYY-DD-MM HH-MM-SS")
        print('\n')
        for p in mycursor:
         print("  (1)        (2)      (3)  (4)  (5)  (6)                            (7)              ") 
         print(p)
         print ('\n')   
    elif userInput == 'h':
        #if the user selects h) then we will display all our data saved sorted by the FCAS Crypto Score Rating in ascending order
        mycursor.execute("SELECT cr_name, fcas_rating, fcas_score, developer_score, market_maturity_score, utility_score FROM stock2.results ORDER BY fcas_score ASC;") 
        #the following code will show all our data saved in the stock2.results database along with a header & legend for the user to understand what the numbers mean
        print("Legend")
        print("1. name")
        print("2. fcas rating")
        print("3. fcas score")
        print("4. developer score")
        print("5. market maturity score")
        print("6. utility score")
        print('\n')
        for p in mycursor:
         print("  (1)        (2)      (3)  (4)  (5)  (6)") 
         print(p)
         print ('\n')    
    elif userInput == 'i':
        #EXTRA CREDIT   (XRP should be deleted)
        #if the user selects i) then we will delete all entried that have a utility score lower than 800 
        mycursor.execute("DELETE FROM stock2.results WHERE stock2.results.utility_score < 800;") 
        print("All entries with a Utility Score Lower than '800' have been deleted!")        
    elif userInput == 'j':
        print('Exit Complete, GoodBye!\n')
        x = 2
        exit





