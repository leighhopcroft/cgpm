import pytest
import numpy as np

from cgpm.mixtures.view import View
from cgpm.crosscat.state import State
from cgpm.utils import general as gu
from cgpm.utils import bayessets_utils as bu

"""
This tests should be run from the main folder cgpm/
"""

OUT = 'tests/resources/out/'
ANIMALSPATH = 'tests/resources/animals.csv'
@pytest.fixture
def priorView():
    data = np.random.choice([0, 1], size=(100, 5))
    outputs = range(5)
    X = {c: data[:, i].tolist() for i, c in enumerate(outputs)}
    model = View(
        X,
        cctypes=['bernoulli']*5,
        outputs=[1000] + outputs,
        rng=gu.gen_rng(0))
    return model

@pytest.fixture
def priorState():
    data = np.random.choice([0, 1], size=(100, 5))
    outputs = range(5)
    rng=gu.gen_rng(0)
    state = State(data, cctypes=['bernoulli']*5, rng=rng)
    return state

def test_comparison_experiment(priorView, priorState):
    view = priorView
    state = priorState
    evidence = ['grizzly bear', 'killer whale', 'lion']
    comparison_df = bu.comparison_experiment(evidence, ANIMALSPATH, view, state)

    print comparison_df
    fig, ax = bu.score_histograms(comparison_df, evidence)
    fig.savefig(OUT + "scored_histograms")
