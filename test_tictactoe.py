import pytest
from tictactoe import Game

_test_did_win = (
        ([0, 0, 0,
          0, 0, 0,
          0, 0, 0], False),

        ([1, 1, 1,
          0, 0, 0,
          0, 0, 0], True),
        ([0, 0, 0,
          1, 1, 1,
          0, 0, 0], True),
        ([0, 0, 0,
          0, 0, 0,
          1, 1, 1], True),
        ([1, 0, 0,
          1, 0, 0,
          1, 0, 0], True),
        ([0, 1, 0,
          0, 1, 0,
          0, 1, 0], True),
        ([0, 0, 1,
          0, 0, 1,
          0, 0, 1], True),
        ([1, 0, 0,
          0, 1, 0,
          0, 0, 1], True),
        ([0, 0, 1,
          0, 1, 0,
          1, 0, 0], True),

        ([1, 0, 1,
          0, 1, 0,
          1, 0, 0], True),
)

@pytest.mark.parametrize('player,expect', _test_did_win)
def test_did_win(player, expect):
    assert expect == Game()._did_win(player)
