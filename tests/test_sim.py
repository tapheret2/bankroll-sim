from bankroll_sim import compare_modes, simulate


def test_reproducible():
    a = simulate(0.55, 1.0, 1000, 50, mode="prop", seed=3)
    b = simulate(0.55, 1.0, 1000, 50, mode="prop", seed=3)
    assert a.path == b.path


def test_compare_three():
    rows = compare_modes(0.55, 1.0, 1000, 30, seed=1)
    assert len(rows) == 3
    assert {r.mode for r in rows} == {"flat", "prop", "kelly"}
