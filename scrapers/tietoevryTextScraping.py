import requests 
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
filePath = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/data/raw/tietoevryblogs.csv"
saveFilePath = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/data/raw/tietoevryBlogsFinal.csv"

df = pd.read_csv(filePath)

df_copy = df.copy()
df_copy["text"] = None
df_copy["author"] = None
df_copy["category"] = None
df_copy["date"] = None
error_list = []
for idx, row in df.iterrows():
    name = row["name"]
    other = row["others"]
    link = row["link"]
    other_list = other.split("/")
    try:
        URL = "https://www.tietoevry.com"+link
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        a_list = soup.find("div", class_="contentArea").findChildren(recursive=False)
        pattern = r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\|\\]'

        # Use the re.sub() function to replace matched characters with an empty string
        cleaned_name = re.sub(pattern, '', name)

        # Remove spaces by replacing them with an empty string
        cleaned_name = cleaned_name.replace(' ', '-')
        
        filename = f"E:/Group1FuturiceDSP/tietoevrytexts/{cleaned_name}.txt"

        textStore = ''
       
        for elem in a_list:
            
            textStore = textStore + elem.text.strip()

        df_copy.loc[idx,"text"] = textStore
        df_copy.loc[idx,"author"] = other_list[1]
        df_copy.loc[idx,"category"] = other_list[0]
        df_copy.loc[idx,"date"] = other_list[2]

        print(cleaned_name+" Done")
    except:
        error_list.append(link)

df_copy.to_csv(saveFilePath)
print(error_list)
