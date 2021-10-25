from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
row = table.find_all('tr')

row_length = len(row)

temp = [] #initiating a list 

for i in row:
    
    daily_rate = i.find_all('td')
    daily_rate = daily_rate[0].text
    
    period = i.find_all('a')
    period = period[0].text
    
    temp.append((daily_rate,period))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp)
df = df.rename(columns={0:'Date',1:'Rate'})

#insert data wrangling here
df['Rate'] = df['Rate'].str.replace(',','')
df['Rate'] = df['Rate'].astype('float64')
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)