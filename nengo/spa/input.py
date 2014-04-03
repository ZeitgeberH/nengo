import nengo
from .. import objects
from .module import Module

class Input(Module):
    def __init__(self, target, value):
        Module.__init__(self)
        self.target = target
        self.value = value

    def on_add(self, spa):
        Module.on_add(self, spa)
        target, vocab = spa.get_module_input(self.target.label)
        if callable(self.value):
            val = lambda t: vocab.parse(self.value(t)).v
            self.input = nengo.Node(val, label='input')
        else:
            val = vocab.parse(self.value).v
            self.input = nengo.Node(val, label='input')

        nengo.Connection(self.input, target, filter=None)
