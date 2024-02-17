import platform
from opentelemetry.sdk.resources import Resource
from kengine.opentelemetry.options import KengineOptions


def create_resource(options: KengineOptions):
    attributes = {
        "service.name": options.service_name,
        "kengine.distro.runtime_version": platform.python_version()
    }
    if options.service_version:
        attributes["service.version"] = options.service_version
    return Resource.create(attributes)