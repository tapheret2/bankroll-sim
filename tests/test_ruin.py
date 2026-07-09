from bankroll_sim.sim import ruin_probability

def test_ruin_probability_bounded():
    r = ruin_probability(0.55, 1.0, 100, 50, mode="prop", trials=30, seed=1, frac=0.05)
    assert 0.0 <= r <= 1.0
