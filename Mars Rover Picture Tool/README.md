# Mars Rover Picture Tool

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

A small tool to fetch and download latest images taken by rovers perseverance, curiosity, opprtunity and spirit on the surface of planet Mars. This Tool requires an active internet connection.

![Alt text](app.png?raw=true "MaRover Tool")

## How to Download

Download this project from here [Download MaRover Tool](https://downgit.github.io/#/home?url=https://github.com/pyGuru123/Python-Space-Science/tree/main/Mars%20Rover%20Picture%20Tool)

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following packages :-
* requests

```bash
pip install requests
```

This Tool uses NASA Mars Photos Api to fetch images. An Api key is necessary for doing this. Register for an Free API Key here : [NASA API](https://api.nasa.gov/)

After getting the api key, click settings or gear icon ⚙️ in the apps top right corner, paste the api key and then click save. Now you can run the tool.

## Usage

Click the application.py to open the app, select the rover from ribbon bar, select the camera, leave any camera if you don't know anything about the rover camera. Enter a sol value (integer) ( Martian day ), or a Earth Date of which you want to get the images, enter the number of images that you want to download, click fetch resources, once done click download and finally click open.

The minimum sol value is 1 i.e, the landing date of rover and max sol value is the last day of contact to earth. To get the maximum sol value see the bottom info bar below the rover picture.

In case, if the number of pictures taken is less than your entered value, only that amount of images will be downloaded.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.