import pandas as pd
import yfinance as yf
import csv
import requests
from bs4 import BeautifulSoup
import os
import time


class stock_info:
    def __init__(self,name,filename="stock.csv",filename2="news.csv",filename3="article.csv") -> None:
        self.name = name
        self.file_name = filename
        self.file_name2 = filename2
        self.file_name3 = filename3
        
    def stock_to_csv(self,period="1d") -> None:
        try:
            tick = yf.Ticker(self.name)
            stock = tick.history(period=period).to_csv(self.file_name)
            df = pd.read_csv(self.file_name)
            df = df.drop(columns=["Dividends","Stock Splits"])
            df.to_csv(self.file_name,index=False)
            print("Success!")
            print(f"{self.file_name} has been created")
        except:
            print("Something went wrong")
    
    def news_to_csv(self) -> None:
        try:
            tick = yf.Ticker(self.name)
            news = tick.news

            with open(self.file_name2,"w") as f:
                writer = csv.writer(f)
                writer.writerow(["Title","Publisher","Link"])
                for i in news:
                    title = i["title"]
                    publisher = i["publisher"]
                    link = i["link"]

                    writer.writerow([title,publisher,link])
            print("Success!")
            print(f"{self.file_name2} has been created")
        except:
            print("Something went wrong")

    def article_to_csv(self) -> None:
        try:
            tick = yf.Ticker(self.name)
            news = tick.news
            news_array = []
            num = 1
            
            for i in news:
                link = i["link"]
                
                article = requests.get(link)
                soup = BeautifulSoup(article.text,"html.parser")
                news = soup.find("div",attrs={'class': 'caas-body'})
                if(news == None):
                    news_array.append(["No Article"])
                else:
                    news_text = news.get_text(separator='\n\n')
                    news_array.append([news_text])
                
            with open(self.file_name3,"w") as f:
                writer = csv.writer(f)
                writer.writerow(["Article's"])
                    
                for article in news_array:
                    writer.writerow([f"Article {num}'s - Body"])
                    writer.writerow(article)     
                    num += 1      
            print("Success!")
            print(f"{self.file_name3} has been created")
        except:
            print("Something went wrong")
    
    def get_yesterdays_article(self) -> None:

        # gets yesterdays date 
        # and gets the article from that date
        try:
            tick = yf.Ticker(self.name)
            news = tick.news
            news_array = []
            title_array = []
            num = 1
            #gets the date in the form of "Month Day, Year"
            yesterday = time.strftime("%B %d, %Y", time.localtime(time.time() - 86400))
            today = time.strftime("%B %d, %Y", time.localtime(time.time()))
            for i in news:
                title = i["title"]
                link = i["link"]
                article = requests.get(link)
                soup = BeautifulSoup(article.text,"html.parser")
                date = soup.find("div",attrs={'class': 'caas-attr-time-style'})
                news = soup.find("div",attrs={'class': 'caas-body'})
                if(news == None):
                    news_array.append(["No Article"])
                else:
                    if(yesterday in date.text or today in date.text):
                        news_text = news.get_text(separator='\n\n')
                        news_array.append([news_text])
                        title_array.append([title])
                
            with open(self.file_name3,"w",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Article's"])
                    
                for article in news_array:
                    
                    writer.writerow([f"Article {num}'s - Body"])
                    writer.writerow(title_array[num-1])
                    writer.writerow(article)     
                    num += 1      
            print("\nSuccess!\n")
            print(f"{self.file_name3} has been created\n")
        except:
            print("\nSomething went wrong")

    def append_yesterdays_article(self) -> None:
        # gets yesterdays date 
        # and gets the article from that date
        tick = yf.Ticker(self.name)
        news = tick.news
        news_array = []
        date_array = []
        title_array = []
        num = 1

        #gets the date in the form of "Month Day, Year"
        yesterday = time.strftime("%B %#d, %Y", time.localtime(time.time() - 86400))
        today = time.strftime("%B %#d, %Y", time.localtime(time.time()))

        #goes through each article and gets the date, title, and article
        for i in news:
            link = i["link"]
            title = i["title"]
            article = requests.get(link)

            #using beautiful soup, we get the date and body of the article
            soup = BeautifulSoup(article.text,"html.parser")
            date = soup.find("div",attrs={'class': 'caas-attr-time-style'})
            news = soup.find("div",attrs={'class': 'caas-body'})


            #depends on the content of the article, we either append the article or append "No Article"
            if(news == None):
                news_array.append(["No Article"])
                date_array.append(["No Date"])
                title_array.append(["No Title"])
            else:
                if(yesterday in date.text or today in date.text):
                    news_text = news.get_text(separator='\n\n')
                    news_array.append([news_text])
                    date_array.append([date.text])
                    title_array.append([title])

        
        #appends the article to the csv file
        with open(self.file_name3,"a",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Article's"])
                    
            for article in news_array:
                
                if(article == ["No Article"]):
                    continue
                else:
                    writer.writerow([f"Article {num}'s - Body | date published: {date_array[num-1]}, title: {title_array[num-1]}"])
                    writer.writerow(article)     
                    num += 1
                          
        print("\nSuccess!\n")
        print(f"{self.file_name3} has been created\n")

    def clear_csv(self,name) -> None:
        try:
            os.remove(name)
            print("Success!")
            print(f"{name} has been deleted")
        except:
            print("Something went wrong \n the file does not exist")
    
    def fetch_data(self) -> None:
        # W.I.P

        try:
            ticker = yf.Ticker(self.name)

            # Get historical market data
            hist = ticker.history(period="1d")
            opening_price = hist['Open'][0]
            closing_price = hist['Close'][0]
            trading_volume = hist['Volume'][0]

            # Get company info
            info = ticker.info
            investor_relations = info['longBusinessSummary']
            company_info = info['fullTimeEmployees']

            # Write data to CSV
            with open('stock.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([ticker, investor_relations, company_info, opening_price, closing_price, trading_volume])
        except:
            print("Something went wrong")


if __name__ == "__main__":
    stock = stock_info("AAPL")
    stock.stock_to_csv()




    