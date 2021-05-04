import sqlite3
from scrape import Scrape
from scrape_last import ScrapeLast


class DataCheck:

    def __init__(self, handle):
        self.handle = handle

    def db_check(self):
        outdated = True
        while outdated:
            # Try table read otherwise create
            try:
                connection = sqlite3.connect("posts.db")
                cursor = connection.cursor()
                sql = f"""SELECT * FROM "{self.handle}" """
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.close()
                # Try table read otherwise populate
                try:
                    #print(result)
                    #print(result[-1])
                    last_location_data = result[-1][0]
                    print(f"Database last recorded location: {last_location_data}")

                    last_location = ScrapeLast(self.handle).get_last()[0]
                    print(f"Instagram last posted location: {last_location}")

                        # Check up to date
                    if last_location_data == last_location:
                        print("Database is up to date!")
                        outdated = False
#____________________________________________________________________________________________________4x4theboiz
                       # Check up to date - 4x4theboiz
                    elif last_location_data == 'Moremi Game Reserve':
                        print("4x4thboiz special exception: Database is up to date!")
                        outdated = False
#____________________________________________________________________________________________________4x4theboiz
                    else:
                        print("Uh oh! we need to update table")

                        # scrape latest data
                        print(f"Starting  Scrape: @{self.handle}")

                        data = Scrape(self.handle).get_locations()
                        locations = data[0]
                        links = data[1]
                        latitudes = data[2]
                        longitudes = data[3]
                        #print(locations[0])
                        connection = sqlite3.connect("posts.db")
                        for i in range(0, len(locations), 1):
                            try:
                                sql = f"""INSERT INTO `{self.handle}` (`location`,`link`,`latitude`,`longitude`) VALUES ("{locations[i]}","{links[i]}","{latitudes[i]}","{longitudes[i]}")"""
                                #print(sql)
                                connection.execute(sql)
                                connection.commit()
                                # print("Table populated")
                                # connection.close()
                            except:
                                pass

                        print("Table updated")
                        outdated = False
                        connection.close()
                        print("connection closed")

                        
                except:
                    print("Uh oh! we need to populate the table for the first time")


                    # scrape latest data
                    print(f"Starting  Scrape: @{self.handle}")

                    data = Scrape(self.handle).get_locations()
                    locations = data[0]
                    links = data[1]
                    latitudes = data[2]
                    longitudes = data[3]
                    print(locations[0])
                    connection = sqlite3.connect("posts.db")
                    for i in range(0, len(locations), 1):
                        try:
                            sql = f"""INSERT INTO `{self.handle}` (`location`,`link`,`latitude`,`longitude`) VALUES ("{locations[i]}","{links[i]}","{latitudes[i]}","{longitudes[i]}")"""
                            print(sql)
                            connection.execute(sql)
                            connection.commit()
                            # print("Table populated")
                            # connection.close()
                        except:
                            pass


            # create table
            except:
                print("table needs to be created")
                # create table
                sql = f"""CREATE TABLE "{self.handle}" ("location" REAL UNIQUE, "link" REAL UNIQUE, "latitude" REAL UNIQUE, "longitude" REAL UNIQUE);"""
                print(sql)
                connection = sqlite3.connect("posts.db")
                connection.execute(sql)
                connection.commit()
                connection.close()
                print("Table created")
                # print("Error, table already exists or error with database")


if __name__ == "__main__":
    datacheck = DataCheck("photos").db_check()
