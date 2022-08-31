from stl_generator.stl_util import build_stl


if __name__ == '__main__':
    golden_hinde_region = [
        (49.6732, -125.7921),
        (49.6440, -125.7706),
        (49.6514, -125.7169),
        (49.6818, -125.7445),
    ]
    vancouver_island_region = [
        (50.7573, -129.3420),
        (48.4292, -124.8486),
        (48.2393, -123.7500),
        (48.4073, -122.9370),
        (49.1026, -123.4753),
        (50.2332, -125.1453),
        (50.8129, -127.1008),
        (51.1173, -128.5730),
        (51.0483, -129.1113),
    ]

    build_stl(golden_hinde_region, "golden_hinde.stl", resolution=0.001, z_scale=0.00001, )
    build_stl(vancouver_island_region, "vancouver_island.stl", resolution=0.002, z_scale=0.00002, fit_to_region=True)
