import requests
url = f'http://api.geonames.org/searchJSON?q=lahor&name_startsWith=lahor&username=haris'
# response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=lahore&appid=77b7d4fa2f6b05ab97b39c227bba2ff3")

response = requests.get(url)

data = response.json()

city_country_pairs = []
 # Create a set to store unique city-country pairs
city_country_set = set()

# Extract city names from the API response and create city-country pairs
for result in data['geonames']:
    city_name = result['name']
    country_name = result['countryName']

    # Append the city-country pair to the set (as tuples)
    city_country_set.add((city_name, country_name))

# Convert the set back to a list of dictionaries
city_country_pairs = [{'city': city, 'country': country} for city, country in city_country_set]


# print(response.json())

print(city_country_pairs, len(city_country_pairs))