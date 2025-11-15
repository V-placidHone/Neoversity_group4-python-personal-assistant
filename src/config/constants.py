"""
Application-wide constants.

Includes:
  - file name for saved data
  - date formats
  - validation patterns
  - UI/CLI limits (truncation lengths, max days, etc.)
"""

# ---------------- Storage / Files ----------------

# Name of the JSON file that stores all assistant data in the user's home dir
DATA_FILE_NAME = ".personal_assistant_data.json"


# ---------------- Dates & Formats ----------------

default_date_format = "%d.%m.%Y"


# ---------------- Validation patterns ----------------

# Email regex pattern:
# - Local part: alphanumeric, dots, underscores, hyphens
# - @ symbol
# - Domain: alphanumeric with dots, ending with 2-6 letter TLD
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


# ---------------- CLI / UI behaviour ----------------

# Notes truncation lengths (characters)
NOTES_SEARCH_RESULT_TRUNCATE = 80
NOTES_LIST_RESULT_TRUNCATE = 60
NOTES_GLOBAL_SEARCH_TRUNCATE = 100

# Global search note preview length
GLOBAL_SEARCH_NOTE_PREVIEW = 100

# Birthdays: maximum allowed days lookahead
BIRTHDAYS_MAX_DAYS = 365
