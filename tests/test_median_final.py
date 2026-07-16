from bankroll_sim.sim import median_final_bankroll

def test_median_final_positive():
    m = median_final_bankroll(0.55, 1.0, 100, 30, mode="prop", trials=21, seed=7, frac=0.05)
    assert m > 0
