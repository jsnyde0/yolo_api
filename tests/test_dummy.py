import pytest


@pytest.mark.asyncio
async def test_dummy():
    """A simple test to verify pytest and pytest-asyncio are working."""
    expected = True
    actual = True
    assert actual == expected, "Basic assertion should pass"
