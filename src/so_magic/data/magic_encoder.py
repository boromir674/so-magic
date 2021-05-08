# import attr
# from so_magic.utils import Subject


# @attr.s
# class MagicEncoder:
#     """Encode information and notify subscribers/listeners (aka observers).

#     Instances of this class can encode data, using a pre-build encoding 
#     algorithm and notifies subscribers/listeners about the result.

#     Args:
#         encoders (dict): str 2 "object with encode method" mapping
#         subject (Subject): an instance that can notify each observers/listeners
#     """
#     encoders = attr.ib(init=True, default={})
#     subject = attr.ib(init=True, default=Subject([]))

#     def encode(self, *args, **kwargs):
#         """Encode information and notify subscribers/listeners (aka observers).
        
#         Encode the input data, using the selected encoding algorithm and 
#         notify subscribers/listeners about the result.

#         Args:
#             encoder_name (str): the desired encoding algorithm to use
#         """
#         encoder = self.encoders[args[0]]

#         self.subject.state = encoder.encode(*args[1:], **kwargs)
#         self.subject.columns = encoder.columns
#         self.subject.notify()
