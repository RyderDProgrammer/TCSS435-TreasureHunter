from Core.tile_colors import TileColors


class TileRenderer:
    @staticmethod
    def get_tile_appearance(val, i, j, grid_instance, fog_of_war, human_player, ai_path, ai_path_p2, noisy_val=None):
        is_on_ai_path = ai_path and (i, j) in ai_path
        is_on_ai_path_p2 = ai_path_p2 and (i, j) in ai_path_p2
        is_on_human_path = human_player.current_path and (i, j) in human_player.current_path

        is_start1 = grid_instance and (i, j) == grid_instance.start1
        is_start2 = grid_instance and (i, j) == grid_instance.start2

        if fog_of_war and not is_start1 and not is_start2 and (i, j) not in human_player.revealed_tiles:
            # In fog of war, unrevealed tiles show as unknown - don't reveal AI path
            return '?', 'lightgray', 'black'

        # Use noisy value if provided, otherwise use actual value
        display_value = noisy_val if noisy_val is not None else val

        if fog_of_war and val == 'X' and (i, j) not in human_player.stepped_on_tiles:
            display_val = ' '
            color = 'white'
            fg = 'black'
        else:
            display_val = display_value
            if display_value == 'S':
                if is_start1:
                    color = '#3544CA'
                    fg = 'white'
                elif is_start2:
                    color = 'lightblue'
                    fg = 'black'
                else:
                    color = 'blue'
                    fg = 'white'
            else:
                color = {'T': 'gold', 'X': 'red', '#': 'gray'}.get(display_value, 'white')
                fg = 'white' if display_value in ['T', 'X', '#'] else 'black'

        stepped_on = (i, j) in human_player.stepped_on_tiles
        if is_on_human_path and is_on_ai_path:
            color = TileColors.get_mixed_path_color(display_value, is_start1, is_start2, fog_of_war, stepped_on)
        elif is_on_ai_path and is_on_ai_path_p2:
            color = TileColors.get_mixed_path_color(display_value, is_start1, is_start2, fog_of_war, stepped_on)
        elif is_on_human_path:
            color = TileColors.get_path_color(display_value, True, is_start1, is_start2, fog_of_war, stepped_on)
        elif is_on_ai_path:
            color = TileColors.get_path_color(display_value, False, is_start1, is_start2, fog_of_war, stepped_on)
        elif is_on_ai_path_p2:
            color = TileColors.get_path_color(display_value, True, is_start1, is_start2, fog_of_war, stepped_on)

        return display_val, color, fg
