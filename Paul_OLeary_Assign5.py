"""
Paul O'Leary   Assignment #5   5/29/2021

Comp 4433 Data Visualization

Assignment #5 - various Geo Data exercises

"""

# Load standard libraries, and some libraries for the geo data.

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# import geopandas as gpd
import json
import pandas as pd
# import altair as alt

import folium

import sys

"""
Part 1

World Map with Capitals, using Folium

"""

caps = pd.read_csv('capitals_lat_lon_csv.txt', sep='\t')
# print(caps)

# Create the empty world map
world_map = folium.Map(tiles="cartodbpositron")

#for each coordinate, create circlemarker
for i in range(len(caps)):
        lat = caps.iloc[i]['Latitude']
        long = caps.iloc[i]['Longitude']
        # radius = 2
        popup_text = """Country : {}<br>
                    Capital : {}<br>"""
        popup_text = popup_text.format(caps.iloc[i]['Country'],
                                   caps.iloc[i]['Capital']
                                   )
        folium.Marker(location = [lat, long],  popup = popup_text, fill = True).add_to(world_map) # radius = radius,

title_html = '''
             <h3 align="center" style="font-size:20px"><b>World Capitals (click on markers for more info</b></h3>
             '''
world_map.get_root().html.add_child(folium.Element(title_html))

print("======")     
print("Part 1")
print("======")

print()
# Save the map as an HTML file
world_map.save('P1_World_Caps.html')
print('Map saved to "P1_World_Caps.html"')
print()

"""
Part 2

Three points of Lat/Lon to cover Africa with a triangle.  Display the three points on a map,
to show that they would cover the continent.  Use shapely to display the triangle, then compute
the area and perimiter of the triangle using the lat/lon as the numerics.

"""

print("======")     
print("Part 2")
print("======")
print()

# Define the three corners
corner_data = {'Corner':['C1', 'C2', 'C3'], 'Lat':[33.972, -33.925, 11.815], 'Lon':[-6.850, 18.424, 51.260]}
tri_df = pd.DataFrame(corner_data)

print()
print("Three corners to cover Africa")
print(tri_df)
print()

# Create the empty world map
world_map = folium.Map(tiles="cartodbpositron", min_zoom=3, max_zoom=18, zoom_start=15, min_lat = -40, max_lat = 40, 
                       min_lon= -10, max_lon = 50, max_bounds=True)  # min_zoom=0, max_zoom=18, 

#for each coordinate, create circlemarker
for i in range(len(tri_df)):
        lat = tri_df.iloc[i]['Lat']
        long = tri_df.iloc[i]['Lon']
        
        folium.Marker(location = [lat, long],  fill = True).add_to(world_map) # radius = radius,

title_html = '''
             <h3 align="center" style="font-size:20px"><b>Corners of Triangle to Cover Africa</b></h3>
             '''
world_map.get_root().html.add_child(folium.Element(title_html))
        
# Save the map as an HTML file
world_map.save('P2_Africa_Tri.html')
print('Map saved to "P2_Africa_Tri.html"')
print()

from shapely.geometry import Point, Polygon
tri = Polygon(((33.972, -6.850), (-33.925, 18.424), (11.815, 51.260)))

print("Dimensions of the triangle:")
print("Area: ", tri.area)
print("Perimeter: ", tri.length)
print()


"""
Part 3

Construct boundaries for Kansas and Nebraska, using 4 and 6 points respectively.  
Create a GeoJSON File, read that file, form a dictionary, plot the results.

I used the web access of "geojson.io" to create a simple geojson file as requested.
That file is called "map.geojson".

"""

import geojson
import geojsonio

print("======")     
print("Part 3")
print("======")
print()

contents = open('map.geojson').read()
print("Contents of the geojson file, 'map.geojson'.")
print(contents)

# Display the contents as a web page.
geojsonio.display(contents)

import geopandas as gpd
import geoplot
import geoplot.crs as gcrs

data = gpd.read_file("map.geojson")
print()
print("Data from the geojson file")
print(data)
print()

# Geoplot of the shapes of the states, without a map behind.
geoplot.polyplot(data)

# Create a Dictionary

import json
f = open('map.geojson')
data = json.load(f)
f.close()

# Print the contents of that dictionary
print("Contents of the Dictionary")
for (i, j) in data.items():
    print("Key: " + i)
    print("Value: " + str(j))
print()


"""
Part 4

Happiness Index
"""

print("======")     
print("Part 4")
print("======")
print()

import plotly
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# List of US States with abbreviations courtesy of:
# https://github.com/jasonong/List-of-US-States/find/master
st = pd.read_csv('states.csv')
# print(st)

# I based a Happiness Index as a random number between 0 and 1.
st['Happiness'] = np.random.rand(51)
# print(st)

labels = {"Happiness":"Happiness Index", "locations":"State"}

fig1 = px.choropleth(st.Happiness, locations=st.Abbreviation, locationmode="USA-states", 
                     scope="usa", color='Happiness', color_continuous_scale="hot", 
                     title="Happiness Index (random)",
                     hover_name="Happiness", labels=labels) #, hover_data="debtfree")

fig1.show()
fig1.write_html('P4_St_Happiness.html')

print("Happiness Map saved to 'P4_St_Happiness.html'")
print()


"""
Part 5

Bokeh Histogram of a 500 random exponential numbers.
"""

from bokeh.plotting import figure
from bokeh.io import output_notebook, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import Tabs
import bokeh

print("======")     
print("Part 5")
print("======")
print()

# Generate 500 random numbers from the exponential distribution.
nums = np.random.exponential(size = 500)
# print(nums)

# For a Histogram

import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file

output_file('P5_Hist_Exponential.html')
print("Histogram will be saved to 'P5_Hist_Exponential.html'")
np.random.seed(51)

xx, edges = np.histogram(nums, bins=20, range=[0, 4])

df=pd.DataFrame({'xx': xx, 'left': edges[:-1], 'right': edges[1:]})

p=figure(plot_width=1200, plot_height=500)

p.quad(bottom=0, top=df['xx'], left=df['left'], right=df['right'], fill_color='red', line_color='black')

show(p)

print()



