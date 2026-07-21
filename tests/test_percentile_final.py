from bankroll_sim.sim import percentile_final_bankroll

def test_percentile_ordering():
    lo = percentile_final_bankroll(0.55, 1.0, 100, 40, q=0.1, trials=41, seed=3, frac=0.05)
    hi = percentile_final_bankroll(0.55, 1.0, 100, 40, q=0.9, trials=41, seed=3, frac=0.05)
    assert lo <= hi
