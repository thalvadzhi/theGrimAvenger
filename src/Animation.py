

class Animation:

    def __init__(self, mutator, duration, value_from, value_to):
        self.mutator = mutator
        self.duration = duration
        self.value_from = value_from
        self.value_to = value_to

    def play(self, start_time):
        self.mutator(self.value_from)
        frame = self.calculate_frame_difference(frame)
        elapsed_time = 0
        bent_fraction = 0
        while elapsed_time < self.duration:
            facing = -1 if self.facing is "left" else 1
            elapsed_time = clock.get_ticks() - start_time
            fraction = elapsed_time / duration - bent_fraction
            if elapsed_time > duration:
                fraction = 1 - bent_fraction
            bent_fraction += fraction
            for joint in self.joints:
                self.joints[joint].bent_keeping_angles(frame[joint] * fraction * facing)
            self.rotate(frame["slope"] * fraction * -facing)
            yield
        raise StopIteration



    
