import math

from nanobot import TissueMap, shortest_path


def solve(text):
    return shortest_path(TissueMap.from_ascii(text))


def test_straight_line():
    path, length = solve("S....T")
    assert length == 5
    assert len(path) == 6


def test_diagonal_is_shorter_than_staircase():
    _, length = solve("""
        S..
        ...
        ..T
    """)
    assert math.isclose(length, 2 * math.sqrt(2))


def test_detours_around_wall_and_avoids_blocked_cells():
    tissue = TissueMap.from_ascii("""
        S#T
        .#.
        ...
    """)
    path, length = shortest_path(tissue)
    assert length == 6
    assert not set(path) & tissue.blocked


def test_cannot_cut_corners():
    assert solve("""
        S#
        #T
    """) is None


def test_unreachable_target():
    assert solve("S#T") is None
