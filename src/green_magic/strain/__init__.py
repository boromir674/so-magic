from .data.commands.invoker import Invoker

invoker = Invoker()

from .data.receiver import Backend

backends = ['df']
b_objs = []

for b in backends:
    b_objs.append(Backend.build(b))


data_master = object()
data_master.