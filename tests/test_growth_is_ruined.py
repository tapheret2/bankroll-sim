from bankroll_sim.sim import growth_factor, is_ruined

def test_growth_factor():
    assert abs(growth_factor(200, 100) - 2.0) < 1e-12

def test_is_ruined():
    assert is_ruined(0)
    assert not is_ruined(10)
