import os
import re 
import requests
from urllib import request
from urllib import error
from bs4 import BeautifulSoup
import time


class Movie:
    __folder=""
    __movieName=""
    __releaseYear="
    __movieType=""
    __Sound=""
    __video=""

    def __init__(self,folder):
        m=re.search("([a-zA-Z0-9\.]+)\.(\d{4})\.([0-9]+p)\.([a-zA-Z0-9\.-]+)\.([a-zA-Z0-9]+)",folder)
        self.__movieName=m.group(1).replace(".","-").lower()
        self.__folder=folder
        self.__releaseYear=m.group(2)

    def getMovieName(self):
        return self.__movieName

    def getFolder(self):
        return self.__folder

    def getReleaseYear(self):
        return self.__releaseYear


def getFolder():
    folder_list = []
    for root, dirs,files in os.walk("movies/",topdown=False):
        for name in dirs:
            folder_list.append(name)
    return folder_list

def getMovies():
    movie_list=[]
    for folder in getFolder():
    # m=re.search("([a-zA-Z0-9\.]+)\.(\d{4})\.([0-9]+p)\.([a-zA-Z0-9\.-]+)\.([a-zA-Z0-9]+)", movie)
    # print(m.group(1))
    # print(m.group(2))
    # print(m.group(3))
    # print(m.group(4))
    # print(m.group(5))
        movie_list.append(Movie(folder))
    return movie_list

link="https://subscene.com/subtitles/" 

def getHeader():
    header={'user-agent':'Mozilla/5.0 (Linux; Android 5.1; Lenovo P1ma40 Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36'}
    return header
 
def getMoviePage(movie):
    try:
        movieLink1 = link+str(movie.getMovieName())+"-"+str(movie.getReleaseYear()+"/English")
        #print(movieLink1)
        time.sleep(3)
        req=request.Request(str(movieLink1),headers=getHeader())
        response=request.urlopen(req)
        time.sleep(3)
        response_page=response.read()
        #print("found with date")
        return response_page
    except error.HTTPError as e:
        if(e.code==404):
            try:
                movieLink2 = link+str(movie.getMovieName()+"/English")
                #print(movieLink2)
                time.sleep(3)
                req=request.Request(str(movieLink2),headers=getHeader())
                response=request.urlopen(req)
                time.sleep(3)
                response_page=response.read()
                #print("found without date")
                return response_page
            except error.HTTPError as e:
                print(str(e.code)+movie.getMovieName())
        else:
            print(str(e.code)+movie.getMovieName())



def getMovieHtml(response_page):
    
    soup = ""

    if not response_page is None:
        soup= BeautifulSoup(response_page,"html.parser") 

    try:
        for page in soup.find_all('a'):
            print(page)
    except error.HTTPError as e:
        e.code
        '''
        try:
            if((str(response_page.contents[3].contents[0].strip())==str(movie.getFolder()).strip()) and str(y.contents[0]).strip()==language.strip()):
                href=['href']
                url=("https://subscene.com/"+href).strip()
                subtitlesLinks.append(str(url).strip())
                print()
        except IndexError as e:
            e
            break
        except: 
            print("error")
            '''
# for movie in getMovies():
#     if not getMoviePage(movie) is None:
#         print('Page')
for movie in getMovies():
    getMovieHtml(getMoviePage(movie))