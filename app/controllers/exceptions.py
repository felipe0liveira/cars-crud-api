class InvalidCarYearException(Exception):
    def __init__(self, year: int):
        self.year = year
        super().__init__(f"Car year cannot be {year}")


class ExistingCarException(Exception):
    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year
        super().__init__(f"Car {make} {model} ({year}) already exists")
