import time
from sys import stdout
from progress.bar import ChargingBar


class SmbProgressBase:
    def __init__(self):
        self.size = 0
        self.size_per = 0
        self.cursor = 0
        self.filepath = None
        self.frame_num = 0

    def begin(self, filepath, size, size_per):
        self.filepath = filepath
        self.size = size
        self.size_per = size_per
        self.on_begin()

    def end(self, filepath):
        self.on_end()

    def status(self, filepath, cursor):
        self.cursor = cursor
        self.on_status()
        self.frame_num += 1

    def on_begin(self):
        pass

    def on_end(self):
        pass

    def on_status(self):
        pass


class SmbProgressCommon(SmbProgressBase):
    speed_delay = 5

    def __init__(self):
        super().__init__()
        self.ts_last = 0.
        self.cursor_last = 0
        self.speed = 0.

    @property
    def formatted_speed(self):
        mb = self.speed / 2 ** 10 / 2 ** 10
        if mb > 1:
            return '%.1f Mb/s' % mb
        kb = self.speed / 2 ** 10
        return '%.1f Kb/s' % kb

    def on_begin(self):
        super().on_begin()
        self.ts_last = time.time()

    def on_status(self):
        super().on_status()
        self.on_status_frame()
        if self.frame_num % self.speed_delay == 0:
            ts = time.time()
            delta = ts - self.ts_last
            self.speed = (self.cursor - self.cursor_last) / (delta or 1)
            self.cursor_last = self.cursor
            self.ts_last = ts
            self.on_status_speed()

    def on_status_frame(self):
        pass

    def on_status_speed(self):
        pass


class SmbBar(ChargingBar):
    file = stdout
    suffix = '%(percent).1f%% %(speed)s'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = ''

    def force_end(self):
        self.index = self.max
        self.update()

    def is_tty(self):
        return True

    def set_speed(self, speed):
        self.speed = speed


class SmbProgressConsole(SmbProgressCommon):
    bar_cls = SmbBar

    def __init__(self):
        super().__init__()
        self.bar = None

    @staticmethod
    def normalize_str(s):
        return s.replace('%', '_').replace('?', '-')

    def on_begin(self):
        super().on_begin()
        self.bar = self.bar_cls(self.normalize_str(self.filepath), max=(self.size // self.size_per) + 1)
        self.bar.update()

    def on_status_frame(self):
        super().on_status_frame()
        self.bar.next()

    def on_status_speed(self):
        super().on_status_speed()
        self.bar.set_speed(self.formatted_speed)

    def on_end(self):
        super().on_end()
        self.bar.force_end()
