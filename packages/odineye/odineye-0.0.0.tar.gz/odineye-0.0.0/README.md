# odineye

A package for downloading satellite maps. Odin sees everything.

## Installation

You can install `odineye` using pip:
```bash
pip install odineye
```

## Usage

`odineye` can be used to download satellite maps given location coordinates. 

You can specify the location by providing the latitude and longitude of the location in the next way:

Here is an example with the location in Vancouver, BC, Canada:
```python
from odineye.maps_downloaders.google_maps_downloader import GoogleMapsDownloader

north_latitude, east_longitude = (49.2806635, -123.1191798)
south_latitude, west_longitude = (49.2753833, -123.1042628)

downloader = GoogleMapsDownloader(download_threads=8)
map_picture = downloader(
	north_latitude,
	east_longitude,
	south_latitude,
	west_longitude,
	zoom=22,
	map_style="satellite",
	return_type="PIL",
)
map_picture.save("map.png")
```


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`odineye` was created by **[NaturalStupidlty](https://github.com/NaturalStupidlty)**.

It is licensed under the terms of the GNU General Public License v3.0 license.
