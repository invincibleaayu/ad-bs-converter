from datetime import date
from functools import lru_cache


from ad_bs_converter.exceptions import ADDateOutOfBoundsError
from ad_bs_converter.constants import (
    REFERENCE_AD_DATE,
    MIN_AD_YEAR,
    MAX_AD_YEAR,
    START_BS_YEAR,
    MONTH_NAMES,
    NEPALI_YEARS,
)
from ad_bs_converter.domain import BSDate


class ADToBSConverter:
    """
    Converts Gregorian (AD) dates to Bikram Sambat (BS) dates.

    The converter uses a pre-defined lookup table for Nepali calendar data
    from 1970 BS (1913 AD) to 2082 BS (2026 AD). It implements LRU caching
    to improve performance for repeated conversions.
    """

    def __init__(self, ad_date: date, cache_size: int = 128) -> None:
        """
        Initialize the converter with an AD date.

        Args:
            ad_date: A datetime.date object representing a Gregorian (AD) date
            cache_size: Size of the LRU cache for storing conversion results (default: 128)

        Raises:
            ADDateOutOfBoundsError: If the provided date is outside the supported range
        """
        self._ad_date = ad_date
        self._cache_size = cache_size

        # Configure the cache size for the convert method
        self._configure_cache(cache_size)

        self._validate_data()
        self._validate_ad_date()
        self._bs_date = self._convert(self._ad_date)

    def _configure_cache(self, cache_size: int) -> None:
        """
        Configure the LRU cache size for the convert method.

        Args:
            cache_size: The maximum size of the LRU cache
        """
        # We need to reconfigure the cache if the size changes
        if hasattr(self._convert, "cache_clear"):
            self._convert.cache_clear()

        # Create a new decorated function with the specified cache size
        self._convert = lru_cache(maxsize=cache_size)(self._raw_convert)

    @lru_cache(maxsize=128)  # Default cache size
    def _raw_convert(self, ad_date: date) -> BSDate:
        """
        Convert the AD date to BS date.

        Args:
            ad_date: A datetime.date object representing a Gregorian (AD) date

        Returns:
            BSDate: The equivalent Bikram Sambat date

        Raises:
            ADDateOutOfBoundsError: If the calculation results in a BS year with no data
        """
        delta_days = (ad_date - REFERENCE_AD_DATE).days

        bs_year = START_BS_YEAR
        bs_month = 1
        bs_day = 1

        while bs_year in NEPALI_YEARS and delta_days >= NEPALI_YEARS[bs_year][0]:
            delta_days -= NEPALI_YEARS[bs_year][0]
            bs_year += 1

        if bs_year not in NEPALI_YEARS:
            raise ADDateOutOfBoundsError(f"No data available for BS year {bs_year}")

        for month in range(1, 13):
            month_days = NEPALI_YEARS[bs_year][month]
            if delta_days < month_days:
                bs_month = month
                bs_day = delta_days + 1
                break
            delta_days -= month_days

        return BSDate(year=bs_year, month=bs_month, day=bs_day)

    def _validate_data(self) -> None:
        """
        Validates the data for each Nepali year.

        Checks for consistency in the number of days in each year and ensures that the sum of days
        in the months matches the total number of days in the year.

        Raises:
            ValueError: If there is an inconsistency or invalid data in the year data.
        """
        for year, days in NEPALI_YEARS.items():
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

    def _validate_ad_date(self) -> None:
        """
        Validate that the AD date is within the supported range.

        Raises:
            ADDateOutOfBoundsError: If the date is outside the supported range
        """
        if not self._is_date_in_range():
            raise ADDateOutOfBoundsError(
                f"Date must be between {MIN_AD_YEAR} and {MAX_AD_YEAR}"
            )

        if (self._ad_date - REFERENCE_AD_DATE).days < 0:
            raise ADDateOutOfBoundsError("Date is before the earliest supported date")

    def _is_date_in_range(self) -> bool:
        """
        Checks whether the AD date is within the allowed range.

        Returns:
            bool: True if the date is within the valid range, False otherwise.
        """
        return MIN_AD_YEAR <= self._ad_date.year <= MAX_AD_YEAR

    def get_bs_date(self) -> BSDate:
        """
        Get the converted BS date.

        Returns:
            BSDate: The equivalent Bikram Sambat date
        """
        return self._bs_date

    def get_formatted(self) -> str:
        """
        Get the formatted string representation of the BS date.

        Returns:
            str: BS date in YYYY-MM-DD format
        """
        return str(self._bs_date)

    def get_month_name(self) -> str:
        """
        Get the Nepali name of the month for the BS date.

        Returns:
            str: Nepali month name

        Raises:
            ValueError: If the month is invalid
        """
        if 1 <= self._bs_date.month <= 12:
            return MONTH_NAMES[self._bs_date.month - 1]
        raise ValueError("Invalid Month")

    @classmethod
    def clear_cache(cls) -> None:
        """
        Clear the conversion cache.

        This method can be used to free up memory if many conversions have been performed.
        """
        for instance in cls.__dict__.values():
            if hasattr(instance, "cache_clear"):
                instance.cache_clear()

    @staticmethod
    def get_cache_info():
        """
        Get information about the current state of the cache.

        Returns:
            CacheInfo: A named tuple with cache statistics
        """
        if hasattr(ADToBSConverter._raw_convert, "cache_info"):
            return ADToBSConverter._raw_convert.cache_info()
        return None
