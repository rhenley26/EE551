#Ryan Henley
#Professor Mukund
#EE-551-WS: Engineering Programming: Python
#18 December 2020

#I pledge my honor that I have abided by the Stevens Honor System. -Ryan Henley

#Project Description:
#PyBox is a virtual media player that allows the user to
#enter whatever song they would like to listen to (or video they would like to watch)
#and the program will search for the first 5 results on YouTube to display to the user
#The information from the search done with the youtube_search library is stored in 
#the SearchOutput.txt file, and this information is read from and displayed for the user
#The user will copy the shortened url from the video they like, enter it in the terminal,
#and the program will play the video (with the help of the python-vlc and pafy libraries)
#Once the video is over, the user can choose whether or not to look up another video

#Third-Party Libraries Used: 
#python-vlc - https://pypi.org/project/python-vlc/
#pafy - https://pypi.org/project/pafy/
#youtube-search - https://pypi.org/project/youtube-search/

#These are some of the links that helped me bring this project together:
#https://pypi.org/project/youtube-search-python/
#https://www.geeksforgeeks.org/playing-youtube-video-using-python/
#https://stackoverflow.com/questions/49354232/how-to-stream-audio-from-a-youtube-url-in-python-without-download
#https://github.com/joetats/youtube_search/blob/master/youtube_search/__init__.py

#IMPORTANT: There is an issue with this program on visual studio code where 
#the vlc media player will crash after a certain amount of time.
#However, I haven't had any issues running this program multiple times through my
#ubuntu terminal, meaning that this is most likely a visual studio code issue. 

import vlc
import pafy 
import urllib.parse
import urllib.request
import re 
import os
from youtube_search import YoutubeSearch

#User Prompt
Status = True
while Status == True:
    print("Welcome to the PyBox! A jukebox for your Python machine!")
    print("Please enter the video you would like to watch!")
    song_name = input("Enter here: ")


#Step 1: Search User Input in Youtube
    #Part a -> Perform the Youtube Search for the song
    videos = YoutubeSearch(song_name, max_results = 5).to_dict()

    #Part b -> Store results into txt file
    with open('SearchOutput.txt', 'w+') as filehandle:
        for listitem in videos:
            filehandle.write('%s\n' % listitem)

    #Part c -> Read out the titles and url-suffixes from the txt file
    res = len(re.findall(r'\w+', song_name)) #Uses length of song name to determine title of video
    with open("SearchOutput.txt") as openfile:
        for line in openfile:
            print(line.split(' ')[6:(int(res) + 12)])
            for part in line.split():
                if "/watch" in part:
                    print(part)


    #Step 2: Allow user to select the desired video
    print("Please copy and paste the URL Suffix of the video you would like to watch!")
    video_url = input("Enter here: ")

    #Step 3: Play audio from video
    #Creating the url for the vlc media player
    url = "https://www.youtube.com" + video_url
    print(url)

    #Setup for the media player using pafy and vlc
    output = pafy.new(url)
    best = output.getbest()
    playurl = best.url
    ins = vlc.Instance()
    player = ins.media_player_new()

    #Checks to make sure that the url provided is working
    code = urllib.request.urlopen(url).getcode()
    if str(code).startswith('2') or str(code).startswith('3'):
        print('Stream is working')
    else:
        print('Stream is dead')

    #Initializes the vlc media player
    Media = ins.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()

    #Checks to make sure the player is running, and while doing so it displays the current video
    good_states = ["State.Playing", "State.NothingSpecial", "State.Opening"]
    while str(player.get_state()) in good_states:
        print("Now playing: " + song_name)
    print('Done Playing. Current state = {}'.format(player.get_state()))
    player.stop()

    #Clears the terminal
    os.system('cls||clear')

    #Step 4: Check to see if user would like to keep listening to music
    print("Would you like to see another video? Please enter yes or no below")
    choice = input("Enter here: ")
    if choice == "Yes" or choice == "y" or choice == "YES" or choice == "yes":
        Status = True
    else:
        print("Thank you for using PyBox!")
        Status = False
