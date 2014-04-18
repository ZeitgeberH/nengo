import numpy as np
import pytest

import nengo
import nengo.spa as spa


def test_spa_basic():

    class SpaTestBasic(spa.SPA):
        def __init__(self):
            spa.SPA.__init__(self)
            self.state = spa.Memory(dimensions=32)

            actions = spa.Actions('dot(state, A) --> state=B',
                                  'dot(state, B) --> state=C',
                                  'dot(state, C) --> state=D',
                                  'dot(state, D) --> state=E',
                                  'dot(state, E) --> state=A',
                                  )

            self.bg = spa.BasalGanglia(actions=actions)
            self.thal = spa.Thalamus(self.bg)

            def state_input(t):
                if t < 0.1:
                    return 'A'
                else:
                    return '0'

            self.input = spa.Input(state=state_input)

    model = nengo.Network()
    with model:
        s = SpaTestBasic(label='spa')
        print s._modules

        pState = nengo.Probe(s.state.state.output, 'output', synapse=0.03)
        pActions = nengo.Probe(s.thal.actions.output, 'output', synapse=0.03)

    sim = nengo.Simulator(model)
    sim.run(1)

    vectors = s.get_module_output('state')[1].vectors.T
    import pylab
    pylab.subplot(2, 1, 1)
    pylab.plot(np.dot(sim.data[pState], vectors))
    pylab.subplot(2, 1, 2)
    pylab.plot(sim.data[pActions])
    pylab.show()


if __name__ == "__main__":
    nengo.log(debug=True)
    pytest.main([__file__, '-v'])
