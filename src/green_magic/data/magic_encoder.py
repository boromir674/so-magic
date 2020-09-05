import attr
from green_magic.utils import Subject


@attr.s
class MagicEncoder:
    encoders = attr.ib(init=True, default={})
    subject = attr.ib(init=True, default=Subject([]))

    def encode(self, *args, **kwargs):
        encoder = self.encoders[args[0]]

        self.subject.state = encoder.encode(*args[1:], **kwargs)
        self.subject.columns = encoder.columns
        self.subject.notify()
