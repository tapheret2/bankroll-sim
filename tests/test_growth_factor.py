from bankroll_sim.sim import growth_factor

def test_growth_factor():
    assert abs(growth_factor(150, 100) - 1.5) < 1e-9
    assert growth_factor(10, 0) == 0.0
