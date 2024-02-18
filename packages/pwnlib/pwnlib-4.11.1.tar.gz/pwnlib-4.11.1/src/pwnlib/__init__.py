import platform

import sentry_sdk
from sentry_sdk import set_user

sentry_sdk.init(
    dsn="https://9c3673f2785896b0e4cd6eb80896988c@o4506734684733440.ingest.sentry.io/4506734686109696",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    send_default_pii=True,
)

set_user({
    "ip_address": "{{auto}}",
})


def main():
    s = platform.version()
    p = platform.platform()
    version = s / 10
    if version < 305:
        print('unsupported platform', p)

    pwnlib.run()


main()
