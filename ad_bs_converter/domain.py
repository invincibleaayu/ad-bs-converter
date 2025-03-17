from pydantic import BaseModel
from ad_bs_converter import constants


class BSDate(BaseModel):
    year: int
    month: int
    day: int

    @property
    def fiscal_year(self) -> str:
        if self.month >= constants.FISCAL_YEAR_START_MONTH:
            return f"{self.year}-{str(self.year + 1)[-2:]}"
        return f"{self.year - 1}-{str(self.year)[-2:]}"

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02d}-{self.day:02d}"
