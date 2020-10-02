# -*- coding: utf-8 -*-

# Importing libraries

import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

# URL validator

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
#urlparse() function parses a URL into six components, 
#we just need to see if the netloc (domain name) and scheme (protocol) are there.


#core function that grabs all image URLs of a web page
def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    #this soup object contains the HTML content of the given url
    
    urls = []
    #find all the images in the url
    
    """
    1. Retrieve all img elements as a Python list.
    2. tqdm is used to wrap everything and display in a progress bar
    3. The src attribute helps to grab the image url
    4. Skipping those image urls that dont have the src attribute
    
    """
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        
    # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
    
    
        #Removing those image urls that contain HTTP GET KEY VALUE pairs
        """
        1. Getting the position of '?' character, then removing everything after it
        2. Raise a value error if there isn't any
        
        """
        try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
                
        except ValueError:
            pass
    
    # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
        
    return urls


# Function to download the images
def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
        
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", 
                    total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    
    # Opening the folder and writing the files
    with open(filename, "wb") as f:
        
        for data in progress:
            # write data to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
            

# Main function
def main(url, path):

    # get all images
    imgs = get_all_images(url)

    for img in imgs:
        # Download each image
        download(img, path)
        

        
#Downloading images
# Just provide the url of the website and path to where the images will be stored and the code will do the rest
main("https://webneel.com/nature-photography-photos", "Desktop/Data Science Projets/Style transfer artworks/images")


