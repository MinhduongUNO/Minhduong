## Import the necessary packages
import pandas as pd
import googlemaps
import json

#add Google API Key
gmaps = googlemaps.Client(key='')

# read the Excel in as a dataframe
df = pd.read_excel('export.xls')

#create a GEOJSON shell
collection = {'type': 'FeatureCollection', 'features': []}

#create a "fulladdress" column that combines address, city and country
df['fulladdress'] = df[['Address', 'City', 'Country']].apply(lambda x: ' '.join(x.astype(str)), axis=1)

coordinates = {}

#this function will assign values to each key in the GEOJSON
def feature_from_row(Factory, Fulladdress, SupplierGroup, Country, Brand, FactoryType, ProductType):
    feature = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': []},
               'properties': {'Factory Name': '', 'Address': '',
                              'Country': '', 'SupplierGroup': '',
                              'Brand': '', 'Factory Type': '', 'Product Type': ''},
               }
    #create a geocoding JSON
    geocode_result = gmaps.geocode(Fulladdress)
    json_str = json.dumps(geocode_result)
    resp_dict = json.loads(json_str)
    #get the coordinates
    for i in resp_dict:
        coordinates = (i['geometry']['location'])

    feature['geometry']['coordinates'] = [coordinates['lng'], coordinates['lat']]
    feature['properties']['Factory Name'] = Factory
    feature['properties']['Address'] = Fulladdress
    feature['properties']['Country'] = Country
    feature['properties']['Brand'] = Brand
    feature['properties']['Factory Type'] = FactoryType
    feature['properties']['Product Type'] = ProductType
    feature['properties']['SupplierGroup'] = SupplierGroup
    collection['features'].append(feature)
    return feature

#feed each row into the previous function
geojson_series = df.apply(
    lambda x: feature_from_row(x['Factory Name'], x['fulladdress'], x['Supplier Group'], x['Country'],
                               x['Brand'], x['Factory Type'], x['Product Type']),
    axis=1)
#create a JSON file
jsonstring = pd.io.json.dumps(collection)
#write the file to a GEOJSON
output_filename = 'Nike.geojson'  # The file will be saved under static/GEOJSON
with open(output_filename, 'w') as output_file:
    output_file.write(format(jsonstring))
