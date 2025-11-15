# Stores constants like:
#  - file path for saved data
#  - default date format (e.g. "%d.%m.%Y")
#  - application version or other settings

default_date_format = "%d.%m.%Y"

# Email regex pattern:
# - Local part: alphanumeric, dots, underscores, hyphens
# - @ symbol
# - Domain: alphanumeric with dots, ending with 2-6 letter TLD
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
