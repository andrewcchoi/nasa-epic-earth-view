"""
Created by: Andrew Choi
Created Date: 8/27/2020
Modified Date: 8/31/2020
Version: 0.1
Creates GIF of rotating earth with
Earth Polychromatic Imaging Camera (EPIC)
"""

import tkinter as tk
import pandas as pd
import requests
import json
import imageio
import datetime as dt
from itertools import repeat
import multiprocessing
from multiprocessing import Pool
from skimage import transform, io
from PIL import Image
from pathlib import Path
import sys
import re
import urllib.request

# opens window to show gif
root = tk.Tk()


def update(id):
    # function to run gif in window
    frame = frames[id]
    print(id)
    if id == img_frames - 1:
        id = 0
    else:
        id += 1
    label.configure(image=frame)
    root.after(100, update, id)


def rate_limit_check(response):
    # checks rate limit for api, default allowance 1000
    if response.status_code == 429:
        print('Reach rate limit of 1,000')
        print(response.json())
        return True


def dl_image(img_name, date, collection, url, api_key):
    # download images of earth
    year = pd.to_datetime(date).year
    month = f'{pd.to_datetime(date).month:02d}'
    day = f'{pd.to_datetime(date).day:02d}'
    # saving image
    img_url = \
        f'{url}/archive/{collection}/{year}/{month}/{day}/png/{img_name}.png{api_key}'
    img_data = requests.get(img_url).content
    with open(f'images/{collection}/{img_name}.png', 'wb') as handler:
        handler.write(img_data)
    print(img_url)
    print(str('i') + ':', img_name)


# creates list of image names and dates
try:
    if __name__ == '__main__':
        # default values
        start_time = dt.datetime.now()  # records start time
        img_names = []
        img_dates = []
        images = []
        img_size = 500
        key = False
        date_range = True
        collection = 'natural'

        # verify directory and create new folder
        Path(rf'./images/{collection}').mkdir(parents=True, exist_ok=True)

        # determines base url based on key
        if key is False:
            # no api key
            url = 'https://epic.gsfc.nasa.gov'
            api_key = ""
        else:
            # with api key
            url = f'https://api.nasa.gov/EPIC'
            api_key = f'?api_key={key}'

        # checking if rate limit is reached
        if rate_limit_check(requests.get(f'{url}/api/{collection}/available{api_key}')):
            sys.exit()

        # print(f'Getting date ranges from {url}/api/{collection}/available{api_key}')
        data_range = json.loads(requests.get(f'{url}/api/{collection}/available{api_key}').text)

        # determine number of dates
        if date_range is False:
            data_len = len(data_range) - 1
            date_list = data_range
        elif date_range is True:
            data_len = 1
            date_list = data_range[-1:]

        # print(f'Getting date ranges from {url}/api/{collection}/available{api_key}')
        data_range = json.loads(requests.get(f'{url}/api/{collection}/available{api_key}').text)
        date_list = data_range[-1:]

        # connecting to api, converting json text, counting number of images
        print(f'Getting response from {url}/api/{collection}/date/{date_list[0]}{api_key}')
        response = requests.get(f'{url}/api/{collection}/date/{date_list[0]}{api_key}')
        data = json.loads(response.text)

        for x in data:
            img_names.append(x['image'])
            img_dates.append(x['date'])

        with Pool(multiprocessing.cpu_count()) as p:
            img_results = \
                p.starmap(dl_image, zip(img_names, img_dates, repeat(collection), repeat(url), repeat(api_key)))

        fp_gif = f'images/{collection}/earth{img_size}' \
                 f'_{pd.to_datetime(img_dates[-1]).year}' \
                 f'{pd.to_datetime(img_dates[-1]).month:02d}' \
                 f'{pd.to_datetime(img_dates[-1]).day:02d}.gif'

        print("Resizing and Creating GIF...")
        print(len(img_names), 'frames')
        print(f'GIF filename: {fp_gif}')

        for i in img_names:
            img_name = i
            img = io.imread(f'images/{collection}/{i}.png')
            small_img = transform.resize(img, (img_size, img_size), mode='symmetric', preserve_range=True)
            images.append(small_img)

        imageio.mimsave(fp_gif, images)
        img_obj = Image.open(fp_gif)

        if img_obj.is_animated:
            img_frames = img_obj.n_frames
            frames = [tk.PhotoImage(file=fp_gif,
                                    format='gif -index %i' % i) for i in range(img_frames)]

        # record time finished
        end_time = dt.datetime.now()

        # gif window
        label = tk.Label(root)
        label.pack()
        root.after(0, update, 0)
        root.lift()
        root.mainloop()

        print(f'You just created a WORLD!', f'{start_time}', f'{end_time}')

except Exception as e:
    print(e)
