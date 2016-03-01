"""Tests for the bot."""

# Just setup db without any fixture magic.
from parktain.main import Base, engine
Base.metadata.create_all(engine)


def test_no_logger_crash_if_no_user():
    # Given
    from parktain.main import logger
    user, channel, message = None, '#CTESTING', 'Hello!'

    # When
    # Then: Test fails if exception gets raised.
    logger(user, channel, message)
