import aiml
import os
import requests
import json




def google_geocode(address):
	new_address=""
	for x in address:
		if x==" ":
			x="+"
		new_address+=x

	google_api_key='AIzaSyAXUtDkcCJVcX14G-wxKk9VJKKHNq-wuXQ'
	google_base_url="https://maps.googleapis.com/maps/api/geocode/json?address="
	

	full_url = google_base_url+address+'&key='+google_api_key
	

	if full_url not in CACHE_DICTION:

	      # make the request and store the response
	    response = requests.get(full_url)
	    CACHE_DICTION[full_url] = response.text

	      # write the updated cache file
	    cache_file = open(CACHE_FNAME, 'w')
	    cache_file.write(json.dumps(CACHE_DICTION))
	    cache_file.close()





	

	data = json.loads(CACHE_DICTION[full_url])
	if (data['status']=='ZERO_RESULTS'):
		return False
	lat= data["results"][0]['geometry']["location"]["lat"]
	lng= data["results"][0]['geometry']["location"]["lng"]
	lat_lng=str(lat)+","+str(lng)
	cityName= data["results"][0]['address_components'][2]['long_name']
	return lat_lng,cityName


def darksy_api(lat_lng):

	base_url = 'https://api.darksky.net/forecast/'
	api_key = "6e493c40808413b6bcc86da1f6d1f433"

	full_url = base_url+api_key+'/'+lat_lng[0]

	if full_url not in CACHE_DICTION:

	      # make the request and store the response
	    response = requests.get(full_url)
	    CACHE_DICTION[full_url] = response.text

	      # write the updated cache file
	    cache_file = open(CACHE_FNAME, 'w')
	    cache_file.write(json.dumps(CACHE_DICTION))
	    cache_file.close()

	
	if CACHE_DICTION[full_url]=="Not Found\n":
		return False
	data = json.loads(CACHE_DICTION[full_url])
	degree_sign= u'\N{DEGREE SIGN}'
	
	
	return data
	




CACHE_FNAME = 'cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}






bot=aiml.Kernel()

for file in os.listdir('aiml_data'):
	bot.learn(os.path.join('aiml_data', file))







def weather_like(city):
	lat_lng = google_geocode(city)
	if lat_lng == False:
		return "Is {} a city?".format(city)
	weather= darksy_api(lat_lng)
	if weather==False:
		return "Sorry, I don't know"
	temp=weather['currently']['temperature']
	temp_summary=weather['currently']['summary']
	return 'In {}, it is {} and {}'.format(city,temp,temp_summary)
	
bot.addPattern("What's the weather like in {city}", weather_like)



def tempMax_weekly(hot_or_cold,city):
	lat_lng = google_geocode(city)
	if lat_lng == False:
		return "Is {} a city?".format(city)
	weather= darksy_api(lat_lng)
	if weather==False:
		return "Sorry, I don't know"
	
	week_weathers=[]

	for x in range(8):
		week_weathers.append(weather['daily']['data'][x]['temperatureMax'])
	max_temps=sorted(week_weathers, reverse=True)
	max_temp=max_temps[0]
	min_temp=max_temps[-1]
	if hot_or_cold=="hot":
		return 'In {} it will reach {}'.format(city,max_temp)
	if hot_or_cold=="cold":
		return 'In {} it will reach {}'.format(city,min_temp)
	
	
bot.addPattern("How {hot_or_cold} will it get in {city} this week?", tempMax_weekly)



def tempMaxMin_today(hot_or_cold, city):
	lat_lng = google_geocode(city)
	if lat_lng == False:
		return "Is {} a city?".format(city)
	weather= darksy_api(lat_lng)
	if weather==False:
		return "Sorry, I don't know"
	max_temp=weather['daily']['data'][0]['temperatureMax']
	min_temp=weather['daily']['data'][0]['temperatureMin']
	if hot_or_cold=="hot":
		return 'In {} it will reach {} today'.format(city,max_temp)
	if hot_or_cold=="cold":
		return 'In {} it will reach {} today'.format(city,min_temp)
	
bot.addPattern("How {hot_or_cold} will it get in {city} today?", tempMaxMin_today)




def rain_probability_Week(city):
	

	lat_lng = google_geocode(city)
	if lat_lng == False:
		return "Is {} a city?".format(city)
	weather= darksy_api(lat_lng)
	if weather==False:
		return "Sorry, I don't know"
	rain_prob_product=1

	for x in range(8):
		rain_prob_product*=(1-weather['daily']['data'][x]['precipProbability'])
	rain_prob=1- rain_prob_product

	if rain_prob < 0.1:
		return 'It almost definitely will not rain in {}'.format(city)
	elif rain_prob >= 0.1 and rain_prob < 0.5:
		return 'It probably will not rain in {}'.format(city)
	elif rain_prob >= 0.5 and rain_prob <= 0.9:
		return 'It probably will rain in {}'.format(city)
	else:
		return 'It will almost definitely rain in {}'.format(city)


bot.addPattern('Is it going to rain in {city} this week?', rain_probability_Week)


def rain_probability_Today(city):
	

	lat_lng = google_geocode(city)
	if lat_lng == False:
		return "Is {} a city?".format(city)
	weather= darksy_api(lat_lng)
	if weather==False:
		return "Sorry, I don't know"
	
	rain_prob=weather['daily']['data'][0]['precipProbability']

	if rain_prob < 0.1:
		return 'It almost definitely will not rain in {}'.format(city)
	elif rain_prob >= 0.1 and rain_prob < 0.5:
		return 'It probably will not rain in {}'.format(city)
	elif rain_prob >= 0.5 and rain_prob <= 0.9:
		return 'It probably will rain in {}'.format(city)
	else:
		return 'It will almost definitely rain in {}'.format(city)


bot.addPattern('Is it going to rain in {city} today?', rain_probability_Today)

q=raw_input("> ")
while(q!="exit"):
    print('{}\n'.format(bot.respond(q)))
    q=raw_input("> ")




























