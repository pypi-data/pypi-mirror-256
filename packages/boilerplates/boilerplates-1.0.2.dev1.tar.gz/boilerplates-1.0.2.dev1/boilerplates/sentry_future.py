
import logging
import pathlib
import pickle
import typing as t

import ratelimit
import sentry_sdk

if t.TYPE_CHECKING:
    from sentry_sdk import _types as sentry_types

from .sentry import Sentry

_LOG = logging.getLogger(__name__)

Limit = t.NamedTuple('Limit', [('calls', int), ('period', int)])


# LimitState = t.NamedTuple('LimitState', [
#     ('limit', Limit), ('decorator', ), ('state', 'sentry_types.EventProcessor')])


def do_nothing(_, __) -> None:
    return None


def default_classifier(event: 'sentry_types.Event', hint: t.Dict[str, t.Any]) -> t.Any:
    """An event classifier based on the exception type."""
    _LOG.debug('detected an event %s, hinting %s', event, hint)
    try:  # pylint: disable = too-many-try-statements
        exc_type, _, _ = hint['exc_info']
        return exc_type
    except KeyError:
        pass
    if event['exception'] is not None and event['exception']['values']:
        for exc in event['exception']['values']:
            if exc['type'] is not None:
                return exc['type']
    return None


class SentryRateLimiter:
    """Sentry rate limiter."""


    thresholds: t.Dict[t.Type, Limit] = {}
    """Event thresholds.

    Example:
    {
        ExceptionType: Limit(calls=10, period=60 * 60),
        OtherType: lambda _, __: None
    }
    """

    default_threshold: t.Optional[Limit] = None
    """Default event threshold, which is no threshold."""

    rate_limits: t.Dict[t.Type, Limit] = {}
    """Event rate limits.

    Example:
    {
        ExceptionType: ratelimit.limits(calls=5, period=15 * 60)(lambda _, __: None),
        OtherType: lambda _, __: None
    }
    """

    default_rate_limit: t.Optional[Limit] = Limit(calls=1, period=1 * 60 * 60)
    """Default event rate limit, which is 1 event per hour."""

    def __init__(self) -> None:
        cls = type(self)
        self._thresholds: t.Dict[t.Type, Limit] = cls.thresholds
        # self._thresholds_state: t.Dict[t.Type, 'sentry_types.EventProcessor'] = {}
        self._rate_limits: t.Dict[t.Type, Limit] = cls.rate_limits
        # self._rate_limits_state: t.Dict[t.Type, 'sentry_types.EventProcessor'] = {}

    def rate_limit_before_sending(
            self, event: 'sentry_types.Event', hint: t.Dict[str, t.Any]
            ) -> t.Optional['sentry_types.Event']:
        """Prevent exceeding Sentry limits by ignoring events if there are too many of them.

        This function relies on the following class members to determine if an event
        should be really sent to Sentry or not:
        * thresholds stores Exception-type specific event thresholds
        * get_default_threshold returns a default event threshold
        * rate_limits stores Exception-type specific event rate limits
        * get_default_rate_limit returns a default event rate limit

        Every event first goes through a threshold filter.
        If a threshold is None, it means no threshold (i.e. always forward to the rate limiter).
        Then, the event goes to a rate limiter.
        If rate limiter is None, event is always sent to Sentry.
        """
        _LOG.debug('detected an event %s, hinting %s', event, hint)
        type_ = default_classifier(event, hint)
        if type_ is None:
            return event

        if type_ not in self._thresholds:
            if self.default_threshold is not None:
                self._thresholds[type_] = self.default_threshold
                self._thresholds_state[type_] = ratelimit.limits(
                    calls=self._thresholds[type_].calls, period=self._thresholds[type_].period)
                return self._thresholds_state[type_](do_nothing)
        else:
            try:
                return self._thresholds_state[type_](event, hint)
            except ratelimit.RateLimitException:
                _LOG.debug('an event %s passed the event threshold', event)

        # if exc_type not in event_rate_limits:
        #     event_rate_limits[exc_type] = get_default_event_rate_limit()

        # if event_rate_limits[exc_type] is None:
        #     return event
        # try:
        #     return event_rate_limits[exc_type](event, hint)
        # except ratelimit.RateLimitException:
        #     _LOG.debug('an event %s passed the event rate limit', event)
        return event


class SentryFuture(Sentry):
    """Sentry configuration."""

    state_file_path: pathlib.Path

    transaction_thresholds: t.Dict[Exception, 'sentry_types.EventProcessor'] = {}
    """Transaction thresholds."""

    @staticmethod
    def get_default_transaction_threshold() -> 'sentry_types.EventProcessor':
        """Return a default event threshold, which is no threshold."""
        return do_nothing

    transaction_rate_limits: t.Dict[Exception, 'sentry_types.EventProcessor'] = {}
    """Transaction rate limits."""

    @staticmethod
    def get_default_transaction_rate_limit() -> 'sentry_types.EventProcessor':
        """Return a default event rate limit, which is 1 event per 12 hours."""
        return ratelimit.limits(calls=1, period=12 * 60 * 60)(do_nothing)

    # state = {}

    # @classmethod
    # def _rate_limit_errors_before_sending(
    #         cls, error: 'sentry_types.Event',
    #         hint: t.Dict[str, t.Any]) -> t.Optional['sentry_types.Event']:
    #     """Prevent exceeding Sentry error limits by ignoring errors if there are too many of them.

    #     This function relies on the following class members to determine if an error
    #     should be really sent to Sentry or not:
    #     * error_thresholds stores Exception-type specific error thresholds
    #     * get_default_error_threshold returns a default error threshold
    #     * error_rate_limits stores Exception-type specific error rate limits
    #     * get_default_error_rate_limit returns a default rate limit

    #     Every error first goes through a threshold filter.
    #     If a threshold is None, it means no threshold (i.e. always forward to the rate limiter).
    #     Then, error goes to a rate limiter.
    #     If rate limiter is None, error is always sent to Sentry.
    #     """
    #     return cls._rate_limit_before_sending(
    #         error, hint, cls.error_thresholds, cls.get_default_error_threshold,
    #         cls.error_rate_limits, cls.get_default_error_rate_limit)

    # @classmethod
    # def _rate_limit_transactions_before_sending(
    #         cls, transaction: 'sentry_types.Event',
    #         hint: t.Dict[str, t.Any]) -> t.Optional['sentry_types.Event']:
    #     """Prevent exceeding Sentry transaction limits by ignoring them if there are too many.

    #     This function relies on the following class members to determine if a transaction
    #     should be really sent to Sentry or not:
    #     * transaction_thresholds stores Exception-type specific transaction thresholds
    #     * get_default_transaction_threshold returns a default transaction threshold
    #     * transaction_rate_limits stores Exception-type specific transaction rate limits
    #     * get_default_transaction_rate_limit returns a default rate limit

    #     Every transaction first goes through a threshold filter.
    #     If a threshold is None, it means no threshold (i.e. always forward to the rate limiter).
    #     Then, transaction goes to a rate limiter.
    #     If rate limiter is None, transaction is always sent to Sentry.
    #     """
    #     return cls._rate_limit_before_sending(
    #         transaction, hint, cls.transaction_thresholds, cls.get_default_transaction_threshold,
    #         cls.transaction_rate_limits, cls.get_default_transaction_rate_limit)

    @classmethod
    def load_state(cls):
        with cls.state_file_path.open('rb') as pickle_file:
            data = pickle.load(pickle_file, encoding='utf-8')
        _LOG.info('%s', data)
        # _LOG.info('%s', cls.error_thresholds)
        # _LOG.info('%s', cls.error_rate_limits)
        _LOG.info('%s', cls.transaction_thresholds)
        _LOG.info('%s', cls.transaction_rate_limits)

    @classmethod
    def save_state(cls):
        """Persist Sentry configuration."""
        # data = {
        #     'error_thresholds': {key: value for key, value in cls.error_thresholds.items()},
        #     'error_rate_limits': cls.error_rate_limits,
        #     'transaction_thresholds': cls.transaction_thresholds,
        #     'transaction_rate_limits': cls.transaction_rate_limits
        # }
        # with cls.state_file_path.open('wb') as pickle_file:
        #     pickle.dump(data, pickle_file)

    @classmethod
    def init(cls, *args, **kwargs):
        # cls.load_state()
        sentry_sdk.init(
            *args,
            # before_send=cls._rate_limit_errors_before_sending,
            # before_send_transaction=cls._rate_limit_transactions_before_sending,
            **kwargs)
