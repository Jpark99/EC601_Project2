import googlemaps
import folium
import os

def geocode_coordinates(api_key, southwest, northeast, num_points):
    gmaps_client = googlemaps.Client(key=api_key)

    geocodes = []

    # Generate evenly distributed points within the bounding box
    for i in range(num_points):
        # Calculate the point's coordinates within the bounding box
        lat = southwest[0] + (northeast[0] - southwest[0]) * (i / (num_points - 1))
        for j in range(num_points):
            lng = southwest[1] + (northeast[1] - southwest[1]) * (j / (num_points - 1))

            # Search for places near the point
            geocodes_result = gmaps_client.places_nearby(
                location=(lat, lng),
                radius=10000  # Adjust the radius as needed (in meters)
            )

            for result in geocodes_result.get('results', []):
                location = result['geometry']['location']
                geocodes.append(location)

    return geocodes

def display_map(southwest, northeast, geocodes):
    m = folium.Map(location=[southwest[0], southwest[1]], zoom_start=10)
    folium.Polygon([
        southwest,
        (northeast[0], southwest[1]),
        northeast,
        (southwest[0], northeast[1]),
        southwest
    ], color='blue').add_to(m)
    
    for location in geocodes:
        folium.Marker([location['lat'], location['lng']], tooltip='Geocode').add_to(m)
    
    return m

def save_to_output_file(geocodes):
    with open("output.txt", "w") as file:
        for location in geocodes:
            file.write(f"Latitude: {location['lat']}, Longitude: {location['lng']}\n")

if __name__ == "__main__":
    api_key = input("Enter your Google Maps API Key: ")

    southwest_coordinates = input("Enter the southwest coordinates (latitude,longitude): ")
    northeast_coordinates = input("Enter the northeast coordinates (latitude,longitude): ")

    southwest_lat, southwest_lng = map(float, southwest_coordinates.split(','))
    northeast_lat, northeast_lng = map(float, northeast_coordinates.split(','))

    num_points = int(input("Enter the number of evenly distributed points: "))

    southwest = (southwest_lat, southwest_lng)
    northeast = (northeast_lat, northeast_lng)

    geocodes = geocode_coordinates(api_key, southwest, northeast, num_points)
    print(f"Number of geocodes: {len(geocodes)}")

    save_to_output_file(geocodes)

    map_obj = display_map(southwest, northeast, geocodes)

    html_file_path = "map.html"
    map_obj.save(html_file_path)

    os.system(f"start {html_file_path}")