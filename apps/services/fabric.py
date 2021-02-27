from apps.builder.services import BuilderService
from apps.generator.services import GeneratorService


class Services:
    builder = BuilderService
    generator = GeneratorService


ServiceClasses = Services()

__all__ = ['ServiceClasses']
