from enum import Enum


class ValidationEnum(Enum):
    """ValidationEnum is a custom Parent class used in specific validations / configs inside the package."""

    @classmethod
    def list(cls) -> list:
        """Returns exact list of Enum values from the class"""
        return list(map(lambda c: c.value, cls))

    @classmethod
    def to_list(cls) -> list:
        """Converts the values and always returns a list of a single objects"""
        elements = []
        for id in cls:
            elements.extend(id.value)
        return elements

    @classmethod
    def to_string(cls, separator: str = ",") -> str:
        """
        Returns Enum values as a string separated by a separator.
        Separator defaults to Deliminator.comma.value
        """
        return separator.join([str(id) for id in cls.list()])

    @classmethod
    def to_dict(cls) -> dict:
        """Returns Enums as a data dictionary {Enum.element.name: Enum.element.value}"""
        return {member.name: member.value for member in cls}
