import time


class Timer:
    def __init__(self):
        self.times = []

    def save_time(self, explanation):
        self.times.append((time.time(), explanation))

    @property
    def total_duration(self):
        return self.times[-1][0] - self.times[0][0]

    def get_summary(self):
        start_time = self.times[0][0]
        return [
            '%6d ms - d %6s ms - %s' % (
                (t - start_time) * 1000,
                '%.2f' % ((t - self.times[i - 1][0]) * 1000),
                explanation,
            )
            for i, (t, explanation)
            in enumerate(self.times[1:], 1)
        ]
