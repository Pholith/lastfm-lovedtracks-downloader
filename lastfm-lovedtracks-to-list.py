from bs4 import BeautifulSoup # for scrapping
import requests # for scrapping
import sys
import time 
from downloader import bcolors # for passing arguments from the console

def generate_list_from_lasftfm_lovedtracks(username):
    print(f"Starting to generate a list with all {username}'s loved tracks...")

    lastpage = 1

    main_url = f"https://www.last.fm/user/{username}/loved"
    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    if (soup == None):
        return
    
    element = soup.find("ul", attrs={'class': "pagination-list"})
    if element == None:
        # it only has 1 page of loved tracks!
        pass
    else:
        element = element.find_all("li")        
        for li in element:
            try: #there are a bunch of non number ones
                navbutton_pagenumber = int(li.text)
                if navbutton_pagenumber > lastpage:
                    lastpage = navbutton_pagenumber
            except:
                pass

    print(f"{username} has {lastpage} pages of loved tracks!")

    loved_tracks = []
    for pagenumber in range(lastpage):
        pagenumber += 1 # pages are 1 based
        print(f"scrapping page {pagenumber} of {lastpage}...")
        url = f"{main_url}?page={pagenumber}"

        # Adds some header to avoid being blocked by last.fm for too many requests
        Headers = {

                # Paste your cookies here from firfox if last.fm blocks you for too many requests.
                'cookie': ''
            }

        page = requests.get(url, headers=Headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup = soup.find("tbody", attrs={'data-playlisting-add-entries': ""})

        if (soup == None):
            print(f"{bcolors.WARNING} Couldn't find page number ! Last.fm might have blocked you for being a bot. Try to copy your cookies from Firefox and paste them in the Headers variable in this script. {bcolors.ENDC}")
            return

        # TODO: There are a lot of tracks that don't have a youtube link! 
        # tracks = soup.find_all("a", attrs={'data-youtube-url': True})

        tracks = soup.find_all("tr", attrs={'class': "chartlist-row"})

        for track in tracks:
            
            artist_name = track.find("td", attrs={'class': "chartlist-artist"}).find("a").get("title")
            track_name = track.find("td", attrs={'class': "chartlist-name"}).find("a").get("title")
            track_url = None

            youtube_element = track.find("td", attrs={'class': "chartlist-play"}).find("a", attrs={'data-youtube-url': True})
            if youtube_element != None:
                track_url = youtube_element["data-youtube-url"]

            space = " || "
            loved_tracks.append(f"{artist_name}{space}{track_name}{space}{track_url}")
        
        time.sleep(1)


    print(f"{username} has a total of {len(loved_tracks)} loved tracks!")

    with open(f"{username}-lovedtracks.txt", "w", encoding="utf-8") as listfile:
        listfile.write("\n".join(loved_tracks))

    print(" ")
    print(f"Now for downloading these songs, run 'python downloader.py {username}-lovedtracks.txt'")


if __name__ == "__main__":
    try:
        username = sys.argv[1]
    except:
        username = "smalldeadinsect"
    generate_list_from_lasftfm_lovedtracks(username)