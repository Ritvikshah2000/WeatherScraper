import requests
from bs4 import BeautifulSoup
import pandas as pd

#----------------------------- a status code starting with a 2 generally indicates success, and a code starting with a 4 or a 5 indicates an error

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=45.6322&lon=-122.6716") #downloads web page containing forecast
soup = BeautifulSoup(page.content, 'html.parser') #crerates a bs4 class to parse the page
week_forecast = soup.find(id="seven-day-forecast") #find the div class with specific id
forecast_items = week_forecast.find_all(class_="tombstone-container") #inside the div, find each individual forecast item
tonight = forecast_items[0]
# print(tonight.prettify())

#---------------------------------extract name of forecast item, short description and temperature for tonight:
period = tonight.find(class_="period-name").get_text()
description = tonight.find(class_="short-desc").get_text()
temperature = tonight.find(class_="temp").get_text()
#print(period)
#print(description)
#print(temperature)

#-----------------------------------extract title attribute img tag. Treat bs4 object like a dictionary, and pass in the attribute we want as a key:
image = tonight.find("img")
desc = image['title']
#print(desc)

#------------------------------------select all items with class period-name inside an item with class tombstone-container in week_forecast
#------------------------------------use a list comprehension to call the get_text method on each beuaitfulsoup object
period_tags = week_forecast.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
#print(periods)

short_descs = [sd.get_text() for sd in week_forecast.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in week_forecast.select(".tombstone-container .temp")]
descs = [d["title"] for d in week_forecast.select(".tombstone-container img")]
#print(short_descs)
#print(temps)
#print(descs)

weather = pd.DataFrame({
    'Period': periods,
    'Brief': short_descs,
    'Temperature': temps,
    'Description': descs
})
print(weather)

