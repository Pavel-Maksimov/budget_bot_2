import pytest

from budget_bot_2.utilities import create_keyboard

params = [
    (2, [0, 1, 2, 3, 4], [[0, 1], [2, 3], [4]]),
    (2, [0, 1, 2, 3], [[0, 1], [2, 3]]),
    (4, [0, 1, 2], [[0, 1, 2]]),
    (1, [1], [[1]]),
    (1, [1, 2, 3], [[1], [2], [3]]),
    (2, [], []),
]


@pytest.mark.parametrize("columns,buttons,expected", params)
def test_create_keyboard(columns, buttons, expected):
    assert create_keyboard(columns, buttons) == expected
