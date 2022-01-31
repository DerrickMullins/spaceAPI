import requests
import cartopy.crs as ccrs # Mapping
import cartopy.feature as cfeature # Map features
import matplotlib.pyplot as plt # Visualization
from geopy.geocoders import Nominatim # Geolocation Service
from functools import partial # Convert location to english
from datetime import datetime
from matplotlib.animation import FuncAnimation # Animate plots on map

# List's to hold lat and long coordinates
latList = []
longList = []


# Create map/figure to plot
fig, _ = plt.subplots(1, 1)
ax = plt.axes(projection=ccrs.PlateCarree())


# Add features to map
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
ax.stock_img()

# Function to animate plots
def animate(i, latList:list, longList:list):

	# Access Internatinal Space Station location API using request lib
	request = requests.get('http://api.open-notify.org/iss-now.json')

	# Access JSON content
	jsonResponse = request.json()
	
	# ISS curent location
	issLocation = jsonResponse["iss_position"]

	# ISS location timestamp
	issTimeStamp = jsonResponse["timestamp"]
	# Convert timestamp to datetime
	dateObj = datetime.fromtimestamp(issTimeStamp)
			
	# Extract lat/long from issLocation dict
	latitude =  issLocation["latitude"]
	longitude = issLocation["longitude"]

	try:
		# Initialize Nominatim API
		geolocator = Nominatim(user_agent="spaceAPI", timeout=20)

		# Location of ISS using geolocator
		location = geolocator.reverse((latitude, longitude))
		
		# Convert geopy location to english
		geocode = partial(geolocator.geocode, language='es')

	except:
		print("Geolocator not working!")

	try:
		# Get raw location address
		address = location.raw['address']
				
		# Define extracted data
		city = address.get('city', '')
		state = address.get('state', '')
		country = address.get('country', '')
		code = address.get('country_code')
		zipcode = address.get('postcode')

		# Display location information to terminal
		print("City:", geocode(city))
		print("State:", geocode(state))
		print("Country:", geocode(country))
		print("Country code:", code)
		print("Time:", dateObj)
		print("longitude:", longitude)
		print("latitude:", latitude)
		print(" ")

	except:
		# Display location information and write to CSV file
		print("The International Space Station is somewhere over the ocean!")
		print("long:", longitude, "|", "lat:", latitude)
		print(" ")

	finally:
		# Add coordinates to lat and long list
		latList.append(float(latitude))
		longList.append(float(longitude))
		

		# Plot map points
		ax.plot(longList,latList, color='red', marker="o", markersize=5,transform=ccrs.PlateCarree())


ani = FuncAnimation(fig, animate, fargs=(longList,latList), interval=60000)
plt.show()
	

