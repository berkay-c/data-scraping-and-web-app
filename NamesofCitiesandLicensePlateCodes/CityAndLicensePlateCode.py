import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from flask import Flask

response = requests.get("https://www.ilimiz.net/il-plaka-kodlari.html")
# print(response.status_code) Returned 200 successful
soup = BeautifulSoup(response.content, "lxml")

data = soup.find_all("span", {"class": "sehir op"})
dataframe = pd.DataFrame(data, columns=["Şehir_Adı", "Boş", "Plaka_Kodu"])
temporaryframes = dataframe.Plaka_Kodu.str.split(" ", expand=True)

temporaryframes.columns = ["Plaka_Kodu", "Delete1", "Delete2"]
# We leave the columns that will not work for us
dataframe = dataframe.drop(columns=['Boş', 'Plaka_Kodu'])
temporaryframes = temporaryframes.drop(columns=["Delete1", "Delete2"])
# We combine our  dataframe and temporaryframes and get the actual cleaned data.
dataframe = pd.concat([dataframe, temporaryframes], axis=1)
# Dataframe to csv  , does not pass index values
dataframe.to_csv("out.csv", index=False)
# print(dataframe.head())

# If it cannot find the database named 'my_database', it creates it
conn = sqlite3.connect('my_database.db')
c = conn.cursor()
# Read 'out.csv'
out = pd.read_csv("out.csv")
# "We need to delete the <strong> and </strong> tags.
out.Şehir_Adı = out.Şehir_Adı.str.replace('<strong>', '').str.replace("</strong>", "")
# print(out)

# If it cannot find the table named 'CityPlateCode', it creates it
out.to_sql("CityPlateCode", conn, if_exists='replace', index=False)
# print(pd.read_sql('''SELECT * FROM CityPlateCode''', conn))

# Creating a web app with Flask
app = Flask(__name__)


@app.route("/welcomepage")  # http://localhost:5000/welcomepage
def hello():
    startPage = "Enter the license plate code or the name of the city in the URL field."\
    "<br/> Example:http://localhost:5000/welcomepage/46 OR http://localhost:5000/welcomepage/aydin"
    return startPage

@app.route("/welcomepage/<int:platecode>")  # http://localhost:5000/welcomepage/[enter plate code ]
def PlateCode(platecode):
    while platecode<82 and platecode>0:
        vt = sqlite3.connect('my_database.db') # We Connect to Database
        cur = vt.cursor()
        # We make our query
        cur.execute('''SELECT Şehir_Adı FROM CityPlateCode where Plaka_Kodu=?''', (platecode,))
        results = cur.fetchall()
        return f"{results[0][0]}"
    return f"{platecode} Plate Codes Are Not Available! <br/> Please Enter A Valid License Plate Code"
       

@app.route("/welcomepage/<string:city>") # # http://localhost:5000/welcomepage/[enter city name ]
def CityName(city):
    city=city.upper() # Capitalize All Letters of the City Name
    con = sqlite3.connect('my_database.db') # We Connect to Database
    cr = con.cursor() 
    # We make our query
    cr.execute("SELECT Plaka_Kodu FROM CityPlateCode WHERE Şehir_Adı like '" +str(city)+"'") 
    dataresults = cr.fetchone() 
    if dataresults[0]<10:
        sonuc = "0"+ str(dataresults[0])
        return sonuc
    else:
        return f"{dataresults[0]}"
   
    

if __name__ == "__main__":
    app.run(host='localhost')  # http://localhost:5000
