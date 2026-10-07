"""
clean.py — Step 1 of the pipeline: turn text into numbers, one value at a time.

Two element functions that each read one messy string and return one number, and
two DataFrame functions that use `Series.apply` to run them down a whole column
and store the result in a **new** column.

The lineage rule, which every step of this pipeline follows:

    A pipeline function takes a DataFrame and returns a WIDER copy of it.
    It never changes a value it was given, never removes a column, never renames
    one, and never modifies the frame the caller passed in.

So `"38h 30m"` stays in `hours`, and `38.5` goes in `hours_worked` beside it. An
auditor reading the payroll table can see both — which is the point.

This step is walked through line by line in each docstring. The next two steps
give you less.
"""

import pandas as pd


def parse_hours(value) -> float:
    """
    Convert time string (e.g., "2h 30m") or number to float hours.
    Returns 0.0 if input empty, NaN, or invalid.
    """
    if not isinstance(value, str):
        if pd.isna(value):
            return 0.0
        else:
            return float(value)

    text = value.strip()
    if text == "":
        return 0.0

    if "h" not in text and "m" not in text:
        try:
            return float(text)
        except ValueError:
            return 0.0

    hours = 0.0
    for word in text.split():
        try:
            if word.endswith("h"):
                hours += float(word[:-1])
            elif word.endswith("m"):
                hours += float(word[:-1]) / 60
        except ValueError:
            # Skip invalid tokens but keep processing others
            continue
    return hours

def clean_currency(value) -> float:
    """
    Convert currency string (e.g., "$1,020.00") to float.
    Returns 0.0 if input empty, NaN, or invalid.
    """
    if not isinstance(value, str):
        if pd.isna(value):
            return 0.0
        return float(value)
    
    value = value.strip()

    try:
      return float(value.replace("$", "").replace(",", "").strip())
    except ValueError:
      return 0.0

print(clean_currency("$1,020.00"))  
print(clean_currency("1020"))       
print(clean_currency(""))           
print(clean_currency(None))         
print(clean_currency("forty"))      
print(clean_currency("USD 1000")) 

def add_hours_worked(timesheet: pd.DataFrame) -> pd.DataFrame:
  out = timesheet.copy()
  out["hours_worked"] = out["hours"].apply(parse_hours)
  return out


def add_hourly_rate(employees: pd.DataFrame) -> pd.DataFrame:
  out = employees.copy()
  out["hourly_rate_usd"] = out["hourly_rate"].apply(clean_currency)
  return out

if __name__ == "__main__":
    # Try the parser here with the debugger — the tests will not stop at breakpoints.
    for sample in ("38h 30m", "42h", "45m", "24.5", "", "forty"):
        print(repr(sample), "->", parse_hours(sample))
    print(clean_currency("$1,020.00"))
