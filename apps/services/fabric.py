from apps.generator.services import GeneratorService


class Services:
    generator = GeneratorService


ServiceClasses = Services()

__all__ = ['ServiceClasses']
