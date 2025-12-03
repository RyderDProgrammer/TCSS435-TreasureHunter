class TileColors:
    @staticmethod
    def get_path_color(tile_val, is_player2, is_start1, is_start2, fog_of_war, stepped_on):
        if tile_val == 'X':
            if fog_of_war and not stepped_on:
                # In fog of war, don't reveal trap until human steps on it
                return 'lightblue' if is_player2 else '#3544CA'
            # Trap shows player color when stepped on
            return 'lightblue' if is_player2 else '#3544CA'
        elif tile_val == 'T':
            # Player 1 (dark blue) or Player 2 (light blue) - green only when both step on it
            return 'lightblue' if is_player2 else '#3544CA'
        elif tile_val == 'S':
            if is_start1:
                return '#3544CA'
            elif is_start2:
                return 'lightblue'
            return 'blue'
        return 'lightblue' if is_player2 else '#3544CA'

    @staticmethod
    def get_mixed_path_color(tile_val, is_start1, is_start2, fog_of_war, stepped_on):
        if tile_val == 'X':
            if fog_of_war and not stepped_on:
                return 'lightblue'
            # Both players stepped on trap - show purple
            return 'purple'
        elif tile_val == 'T':
            return 'green'
        elif tile_val == 'S':
            if is_start1:
                return '#3544CA'
            elif is_start2:
                return 'lightblue'
            return '#5B6FC9'
        return '#5B6FC9'
