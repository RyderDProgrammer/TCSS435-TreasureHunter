from matplotlib.widgets import Button


class ModeSelector:
    playerColors = ['#3544CA', 'lightblue']
    def __init__(self, fig, ax):
        self.fig = fig
        self.ax = ax
        self.ax_human = None
        self.ax_ai = None
        self.btn_human = None
        self.btn_ai = None

    def show_selection(self, on_selection_callback):
        self.ax.clear()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.axis("off")

        self.ax.text(5, 7, 'Select Player Mode',
                    ha='center', va='center',
                    fontsize=24, fontweight='bold')

        self.ax_human = self.fig.add_axes([0.25, 0.4, 0.2, 0.1])
        self.btn_human = Button(self.ax_human, 'Human', color=self.playerColors[0], hovercolor=self.playerColors[1])

        self.ax_ai = self.fig.add_axes([0.55, 0.4, 0.2, 0.1])
        self.btn_ai = Button(self.ax_ai, 'AI', color=self.playerColors[0], hovercolor=self.playerColors[1])

        def on_human_click(event):
            self._set_mode('human', True, on_selection_callback)

        def on_ai_click(event):
            self._set_mode('ai', False, on_selection_callback)

        self.btn_human.on_clicked(on_human_click)
        self.btn_ai.on_clicked(on_ai_click)

        self.fig.canvas.draw_idle()

    def _set_mode(self, player_mode, fog_of_war, callback):
        self.btn_human.disconnect_events()
        self.btn_ai.disconnect_events()
        self.ax_human.remove()
        self.ax_ai.remove()
        callback(player_mode, fog_of_war)
        self.fig.canvas.draw_idle()
