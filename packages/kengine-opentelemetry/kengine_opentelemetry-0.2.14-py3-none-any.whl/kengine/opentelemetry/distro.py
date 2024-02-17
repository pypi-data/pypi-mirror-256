"""This honey-flavored Distro configures OpenTelemetry for use with Kengine.

Typical usage example:

    using the opentelemetry-instrument command with
    requisite env variables set:

    $bash> opentelemetry-instrument python program.py

    or configured by code within your service:
    configure_opentelemetry(
        KengineOptions(
            debug=True,
            apikey=os.getenv("KENGINE_API_KEY"),
            service_name="otel-python-example"
        )
    )
"""
from logging import getLogger
from kengine.opentelemetry.options import KengineOptions
from kengine.opentelemetry.trace import create_tracer_provider
from kengine.opentelemetry.resource import create_resource
from opentelemetry.instrumentation.distro import BaseDistro

from opentelemetry.trace import set_tracer_provider

from typing import Optional
_logger = getLogger(__name__)

def configure_opentelemetry(
    options: Optional[KengineOptions] = None,
):
    """Configure OpenTelemetry for use with Kengine.

    Args:
        kengine_options (Kengine): The options to configure
            OpenTelemetry with.
    """
    if options is None:
        options = KengineOptions()
    _logger.setLevel(level=options.log_level)
    _logger.info("Configuring OpenTelemetry using the Kengine distro")
    _logger.debug(vars(options))
    resource = create_resource(options)
    set_tracer_provider(
        create_tracer_provider(options, resource)
    )

    # pylint: disable=too-few-public-methods
class KengineDistro(BaseDistro):
    """
    An extension of the base python OpenTelemetry distro, which provides
    a mechanism to automatically configure some of the more common options
    for users. This class is auto-detected by the `opentelemetry-instrument`
    command.

    This class doesn't need to be touched directly when using the distro. If
    you'd like to explicitly set configuration in code, use the
    configure_opentelemetry() function above instead of the
    `opentelemetry-instrument` command.

    If you're wondering about the under-the-hood magic - we add the following
    declaration to package metadata in our pyproject.toml, like so:

    [tool.poetry.plugins."opentelemetry_distro"]
    distro = "kengine.opentelemetry.distro:KengineDistro"
    """

    def _configure(self, **kwargs):
        configure_opentelemetry()