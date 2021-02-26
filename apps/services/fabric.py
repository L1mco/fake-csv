from apps.builder.services import BuilderService


class Services:
    builder = BuilderService


ServiceClasses = Services()

__all__ = ['ServiceClasses']
