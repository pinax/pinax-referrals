try:  # Python 3.8+
    from importlib.metadata import version
except ImportError:  # Python < 3.8
    from pkg_resources import get_distribution

    def version(distribution_name):
        return get_distribution(distribution_name).version


default_app_config = "pinax.referrals.apps.AppConfig"
__version__ = version("pinax-referrals")
