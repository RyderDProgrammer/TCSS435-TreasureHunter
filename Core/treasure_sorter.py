import math
import numpy


class TreasureSorter:
    @staticmethod
    def sort_by_distance(treasures, start_pos):
        treasure_distances = {}
        for treasure in treasures:
            distance = math.sqrt(
                (treasure[0] - start_pos[0]) ** 2 +
                (treasure[1] - start_pos[1]) ** 2
            )
            treasure_distances[treasure] = distance

        keys = list(treasure_distances.keys())
        values = list(treasure_distances.values())
        sorted_indices = numpy.argsort(values)
        return {keys[i]: values[i] for i in sorted_indices}
