from datetime import date
from src.ad_bs_converter import ADToBSConverter

# Create a converter with an AD date
ad_date = date(2000, 3, 21)
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