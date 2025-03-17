# AD-BS Converter

A Python library for converting Gregorian calendar (AD) dates to Bikram Sambat (BS) dates used in Nepal.

## Overview

This library provides functionality to convert dates from the Gregorian calendar (AD) to the Bikram Sambat (BS) calendar system, which is the official calendar of Nepal. The implementation uses a pre-defined lookup table for Nepali calendar data from 1970 BS (1913 AD) to 2082 BS (2026 AD) for accurate conversions.

## Features

- Convert AD dates to BS dates
- Get formatted BS date in YYYY-MM-DD format
- Get Nepali month names
- Built-in validation for date ranges
- LRU caching for improved performance

## Installation

```bash
pip install ad_bs_converter
```

## Usage

### Basic Conversion

```python
from datetime import date
from ad_bs_converter import ADToBSConverter

# Create a converter with an AD date
ad_date = date(2023, 5, 15)
converter = ADToBSConverter(ad_date)

# Get the BS date
bs_date = converter.get_bs_date()
print(bs_date)  # Output: 2080-2-1

# Get formatted date
formatted_date = converter.get_formatted()
print(formatted_date)  # Output: 2080-2-1

# Get Nepali month name
month_name = converter.get_month_name()
print(month_name)  # Output: Jestha
```

### Cache Management

The library uses LRU caching to improve performance for repeated conversions.

```python
# Configure cache size when creating a converter
converter = ADToBSConverter(date(2023, 5, 15), cache_size=256)

# Get cache information
cache_info = ADToBSConverter.get_cache_info()
print(cache_info)

# Clear the cache if needed
ADToBSConverter.clear_cache()
```

## Error Handling

The library provides specific error handling for date range validation:

```python
from datetime import date
from ad_bs_converter import ADToBSConverter
from ad_bs_converter.exceptions import ADDateOutOfBoundsError

try:
    # Try with a date outside the supported range
    converter = ADToBSConverter(date(1900, 1, 1))
except ADDateOutOfBoundsError as e:
    print(f"Error: {e}")
```

## Supported Date Range

The converter supports AD dates from approximately 1913 to 2026, corresponding to BS dates from 1970 to 2082.

## Documentation

For more detailed documentation including:
- API reference
- Implementation details
- Calendar data sources

Please refer to the github link [Aayush Dip Giri](https://github.com/invincibleaayu/ad-bs-converter).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

