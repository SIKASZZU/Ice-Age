class Framerate:
    def __init__(self):
        self.fps_list = []
        self.frame_counter = 0
        self.smoothing_window = 1000

    def update(self, current_fps):
        self.frame_counter += 1

        # Only update every N frames to reduce noise
        if self.frame_counter % 34 == 0:  # Update every 35 frames
            self.fps_list.append(current_fps)

            # Limit the size of the FPS list
            if len(self.fps_list) > self.smoothing_window:
                self.fps_list.pop(0)

    def get_fps_statistics(self):
        if not self.fps_list:
            return 0, 0, 0

        # Calculate smoothed statistics
        smoothed_fps = sum(self.fps_list) / len(self.fps_list)
        min_fps = min(self.fps_list)
        max_fps = max(self.fps_list)
        return int(smoothed_fps), int(min_fps), int(max_fps)

    def display_fps_statistics(self):
        avg_fps, min_fps, max_fps = self.get_fps_statistics()
        try:
            current_fps = int(self.fps_list[-1])
        except IndexError:
            current_fps = 0
        fps_text = f"FPS {current_fps} [Avg: {avg_fps}, Min: {min_fps}, Max: {max_fps}]"
        return fps_text
