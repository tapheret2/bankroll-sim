from bankroll_sim.sim import max_drawdown_from_path

def test_max_drawdown_from_path():
    assert abs(max_drawdown_from_path([100, 120, 90, 110]) - 0.25) < 1e-12
