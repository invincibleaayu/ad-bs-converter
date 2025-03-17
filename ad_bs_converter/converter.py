from datetime import date
from ad_bs_converter import constants
from ad_bs_converter.domain import BSDate
from ad_bs_converter.exception import ADDateOutOfBoundsError


class ADToBSConverter:
    """
    A class to convert an AD (Gregorian) date to a BS (Nepali) date.

    Attributes:
        ad_date (date): The AD date to be converted.
        cache_size (int): The size of the cache for storing previously calculated conversions.
        bs_date (BSDate): The converted BS date.

    Methods:
        get_bs_date(): Returns the converted BS date.
        get_formatted(): Returns the converted BS date as a string.
        get_month_name(): Returns the name of the month in the BS calendar.
    """

    def __init__(self, ad_date: date, cache_size: int = 128) -> None:
        """
        Initializes the AD to BS converter.

        Args:
            ad_date (date): The AD date to be converted.
            cache_size (int, optional): The cache size for storing previously calculated conversions. Defaults to 128.

        Raises:
            ValueError: If the year data in the constants is inconsistent or invalid.
            ADDateOutOfBoundsError: If the provided AD date is out of the allowed range.
        """
        self._ad_date = ad_date
        self._cache_size = cache_size
        self._validate_data()
        self._validate_ad_date()
        self._bs_date = self._convert()

    def _validate_data(self) -> None:
        """
        Validates the data for each Nepali year.

        Checks for consistency in the number of days in each year and ensures that the sum of days
        in the months matches the total number of days in the year.

        Raises:
            ValueError: If there is an inconsistency or invalid data in the year data.
        """
        for year, days in constants.NEPALI_YEARS.items():
            if len(days) != 13:
                raise ValueError(
                    f"Invalid data for year {year}: expected 13 elements, got {len(days)}"
                )

            if days[0] not in (365, 366):
                raise ValueError(f"Invalid total days for year {year}: {days[0]}")

            month_sum = sum(days[1:])
            if month_sum != days[0]:
                raise ValueError(
                    f"Data inconsistency for year {year}: sum of months {month_sum} != total {days[0]}"
                )

    def _convert(self) -> BSDate:
        """
        Converts the given AD date to a BS date.

        The method calculates the number of days since the reference AD date, and then uses the
        Nepali calendar data to determine the corresponding BS year, month, and day.

        Returns:
            BSDate: The corresponding BS date.

        Raises:
            ADDateOutOfBoundsError: If the provided AD date cannot be converted to a BS date due to out-of-bounds error.
        """
        delta_days = (self._ad_date - constants.REFERENCE_AD_DATE).days

        bs_year = constants.START_BS_YEAR
        bs_month = 1
        bs_day = 1

        while (
            bs_year in constants.NEPALI_YEARS
            and delta_days >= constants.NEPALI_YEARS[bs_year][0]
        ):
            delta_days -= constants.NEPALI_YEARS[bs_year][0]
            bs_year += 1

        if bs_year not in constants.NEPALI_YEARS:
            raise ADDateOutOfBoundsError(
                message=f"No data available for BS year {bs_year}",
            )

        for month in range(1, 13):
            month_days = constants.NEPALI_YEARS[bs_year][month]
            if delta_days < month_days:
                bs_month = month
                bs_day = delta_days + 1
                break
            delta_days -= month_days

        return BSDate(year=bs_year, month=bs_month, day=bs_day)

    def _validate_ad_date(self) -> None:
        """
        Validates that the AD date is within the valid range and not before the earliest supported date.

        Raises:
            ADDateOutOfBoundsError: If the AD date is outside the supported range.
        """
        if not self._is_date_in_range():
            raise ADDateOutOfBoundsError(
                message=f"Date must be between {constants.MIN_AD_YEAR} and {constants.MAX_AD_YEAR}",
            )

        if (self._ad_date - constants.REFERENCE_AD_DATE).days < 0:
            raise ADDateOutOfBoundsError(
                message="Date is before the earliest supported date",
            )

    def get_bs_date(self) -> BSDate:
        """
        Returns the converted BS date.

        Returns:
            BSDate: The converted BS date.
        """
        return self._bs_date

    def get_formatted(self) -> str:
        """
        Returns the converted BS date as a formatted string.

        Returns:
            str: The BS date formatted as a string.
        """
        return str(self._bs_date)

    def get_month_name(self) -> str:
        """
        Returns the name of the month in the BS calendar.

        Args:
            None

        Returns:
            str: The name of the month in the BS calendar.

        Raises:
            ValueError: If the month number is not valid.
        """
        if 1 <= self._bs_date.month <= 12:
            return constants.MONTH_NAMES[self._bs_date.month - 1]
        raise ValueError("Invalid Month")

    def _is_date_in_range(self) -> bool:
        """
        Checks whether the AD date is within the allowed range.

        Returns:
            bool: True if the date is within the valid range, False otherwise.
        """
        return constants.MIN_AD_YEAR <= self._ad_date.year <= constants.MAX_AD_YEAR
