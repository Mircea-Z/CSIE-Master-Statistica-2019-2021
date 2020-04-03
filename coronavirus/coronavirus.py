import pandas as pd
import matplotlib.pyplot as plt
import requests

def get_data():
    data = requests.get('https://pomber.github.io/covid19/timeseries.json').json()
    return data

data = get_data()
data = data['Romania']

data = [item for item in data if item['confirmed']!=0]

data[0]['day_cases'] = 0
data[0]['day_deaths'] = 0
data[0]['day_recoveries'] = 0
data[0]['change_rate'] = 1
data[0]['cases_at_1_percent_mortality'] = 0


for i in range(1,len(data)):
    data[i]['day_cases'] = data[i]['confirmed'] - data[i-1]['confirmed']
    data[i]['day_deaths'] = data[i]['deaths'] - data[i-1]['deaths']
    data[i]['day_recoveries'] = data[i]['recovered'] - data[i-1]['recovered']
    data[i]['change_rate'] = data[i]['confirmed']/data[i-1]['confirmed']
    if i > 18:
        data[i-18]['cases_at_1_percent_mortality'] = data[i-19]['cases_at_1_percent_mortality']+data[i]['day_deaths']*100
    else:
        data[i]['cases_at_1_percent_mortality'] = 0

data = pd.io.json.json_normalize(data)
print(data.describe())

ax = plt.gca()

data.plot(kind='line', x='date', y='deaths', ax=ax)
data.plot(kind='line', x='date', y='recovered', color='red', ax=ax)
data.plot(kind='line', x='date', y='confirmed', color='green', ax=ax)
data.plot(kind='line', x='date', y='cases_at_1_percent_mortality', color='yellow', ax=ax)

plt.show()
