"""Tests for the bot."""

def test_no_logger_crash_if_no_user():
    # Given
    from parktain.main import logger
    user, channel, message = None, '#CTESTING', 'Hello!'

    # When
    # Then: Test fails if exception gets raised.
    logger(user, channel, message)
