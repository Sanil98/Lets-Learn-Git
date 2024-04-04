# # istic and has some basic problems but I'd like to learn how to do this properly.

# import requests
# from bs4 import BeautifulSoup

# # URL of the OpenSubtitles website
# url = "https://mkvcinemas.rsvp/captain-miller-2024/"

# # List of movies/shows
# movies = ["Captain Miller"]

# # Loop through each movie/show
# for movie in movies:
#     # Build the URL for the movie/show
#     movie_url = url + "?q=" + movie
    
#     # Request the URL
#     response = requests.get(movie_url)

#     # Parse the HTML content
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Find the download link
#     download_link = soup.find('a', {'class': 'download-subtitle'})['href']


#     # Download the subtitle file
#     subtitle_file = requests.get(download_link, allow_redirects=True)

# # Save the file
#     open('subtitle_file.srt', 'wb').write(subtitle_file.content)

import requests
from bs4 import BeautifulSoup

# URL of the OpenSubtitles website
url = "https://new.gdtot.dad/ondl"

# List of movies/shows
movies = ["Captain Miller"]

# Loop through each movie/show
for movie in movies:
    # Build the URL for the movie/show
    movie_url = url + "?q=" + movie
    
    # Request the URL
    response = requests.get(movie_url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the download link
    download_link_element = soup.find('a', {'class': 'download-subtitle'})

    # Check if the element was found
    if download_link_element:
        download_link = download_link_element['href']

        # Download the subtitle file
        subtitle_file = requests.get(download_link, allow_redirects=True)

        # Save the file
        open('subtitle_file.srt', 'wb').write(subtitle_file.content)
    else:
        print(f"Download link not found for {movie}")
