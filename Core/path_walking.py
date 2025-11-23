from matplotlib.animation import FuncAnimation


class PathWalking:
    def __init__(self, gui_manager):
        self.gui = gui_manager
        self.animation = None
        self.animating = False

    def start(self):
        if self.animating:
            return

        self.animating = True
        self.gui._clear_and_setup_axes()
        self.gui._draw_grid_tiles()
        self.gui.fig.canvas.draw_idle()

        moves_p1 = 1
        moves_p2 = 1
        processed = [False]

        def animate(frame):
            nonlocal moves_p1, moves_p2

            if frame == 0 and processed[0]:
                return
            if frame == 0:
                processed[0] = True

            if frame % 2 == 0:
                if moves_p1 < len(self.gui.ai_full_path):
                    self.gui.ai_solution_path = self.gui.ai_full_path[:moves_p1 + 1]
                    self.gui._redraw_grid()
                    moves_p1 += 1
            else:
                if moves_p2 < len(self.gui.ai_full_path_p2):
                    self.gui.ai_solution_path_p2 = self.gui.ai_full_path_p2[:moves_p2 + 1]
                    self.gui._redraw_grid()
                    moves_p2 += 1

            if moves_p1 >= len(self.gui.ai_full_path) and moves_p2 >= len(self.gui.ai_full_path_p2):
                self.animating = False
                if self.animation:
                    self.animation.event_source.stop()

        max_frames = (len(self.gui.ai_full_path) - 1 + len(self.gui.ai_full_path_p2) - 1) * 2
        self.animation = FuncAnimation(self.gui.fig, animate, frames=max_frames,
                                      interval=50, repeat=False, blit=False)
        self.gui.fig.canvas.draw_idle()

    def stop(self):
        self.animating = False
        if self.animation:
            self.animation.event_source.stop()
            self.animation = None
