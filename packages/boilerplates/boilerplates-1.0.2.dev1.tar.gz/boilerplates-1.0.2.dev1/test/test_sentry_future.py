"""Unit tests for Sentry boilerplate."""

import unittest

import boilerplates.sentry


class SentryTests(unittest.TestCase):

    def test_save_and_load(self):
        pass


class Tests(unittest.TestCase):

    def test_classifier(self):
        pass
        # boilerplates.sentry.default_classifier(event, hint)


class SentryRateLimiterTests(unittest.TestCase):

    def test_init(self):
        class SentryRateLimiter(boilerplates.sentry.SentryRateLimiter):
            pass
        limiter = SentryRateLimiter()
        self.assertIsInstance(limiter, boilerplates.sentry.SentryRateLimiter)

    def test_rate_limit(self):
        class SentryRateLimiter(boilerplates.sentry.SentryRateLimiter):
            rate_limits = {
                RuntimeError: boilerplates.sentry.Limit(calls=1, period=60 * 60)
            }
        limiter = SentryRateLimiter()

        limiter.rate_limit_before_sending(event, hint)

    def test_save_and_load(self):
        pass