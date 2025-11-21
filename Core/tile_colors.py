class TileColors:
    @staticmethod
    def get_path_color(tile_val, is_human, is_start1, is_start2, fog_of_war, stepped_on):
        if tile_val == 'X':
            if fog_of_war and is_human and not stepped_on:
                return 'lightblue'
            return 'cyan'
        elif tile_val == 'T':
            return 'green' if is_human else '#3544CA'
        elif tile_val == 'S':
            if is_start1:
                return '#3544CA'
            elif is_start2:
                return 'lightblue'
            return 'blue'
        return 'lightblue' if is_human else '#3544CA'

    @staticmethod
    def get_mixed_path_color(tile_val, is_start1, is_start2, fog_of_war, stepped_on):
        if tile_val == 'X':
            if fog_of_war and not stepped_on:
                return 'lightblue'
            return 'cyan'
        elif tile_val == 'T':
            return 'green'
        elif tile_val == 'S':
            if is_start1:
                return '#3544CA'
            elif is_start2:
                return 'lightblue'
            return '#5B6FC9'
        return '#5B6FC9'
