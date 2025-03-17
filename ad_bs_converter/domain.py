from pydantic import BaseModel
from ad_bs_converter import constants


class BSDate(BaseModel):
    """
    Represents a date in the Bikram Sambat (BS) calendar.

    Attributes:
        year: The BS year
        month: The BS month (1-12)
        day: The BS day
    """

    year: int
    month: int
    day: int

    @property
    def fiscal_year(self) -> str:
        """
        Returns the fiscal year representation for this BS date.
        In Nepal, the fiscal year starts from month 4 (Shrawan).

        Returns:
            str: Fiscal year in the format "YYYY-YY"
        """
        if self.month >= constants.FISCAL_YEAR_START_MONTH:
            return f"{self.year}-{str(self.year + 1)[-2:]}"
        return f"{self.year - 1}-{str(self.year)[-2:]}"

    def __str__(self) -> str:
        """
        Returns the string representation of the date in YYYY-MM-DD format.

        Returns:
            str: Date string in ISO format
        """
        return f"{self.year}-{self.month:02d}-{self.day:02d}"
