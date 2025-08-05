
from dataclasses import dataclass

@dataclass
class SheetStructItem:
    variableName: str
    function: str
    value: any
    conversionFunction: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            variableName=data.get('variableName'),
            function=data.get('function'),
            value=data.get('value'),
            conversionFunction=data.get('conversionFunction')
        )