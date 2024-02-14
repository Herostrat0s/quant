import requests
from bs4 import BeautifulSoup
import pandas as pd 
stocks = ["ACSEL"]
url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=A1CAP"
r = requests.get(url)

for i in stocks:
    name = i
    dates = []
    year = []
    periods = []

    url_1 = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+name
    r_1 = requests.get(url_1)
    soup = BeautifulSoup(r_1.text,"html.parser")
    choice = soup.find("select",id="ddlMaliTabloFirst")
    choice_2 = soup.find("select",id="ddlMaliTabloGroup")
    
    try:
        extracted_dates = choice.findChildren("option")
        extracted_dates_2 = choice_2.find("option")["value"]
    
        for date in extracted_dates:
            dates.append(date.string.rsplit("/"))
        
        for j in dates:
            year.append(j[0])
            periods.append(j[1])
    
        if len(dates) >= 4:
            parameters = (
                ("companyCode",name),
                ("exchange","TRY"),
                ("financialGroup",extracted_dates_2),
                ("year1",year[0]),
                ("period1",periods[0]),
                ("year2",year[1]),
                ("period2",periods[1]),
                ("year3",year[2]),
                ("period3",periods[2]),
                ("year4",year[3]),
                ("period4",periods[3]))
            url_2 = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
            r_2= requests.get(url_2,params=parameters).json()["value"]
            data = pd.DataFrame.from_dict(r_2)
            data.drop(columns=["itemCode","itemDescEng"],inplace=True)
        else:
            continue
    except AttributeError:
        continue
    del dates[0:4]
    all_data = [data]

    for _ in range(0,int(len(dates)+1)):
        if len(dates) == len(year):
            del dates[0:4]
        else:
            year = []
            periods = []
            for j in dates:
                year.append(j[0])
                periods.append(j[1])
            print(year)
        if len(dates) >= 4:
            parameters_2 = (
                ("companyCode",name),
                ("exchange","TRY"),
                ("financialGroup",extracted_dates_2),
                ("year1",year[0]),
                ("period1",periods[0]),
                ("year2",year[1]),
                ("period2",periods[1]),
                ("year3",year[2]),
                ("period3",periods[2]),
                ("year4",year[3]),
                ("period4",periods[3]),)
            r_2= requests.get(url_2,params=parameters).json()["value"]
            data = pd.DataFrame.from_dict(r_2)
            data.drop(columns=["itemCode","itemDescEng"],inplace=True)
