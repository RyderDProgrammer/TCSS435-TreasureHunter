from Algorithms import Alpha_Beta
class TitleFormatter:
    @staticmethod
    def format_player_stats(player_num, is_ai, info, is_human_cost=False):
        if is_human_cost:
            return f"Player {player_num} (Human) - Cost: {info}"

        runtime_str = f"{info.get('runtime', 0):.4f}s" if info.get('runtime', 0) > 0 else "N/A"
        heuristic_str = f"{info.get('heuristic'):.2f}" if info.get('heuristic') is not None else "N/A"
        pruned_str = str(info.get('pruned_branches')) if info.get('pruned_branches') is not None else "N/A"

        player_type = "AI" if is_ai else "Human"
        return (
            f"Player {player_num} ({player_type}) - Algorithm: {info.get('algorithm', 'None')} | "
            f"Cost: {info.get('cost', 0)} | "
            f"Runtime: {runtime_str} | "
            f"Expanded Nodes: {info.get('expanded_nodes', 0)} | "
            f"Heuristic: {heuristic_str} | "
            f"Pruned: {pruned_str} | "
            f"ABP Depth: {Alpha_Beta.MAX_DEPTH}"
        )

    @staticmethod
    def format_dual_title(player1_info, player2_info, player_mode, human_cost=None, noise_level='none'):
        player1_title = TitleFormatter.format_player_stats(1, True, player1_info)

        if player_mode == 'human':
            player2_title = TitleFormatter.format_player_stats(2, False, human_cost, is_human_cost=True)
        elif player_mode == 'ai' and player2_info:
            player2_title = TitleFormatter.format_player_stats(2, True, player2_info)
        else:
            player2_title = "Player 2 - N/A"

        # Add noise level indicator
        noise_display = noise_level.capitalize() if noise_level != 'none' else 'None'
        noise_info = f"Sensor Noise: {noise_display}"

        return f"{player1_title}\n{player2_title}\n{noise_info}"
