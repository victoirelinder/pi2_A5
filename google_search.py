from bs4 import BeautifulSoup
import requests
import regex as re
import pandas as pd
import time
import random
class Google_Analysis:
    
    def __init__(self, term):
        self.completeQuery = 'twitter.com '+str(term)
        self.encodedQuery = self.completeQuery.replace(' ','+')
        self.url = 'https://www.google.com/search?q={0}&source=lnms&tmb=nws'.format(self.encodedQuery)
    

    def run(self):
        soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        pattern = re.compile(r"@[^) ]+")
        result = soup.find("h3", {'class':'r'})
        if result is not None:
            if len(pattern.findall(result.text))>0:
                #print(result)
                return(pattern.findall(result.text)[0])
        else:
            return('')

df = pd.read_csv('LinkedInCompanies.csv', encoding='utf-8', delimiter=';')
companies_list = df["companies"].tolist()
companies_twitter_account = []
progress=round(1*100/len(companies_list),2)

#print(companies_list)
for companie in companies_list:
    time.sleep(random.randrange(start=7,stop=10)/10)
    print("progress : "+ str(progress) +'%')
    test = Google_Analysis(term=companie)
    companies_twitter_account.append(test.run())
    progress+=round(1*100/len(companies_list),2)
    
print(companies_twitter_account)

df["twitter_account"] = companies_twitter_account
df = df[['companies', 'twitter_account', 'location', 'nb_of_followers', 'url', 'about']]
df.to_csv('LinkedInCompanies.csv', encoding='utf-8', index=False, sep=';')