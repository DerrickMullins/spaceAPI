import json
import time
import cartopy.crs as ccrs
import matplotlib.pyplot as plt



def plotMap():

	fig, _ = plt.subplots(1, 1)
	ax = plt.axes(projection=ccrs.PlateCarree())
	ax.stock_img()

	plt.show()




plot = plotMap()