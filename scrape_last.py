import requests
from bs4 import BeautifulSoup


# Create Variables
class ScrapeLast:

    def __init__(self, handle):
        self.handle = handle

    def get_last(self):
        base_url = "https://www.picuki.com/profile/" + self.handle
        r = requests.get(base_url,
                         headers={
                             'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        last_loc = soup.find_all("div", {"class": "photo-location"})
        last_location = []
        # Add unique locations to list

        for i in range(0, len(last_loc), 1):
            xx = last_loc[i].text.replace("\n", "")
            if xx not in last_location:
                if xx != '':
                    while len(last_location) < 1:
                        last_location.append(xx)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        return last_location


if __name__ == "__main__":
    handle = str(input("Please enter handle of user: ") or '4x4theboiz')
    print(handle)
    point1 = ScrapeLast(handle=handle)
    address = point1.get_last()
    print(address[0])
