import requests
import json
from bs4 import BeautifulSoup
import sqlite3

MAIN_URL = "https://infopark.in/companies/company/kochi-phase-2"

connect = sqlite3.connect('data.db')

class InfoparkBasics:


    def __init__(self):
        pass


    def execute(self)
        print("[INFO] Fetching Data")
        response = requests.get(MAIN_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        self.companys(soup)

    def companys(self,soup):
        companys = soup.find_all("div", {"class": "my-list"})
        for company in companys:
            self.company_info(company)

    def update_data(self,data):
        cursor = connect.cursor()
        cursor.execute('select name from infophark where name = ?',(data['name'],))
        name = cursor.fetchall()

        if name[0] is not None:
            connect.execute('update infophark set logo = ?, url = ?, details = ?, opening = ?, profile = ? where name = ?',(data['logo'],data['url'],data['detail'],data['opening'],data['profile'],data['name']))
            connect.commit()
        else:
            connect.execute('insert into infophark (name,logo,url,details,opening,profile) values (?,?,?,?,?,?)',(data['name'],data['logo'],data['url'],data['detail'],data['opening'],data['profile']))
            connect.commit()

    def company_info(self,company):
       try:
            data = dict()
            data['logo'] = company.find("img")['src']
            data['name'] = company.find("h3").text
            data['url'] = company.find('div',{'class':'offer'}).find('a')['href'].replace('/',"")
            data["detail"] = "".join(company.find('div', {'class': "detail"}).find('span',{'class': "logo-container"}).find('p').text.strip().split("\r\n")).split("  ")[0]

            urls = company.find_all('div', {'class': "button_container"})
            for url in urls:
                data['opening'] = url.find('a', {'class': "btn-info"})['href']
                data['profile'] = url.find('a', {'class': "btn-success"})['href']
            
            self.update_data(data)
       except Exception as e:
           print(f"Erro on Compnay info: {e}")

    def save(self, data):
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    

if __name__ == "__main__":
    infopark = InfoparkBasics()
    infopark.execute()

