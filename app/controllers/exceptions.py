class InvalidCarYearException(Exception):
    def __init__(self, year: int):
        self.year = year
        super().__init__(f"Car year cannot be {year}")
