from __future__ import annotations

from numpy.random.mtrand import rand

from shapes import polygon2d
from numpy.random import rand, seed

from time import time_ns

from multiprocessing import Pool, cpu_count

def check_intersects(gon1 : polygon2d, gon2 : polygon2d):
    if gon1 != gon2:
        return gon1.has_intersect(gon2)
    else:
        return False

def main(use_mt = False, gon_qty = 100):
    mygons = []
    seed(7903214)

    start_time = time_ns()
    for _ in range(gon_qty):
        coords = rand(4, 2)
        mygon = polygon2d(*coords)
        mygons.append(mygon)
    pass
    finish_random_gen_time = time_ns()

    intersecting_gons = 0
    gon1 : polygon2d
    gon2 : polygon2d
    gon_pairs = []
    for gon1 in mygons:
        for gon2 in mygons:
            gon_pairs.append((gon1, gon2))

    if not use_mt:
        for pair in gon_pairs:
            if check_intersects(*pair):
                intersecting_gons += 1
    else:
        with Pool(cpu_count()) as p:
            results = p.starmap(check_intersects, gon_pairs)
            intersecting_gons = sum(results)


    finish_intersect_check_time = time_ns()

    total_time = (finish_intersect_check_time - start_time) / 10**9 # Total time in seconds
    rand_time = (finish_random_gen_time - start_time) / 10**9 # Time to generate polygons
    check_time = (finish_intersect_check_time - finish_random_gen_time) / 10**9 # Time to check for intersection

    print('Checked polygon quantity: '  + str(gon_qty))
    print('Using multithreading: ' + str(use_mt))
    print('Total time (s): ' + str(total_time))
    print('Random generating time (s): ' + str(rand_time))
    print('Check generating time (s): ' + str(check_time))
    print('Intersections found: ' + str(intersecting_gons))



if __name__ == '__main__': 
    for i in range(100, 600, 100):
        main(False, i)
        main(True, i)