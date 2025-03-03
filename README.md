# shp3d2cityjson

## About

* Input: A "3D shapefile" of buildings surfaces with an unique building identifier and a surface type (wall, ground, surface) attribute
* Output: A CityJSON file containing the same buildings
* Using: GeoPandas , cjio (develop branch), tqdm

## Setup

```
python3 -m venv env_dir
source env_dir/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

```
usage: shp3d2cityjson.py [-h] [--input INPUT] [--bid_field BID_FIELD] [--surf_type_field SURF_TYPE_FIELD] [--wall_type_value WALL_TYPE_VALUE]
                         [--ground_type_value GROUND_TYPE_VALUE] [--roof_type_value ROOF_TYPE_VALUE] [--output OUTPUT]

options:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        input
  --bid_field BID_FIELD, -b BID_FIELD
                        building id field name
  --surf_type_field SURF_TYPE_FIELD, -s SURF_TYPE_FIELD
                        surface type field name
  --wall_type_value WALL_TYPE_VALUE, -w WALL_TYPE_VALUE
                        wall surface type value
  --ground_type_value GROUND_TYPE_VALUE, -g GROUND_TYPE_VALUE
                        ground surface type value
  --roof_type_value ROOF_TYPE_VALUE, -r ROOF_TYPE_VALUE
                        roof surface type value
  --output OUTPUT, -o OUTPUT
                        output CityJSON file
```
