from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Score:
    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("Балл должен быть целым числом")
        
        if self.value < 0:
            raise ValueError("Балл должен быть неотрицательным")


    def __int__(self):
        return self.value
