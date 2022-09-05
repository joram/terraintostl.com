from stl_util import build_stl

if __name__ == '__main__':
    VI = [
        [50.7573, -129.3420],
        [48.4292, -124.8486],
        [48.2393, -123.7500],
        [48.4073, -122.9370],
        [49.1026, -123.4753],
        [50.2332, -125.1453],
        [50.8129, -127.1008],
        [51.1173, -128.5730],
        [51.0483, -129.1113],
    ]
    build_stl(VI, "vancouver_island_bounded.stl", resolution=0.005, z_scale=0.00005, fit_to_region=True)