import sys
import argparse
from cjio import cityjson
from cjio.models import CityObject, Geometry
import json
import geopandas as gpd
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser("shp3d2cityjson.py")
    parser.add_argument(
        "--input", "-i", help="input", default="marseille_urbain_2a_20240527_reg_fp.shp"
    )
    parser.add_argument(
        "--bid_field", "-b", help="building id field name", default="BID"
    )
    parser.add_argument(
        "--surf_type_field", "-s", help="surface type field name", default="TYPE"
    )
    parser.add_argument(
        "--wall_type_value", "-w", help="wall surface type value", default="W"
    )
    parser.add_argument(
        "--ground_type_value", "-g", help="ground surface type value", default="G"
    )
    parser.add_argument(
        "--roof_type_value", "-r", help="roof surface type value", default="R"
    )
    parser.add_argument(
        "--output", "-o", help="output CityJSON file", default="output.city.json"
    )
    return parser.parse_args()


def fill_surf_lists(feature, walls, grounds, roofs, args):
    if feature["properties"][args.surf_type_field] == args.wall_type_value:
        walls.append([list(x) for x in feature["geometry"]["coordinates"]])
    elif feature["properties"][args.surf_type_field] == args.ground_type_value:
        grounds.append([list(x) for x in feature["geometry"]["coordinates"]])
    elif feature["properties"][args.surf_type_field] == args.roof_type_value:
        roofs.append([list(x) for x in feature["geometry"]["coordinates"]])


def main():

    args = parse_args()

    # load input file
    gdf = gpd.read_file(args.input)
    gdf = gdf.sort_values(by=[args.bid_field])
    crs_code = int(gdf.crs.to_epsg())

    # Create empty cityjson structure
    cj = cityjson.CityJSON()
    cj.set_epsg(crs_code)

    # iterate over buildings
    bid = gdf.iloc[0][args.bid_field]
    walls, roofs, grounds = [], [], []
    count = 0
    for f in tqdm(gdf.iterfeatures(), total=gdf.shape[0]):

        if f["properties"][args.bid_field] == bid:
            fill_surf_lists(f, walls, grounds, roofs, args)

        elif (f["properties"][args.bid_field] != bid) or (count == gdf.shape[0] - 1):

            # Empty cityobject building with id
            co = CityObject(id=bid)
            co.type = "Building"

            # Add attributes
            co_attrs = {
                "building_name": bid,
            }
            co.attributes = co_attrs

            # Instantiate geometry
            geom = Geometry(type="Solid", lod=2)
            bdry = walls + grounds + roofs
            geom.boundaries.append(bdry)

            # add surfaces index
            geom.surfaces[0] = {
                "surface_idx": [[0, x] for x in range(len(walls))],
                "type": "WallSurface",
            }
            geom.surfaces[1] = {
                "surface_idx": [[0, len(walls) + x] for x in range(len(grounds))],
                "type": "GroundSurface",
            }
            geom.surfaces[2] = {
                "surface_idx": [
                    [0, len(walls) + len(grounds) + x] for x in range(len(roofs))
                ],
                "type": "RoofSurface",
            }
            co.geometry.append(geom)

            # Add cityobject to cityjson cityobjects list
            cj.cityobjects[co.id] = co

            # continue with next building
            walls.clear()
            roofs.clear()
            grounds.clear()
            bid = f["properties"][args.bid_field]
            fill_surf_lists(f, walls, grounds, roofs, args)

        count += 1

    # Add all buildings
    cj.add_to_j()
    # Update bbox
    cj.update_bbox()
    # Add transform and shift coordinates
    cj.compress()
    # write result to cityjson file
    with open(args.output, "w") as fout:
        json_str = json.dumps(cj.j, indent="\t")
        fout.write(json_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())
