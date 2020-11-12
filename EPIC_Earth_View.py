"""
Created by: Andrew Choi
Created Date: 8/27/2020
Modified Date: 8/28/2020
Version: 0.31
Creates GIF of rotating earth with
Earth Polychromatic Imaging Camera (EPIC)
"""

import tkinter as tk
import pandas as pd
import requests
import json
import imageio
import datetime as dt
from skimage import transform, io
from PIL import Image
import sys

# opens window to show gif
root = tk.Tk()


def earth_view(collection, date_range=None, key=None):
    # function requires collection [natural/enhanced], optional: date_range default None or 'all', key for api key
    start_time = dt.datetime.now()  # records start time

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
        try:
            print(response.headers['X-RateLimit-Remaining'])
        except Exception:
            pass

        if response.status_code == 429:
            print('Reach rate limit of 1,000')
            print(response.json())
            return True

    # determines base url based on key
    if key is not None:
        # with api key
        url = f'https://api.nasa.gov/EPIC'
        api_key = f'?api_key={key}'
    else:
        # no api key
        url = 'https://epic.gsfc.nasa.gov'
        api_key = ""

    # checking if rate limit is reached
    if rate_limit_check(requests.get(f'{url}/api/{collection}/available{api_key}')) and key is not None:
        sys.exit()

    print(f'Getting date ranges from {url}/api/{collection}/available{api_key}')
    data_range = json.loads(requests.get(f'{url}/api/{collection}/available{api_key}').text)

    # determine number of dates
    if date_range == 'all':
        data_len = len(data_range) - 1
        date_list = data_range
    else:
        data_len = 1
        date_list = data_range[-1:]

    # create empty list for images and image pixel size
    images = []
    img_size = 500

    # loop through all dates
    for n in range(data_len):
        # connecting to api, converting json text, counting number of images
        print(f'Getting response from {url}/api/{collection}/date/{date_list[n]}{api_key}')
        response = requests.get(f'{url}/api/{collection}/date/{date_list[n]}{api_key}')
        data = json.loads(response.text)
        img_index = range(len(data))
        print('Received Response...')

        # if rate limit is not reached continue to downloading images
        print("Exporting JSON file and saving images...")
        if rate_limit_check(response) is not True:
            try:
                # determine file name and path, export json and csv files, save images
                for x in data:
                    # exit loop if rate limit is reached or request is not ok
                    if response.status_code == 429:
                        print('X-RateLimit-Remaining:',response.headers.get('X-RateLimit-Remaining'))
                        print(response['error']['code'])
                        break
                    if response.status_code != 200:
                        print(response.status_code)
                        print(response.json())
                        break

                    year = pd.to_datetime(x['date']).year
                    month = f'{pd.to_datetime(x["date"]).month:02d}'
                    day = f'{pd.to_datetime(x["date"]).day:02d}'

                    # exporting json and csv file
                    df_json = pd.DataFrame(response.json())
                    df_data = pd.DataFrame(data)
                    df_data.to_csv(f'data/EPIC_{collection}_data_{year}{month}{day}.csv', index=True, header=True)
                    df_json.to_json(
                        rf'c:\users\lilco\Documents\Python Projects\API'
                        rf'\data\EPIC_{collection}_response_{year}{month}{day}.json')

                    # saving image
                    img_name = x['image']
                    img_url = \
                        f'{url}/archive/{collection}/{year}/{month}/{day}/png/{img_name}.png{api_key}'
                    img_data = requests.get(img_url).content
                    with open(f'images/{collection}/{img_name}.png', 'wb') as handler:
                        handler.write(img_data)
                    print(img_url)

                print("Resizing and Creating GIF...")
                for i in img_index:
                    img_name = data[i]['image']
                    img = io.imread(f'images/{collection}/{img_name}.png')
                    small_img = transform.resize(img, (img_size, img_size), mode='symmetric', preserve_range=True)
                    images.append(small_img)
                    print(str(i) + ':', img_name)

            except Exception as e:
                # continue current loop on error
                end_time = dt.datetime.now()
                print(e, start_time, end_time, sep='\n')
                continue

    print("Saving GIF...")
    fp_gif = f'images/{collection}/earth{img_size}_{year}{month}{day}.gif'
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

    print(f'{fp_gif} created!', f'{start_time}', f'{end_time}', sep='\n')


# # Choose between natural or enhanced images of earth
collection = 'natural'
# collection = 'enhanced'

earth_view(collection)
