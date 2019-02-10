from geopy.extra.rate_limiter import RateLimiter
import folium
import pandas
import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim(timeout=100)

geocode = RateLimiter(geolocator.geocode, error_wait_seconds=0.5,
                      max_retries=0, swallow_exceptions=False, return_value_on_exception=True)


def find_titles(fname, year):
    """
    (str) -> dict
    returns a dict with a title of a movie, made that year, as a key and a location as a value
    """
    eeee = 1241786
    #eeee = 12417
    main_dict = {}
    with open(fname, "r", encoding='utf-8', errors='ignore') as file:
        for x, line in enumerate(file):
            if x > 13 and x < eeee and str(year) in line:
                words = line.split()
                title = ''
                name = ''
                location = ''
                for i in range(len(words)):
                    if words[i].startswith("(") and words[i][1:5].isdigit() is True\
                            and len(words[i]) > 5 and words[i][1:5] == str(year) and i != len(words)-1:
                        name = words[:i]
                        if words[i+1].startswith("{"):
                            i1 = line.index('}')
                            place = line[i1+1:]
                            try:
                                index2 = place.index('(')
                                location = place[:index2]
                            except:
                                location = place
                        else:
                            place = words[i+1:]
                            for n in place:
                                location += n + ' '
                            try:
                                index2 = location.index('(')
                                location = location[:index2]
                            except:
                                pass

                location = location.replace('\t', '').replace('\n', '')
                for n in name:
                    title += n + ' '
                if title != '':
                    try:
                        main_dict[location].add(title)
                    except:
                        main_dict.update({location: {title}})
    return main_dict


def draw_movies(year, main_dict, map):
    """
    (str,dict,map) -> None
    Points a location of a movie at a map
    """
    movies_layer = folium.FeatureGroup(name="movies in " + str(year))
    for i in main_dict:
        movies_list = ", ".join(x for x in list(main_dict[i]))[1:-1]
        movies_list = movies_list.replace('"', '').replace("'", "")
        location = geolocator.geocode(i)
        if location is None:
            pass
        else:
            movies_layer.add_child(folium.Marker(location=[location.latitude, location.longitude],
                                                 popup=movies_list))
    map.add_child(movies_layer)


def draw_population(map):
    """
    (map) -> None
    Draws a map of population
    """
    population_layer = folium.FeatureGroup(name="Population")
    population_layer.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                                              style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                                                        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))
    map.add_child(population_layer)


def main():
    """
    The main function of a module
    """
    map = folium.Map()
    print('Type a year')
    year = input()
    main_dict = find_titles('locations.list', year)
    print(main_dict)
    draw_movies(year, main_dict, map)
    draw_population(map)
    map.add_child(folium.LayerControl())
    map.save('Map.html')


if __name__ == '__main__':
    main()
