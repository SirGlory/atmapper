# Imports
import requests
from bs4 import BeautifulSoup
from geopy import Nominatim


class Scrape:

    def __init__(self, handle):
        self.handle = handle

    def get_locations(self):

        # Create Variables
        base_url = "https://www.picuki.com/profile/" + self.handle
        r = requests.get(base_url,
                         headers={
                             'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        all_locations = soup.find_all("div", {"class": "photo-location"})
        # print(all_locations)
        all_links = soup.find_all("div", {"class": "photo"})
        locations = []
        links = []
        latitudes = []
        longitudes = []
        # Add unique locations to list
        for i in range(0, len(all_locations), 1):
            locator = Nominatim(user_agent="myGeocoder")
            xx = all_locations[i].text.replace("\n", "")
            yy = all_links[i].find('a').get('href')
            try:
                locationi = locator.geocode(xx)
                zz = locationi.latitude
                ww = locationi.longitude
                # print(zz)
                if xx not in locations:
                    if xx != '':
                        locations.append(xx)
                        links.append(yy)
                        latitudes.append(zz)
                        longitudes.append(ww)
                    else:
                        pass
                else:
                    pass
            except:
                pass
        else:
            pass


        #
        reversed_locations = locations[::-1]
        reversed_links = links[::-1]
        reversed_latitudes = latitudes[::-1]
        reversed_longitudes = longitudes[::-1]
        # print(locs)
        # print(links)
        # print(base_url)
        return reversed_locations, reversed_links, reversed_latitudes, reversed_longitudes  # Revered location order. scraping puts newest first,
        # return l            # but to plot journey we would want oldest post as starting point


if __name__ == "__main__":
    #handle = str(input("Please enter handle of user: ") or '4x4theboiz')
    handle = "4x4theboiz"
    print(handle)
    point1 = Scrape(handle=handle)
    address = Scrape(handle=handle).get_locations()
    print(address[0][-1])
    # print(address[1])
    # print(address[2])
    # print(address[3])
