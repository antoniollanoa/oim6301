import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📕 Mini Project 2: Economic Performance Analyzer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    This tool helps business analysts and decision-makers compare the economic performance of Argentina, Brazil, Colombia, and Mexico using GDP growth, inflation, and unemployment rates from 2000 to 2024. It helps identify which countries have demonstrated stronger economic performance and stability over time, supporting informed decisions about potential business expansion and investment opportunities.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    `How I Would Solve It`

    1. Define the four countries, the three economic indicators, and the period from 2000 to 2024.
    2. Create a Python function that requests data from the World Bank API using requests.
    3. Retrieve all available records for each indicator and country, including additional pages if necessary.
    4. Organize the results into a list of dictionaries containing the country, year, indicator, and value.
    5. Save the fetched records as a JSON file in projects/mp2/data/.
    6. Exclude missing values from calculations while keeping track of how many observations are available.
    7. Calculate the average GDP growth, inflation, and unemployment for each country.
    8. Compare the results and identify which countries performed better on each indicator.
    9. Print a formatted table and a short conclusion explaining the findings.
    10. Verify at least one result using an independent calculation.



    `Which functions will your tool need? For each, what goes in and what comes out?`

    The tool will need four main functions:
    The first function, `fetch_world_bank_data()`, will take the countries, economic indicator, and date range as inputs and return a list of records from the World Bank API.
    The second function, `calculate_averages()`, will take the retrieved records and calculate the average GDP growth, inflation, and unemployment for each country.
    The third function, `save_data()`, will take the records and a file path to save the information as a JSON file. Finally, `find_best_performers()` will use the calculated averages to identify which country performed best for each economic indicator.


    `Which addresses will they request?`

    The fetching function will request three World Bank API endpoints, one for each indicator, using this general structure:
    https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}?format=json&date={start}:{end}&per_page=500&page=1
    Only the fetching function needs to make API requests. The remaining functions process the returned data locally.

    `How will you know you have every record?`

    The World Bank API provides pages and total fields in its response metadata.
    The tool will request every page and compare the number of retrieved records with the API's reported total for each indicator.
    Missing economic values will still count as retrieved records, even though they won't be used to calculate averages.

    `Which check will you use in section 6, and which two numbers should agree?`

    Check 1 — API completeness: Compare the number of records retrieved with the total reported by the World Bank API.
    Check 2 — Calculation accuracy: Independently calculate Argentina's average GDP growth from its available annual values and compare it with the average displayed in the final results table.
    Both checks can run directly in Python and print the two numbers being compared.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs
    """)
    return


@app.cell
def _():
    # Countries to analyze
    countries = {
        "ARG": "Argentina",
        "BRA": "Brazil",
        "COL": "Colombia",
        "MEX": "Mexico",
    }

    # Economic indicator codes
    gdp_indicator = "NY.GDP.MKTP.KD.ZG"
    inflation_indicator = "FP.CPI.TOTL.ZG"
    unemployment_indicator = "SL.UEM.TOTL.ZS"

    indicators = {
        gdp_indicator: "GDP Growth",
        inflation_indicator: "Inflation",
        unemployment_indicator: "Unemployment",
    }

    # Analysis period
    start_year = 2000
    end_year = 2024

    # API settings
    base_url = "https://api.worldbank.org/v2"
    records_per_page = 50
    request_timeout = 30

    # File destination
    output_file = "projects/mp2/data/economic_data.json"
    return (
        base_url,
        countries,
        end_year,
        gdp_indicator,
        indicators,
        inflation_indicator,
        output_file,
        records_per_page,
        request_timeout,
        start_year,
        unemployment_indicator,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work
    """)
    return


@app.cell
def _():
    import requests as mp2_requests
    import json as mp2_json
    from pathlib import Path as MP2Path

    return MP2Path, mp2_json, mp2_requests


@app.cell
def _(mp2_requests):
    def fetch_world_bank_records(
        api_url,
        country_codes,
        indicator_code,
        first_year,
        last_year,
        page_size,
        timeout_seconds,
    ):
        # Join the country codes in the format the API expects.
        # Example: ARG;BRA;COL;MEX
        _country_text = ";".join(country_codes)

        # Build the URL for one economic indicator.
        _url = (
            f"{api_url}/country/{_country_text}"
            f"/indicator/{indicator_code}"
        )

        # Start with an empty list and the first page.
        _records = []
        _page = 1
        _pages = 1
        _total = 0

        # Keep requesting pages until all pages have been fetched.
        while _page <= _pages:
            _response = mp2_requests.get(
                _url,
                params={
                    "format": "json",
                    "date": f"{first_year}:{last_year}",
                    "per_page": page_size,
                    "page": _page,
                },
                timeout=timeout_seconds,
            )

            # Stop with an error if the HTTP request failed.
            _response.raise_for_status()

            # Convert the JSON response into Python lists and dictionaries.
            _data = _response.json()

            # The API should return metadata followed by a list of records.
            if len(_data) != 2 or not isinstance(_data[1], list):
                raise ValueError("The API did not return a list of records.")

            # Read the number of pages and records reported by the API.
            _pages = int(_data[0]["pages"])
            _total = int(_data[0]["total"])

            # Add each record from this page to our list.
            for _record in _data[1]:
                _records.append(_record)

            # Move to the next page.
            _page += 1

        # Check that we fetched the number of records the API reported.
        if len(_records) != _total:
            raise ValueError("The number of fetched records is incorrect.")

        # Send the complete list back to the code that called the function.
        return _records

    return (fetch_world_bank_records,)


@app.cell
def _(
    base_url,
    countries,
    end_year,
    fetch_world_bank_records,
    indicators,
    records_per_page,
    request_timeout,
    start_year,
):
    mp2_fetched_records = []

    # Each indicator should have one record per country per year.
    # Adding 1 includes both the start year and the end year.
    _expected_records = (
        len(countries) * (end_year - start_year + 1)
    )

    # Fetch each indicator separately.
    for _indicator_code in indicators:
        _indicator_records = fetch_world_bank_records(
            base_url,
            countries,
            _indicator_code,
            start_year,
            end_year,
            records_per_page,
            request_timeout,
        )

        # Check that the country-year record count matches our inputs.
        # Records with missing values still count as records.
        if len(_indicator_records) != _expected_records:
            raise ValueError(
                f"Expected {_expected_records} records for "
                f"{indicators[_indicator_code]}, "
                f"but received {len(_indicator_records)}."
            )

        # Combine this indicator's records with the other indicators.
        for _record in _indicator_records:
            mp2_fetched_records.append(_record)

        print(
            f"{indicators[_indicator_code]}: "
            f"{len(_indicator_records)} records fetched"
        )
    return (mp2_fetched_records,)


@app.cell
def _(MP2Path, mp2_fetched_records, mp2_json, output_file):
    mp2_output_path = MP2Path(output_file)

    # Create the destination folders if they do not already exist.
    mp2_output_path.parent.mkdir(parents=True, exist_ok=True)

    # Open the file for writing and save the original fetched records.
    # indent=2 makes the JSON easier to read.
    # Missing values (None) are saved as JSON null.
    with mp2_output_path.open("w", encoding="utf-8") as _file:
        mp2_json.dump(
            mp2_fetched_records,
            _file,
            indent=2,
            allow_nan=False,
        )

    # Print the full path so we can find the saved file.
    print(
        f"Saved {len(mp2_fetched_records)} records to "
        f"{mp2_output_path.resolve()}"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer
    """)
    return


@app.cell
def _(
    countries,
    gdp_indicator,
    indicators,
    inflation_indicator,
    mp2_fetched_records,
    unemployment_indicator,
):
    mp2_country_results = {}

    for _country_code, _country_name in countries.items():
        _averages = {}
        _counts = {}

        # Calculate each indicator's average for this country.
        for _indicator_code in indicators:
            _total = 0
            _count = 0

            for _record in mp2_fetched_records:
                # Use only this country's records for this indicator.
                # Skip missing values instead of treating them as zero.
                if (
                    _record["countryiso3code"] == _country_code
                    and _record["indicator"]["id"] == _indicator_code
                    and _record["value"] is not None
                ):
                    _total += _record["value"]
                    _count += 1

            # An average cannot be calculated without any values.
            if _count == 0:
                raise ValueError(
                    f"No available {indicators[_indicator_code]} "
                    f"data for {_country_name}."
                )

            # Average = sum of available values / number of available values.
            _averages[_indicator_code] = _total / _count
            _counts[_indicator_code] = _count

        # Measure how much annual GDP growth differed from its average.
        _squared_difference_total = 0

        for _record in mp2_fetched_records:
            if (
                _record["countryiso3code"] == _country_code
                and _record["indicator"]["id"] == gdp_indicator
                and _record["value"] is not None
            ):
                _difference = (
                    _record["value"] - _averages[gdp_indicator]
                )

                # Squaring prevents positive and negative differences
                # from cancelling each other out.
                _squared_difference_total += _difference ** 2

        # Standard deviation is the square root of the average
        # squared difference. Raising a number to 0.5 takes its square root.
        _growth_sd = (
            _squared_difference_total / _counts[gdp_indicator]
        ) ** 0.5

        # Save this country's averages, stability measure, and data counts.
        mp2_country_results[_country_name] = {
            "gdp_growth": _averages[gdp_indicator],
            "inflation": _averages[inflation_indicator],
            "unemployment": _averages[unemployment_indicator],
            "growth_sd": _growth_sd,
            "counts": _counts,
        }
    return (mp2_country_results,)


@app.cell
def _(
    end_year,
    gdp_indicator,
    inflation_indicator,
    mp2_country_results,
    start_year,
    unemployment_indicator,
):
    print(f"Economic comparison, {start_year}–{end_year}")
    print("Average rates (%); growth SD in percentage points")
    print()

    print(
        f"{'Country':<12}"
        f"{'GDP growth':>12}"
        f"{'Inflation':>12}"
        f"{'Unemployment':>15}"
        f"{'Growth SD':>12}"
        f"{'Years G/I/U':>15}"
    )
    print("-" * 78)

    for _country_name, _result in mp2_country_results.items():
        # Show how many years contributed to each average:
        # GDP growth / inflation / unemployment.
        _coverage = (
            f"{_result['counts'][gdp_indicator]}/"
            f"{_result['counts'][inflation_indicator]}/"
            f"{_result['counts'][unemployment_indicator]}"
        )

        print(
            f"{_country_name:<12}"
            f"{_result['gdp_growth']:>12.2f}"
            f"{_result['inflation']:>12.2f}"
            f"{_result['unemployment']:>15.2f}"
            f"{_result['growth_sd']:>12.2f}"
            f"{_coverage:>15}"
        )

    print()
    print("Lower Growth SD means GDP growth fluctuated less.")
    return


@app.cell
def _(end_year, mp2_country_results, start_year):
    mp2_best_growth = None
    mp2_lowest_inflation = None
    mp2_lowest_unemployment = None
    mp2_lowest_growth_sd = None

    # These strings will hold the names of the leading countries.
    mp2_growth_country = ""
    mp2_inflation_country = ""
    mp2_unemployment_country = ""
    mp2_stability_country = ""

    for _country_name, _result in mp2_country_results.items():
        # Give the current country's results shorter names.
        _growth = _result["gdp_growth"]
        _inflation = _result["inflation"]
        _unemployment = _result["unemployment"]
        _stability = _result["growth_sd"]

        # Keep the highest average GDP growth.
        # The first country becomes the initial leader.
        if mp2_best_growth is None or _growth > mp2_best_growth:
            mp2_best_growth = _growth
            mp2_growth_country = _country_name
        elif _growth == mp2_best_growth:
            # Include both countries if their results are exactly equal.
            mp2_growth_country += f" and {_country_name}"

        # Keep the lowest average inflation.
        if (
            mp2_lowest_inflation is None
            or _inflation < mp2_lowest_inflation
        ):
            mp2_lowest_inflation = _inflation
            mp2_inflation_country = _country_name
        elif _inflation == mp2_lowest_inflation:
            mp2_inflation_country += f" and {_country_name}"

        # Keep the lowest average unemployment.
        if (
            mp2_lowest_unemployment is None
            or _unemployment < mp2_lowest_unemployment
        ):
            mp2_lowest_unemployment = _unemployment
            mp2_unemployment_country = _country_name
        elif _unemployment == mp2_lowest_unemployment:
            mp2_unemployment_country += f" and {_country_name}"

        # Keep the lowest GDP growth standard deviation.
        # A lower value means annual growth fluctuated less.
        if (
            mp2_lowest_growth_sd is None
            or _stability < mp2_lowest_growth_sd
        ):
            mp2_lowest_growth_sd = _stability
            mp2_stability_country = _country_name
        elif _stability == mp2_lowest_growth_sd:
            mp2_stability_country += f" and {_country_name}"

    # Print one sentence using the calculated names and numbers.
    # The answer changes when the input data changes.
    print(
        f"Using available data from {start_year} to {end_year}, "
        f"{mp2_growth_country} had the highest average GDP growth "
        f"({mp2_best_growth:.2f}%), "
        f"{mp2_inflation_country} had the lowest average inflation "
        f"({mp2_lowest_inflation:.2f}%), "
        f"{mp2_unemployment_country} had the lowest average unemployment "
        f"({mp2_lowest_unemployment:.2f}%), and "
        f"{mp2_stability_country} had the most stable GDP growth "
        f"(standard deviation {mp2_lowest_growth_sd:.2f} percentage points), "
        f"showing different strengths relevant to business expansion."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right?

    I check the first country's average GDP growth a second way. Instead of
    using the records collected earlier, I request each year's GDP growth
    separately from the World Bank API and calculate the average again.

    The code prints both averages, the number of available years, and whether
    the results agree. Missing values are excluded in both calculations.
    """)
    return


@app.cell
def _(
    base_url,
    countries,
    end_year,
    gdp_indicator,
    mp2_country_results,
    mp2_requests,
    request_timeout,
    start_year,
):
    # Select the first country from the Inputs dictionary.
    mp2_check_country_code = ""

    for _country_code in countries:
        mp2_check_country_code = _country_code
        break

    mp2_check_country_name = countries[mp2_check_country_code]

    # Get the average already calculated for the result table.
    mp2_original_average = (
        mp2_country_results[mp2_check_country_name]["gdp_growth"]
    )

    # Calculate a second average using separate requests for each year.
    mp2_check_total = 0
    mp2_check_count = 0

    for _year in range(start_year, end_year + 1):
        _url = (
            f"{base_url}/country/{mp2_check_country_code}"
            f"/indicator/{gdp_indicator}"
        )

        _response = mp2_requests.get(
            _url,
            params={
                "format": "json",
                "date": _year,
            },
            timeout=request_timeout,
        )
        _response.raise_for_status()
        _reply = _response.json()

        # One country, one indicator, and one year should give one record.
        if (
            len(_reply) != 2
            or not isinstance(_reply[1], list)
            or len(_reply[1]) != 1
        ):
            raise ValueError(f"Unexpected API response for {_year}.")

        for _record in _reply[1]:
            # Skip missing values, just as the original calculation does.
            if _record["value"] is not None:
                mp2_check_total += _record["value"]
                mp2_check_count += 1

    if mp2_check_count == 0:
        raise ValueError("No values were available for the check.")

    mp2_second_average = mp2_check_total / mp2_check_count

    # Also compare the number of values used in each calculation.
    mp2_original_count = (
        mp2_country_results[mp2_check_country_name]["counts"][gdp_indicator]
    )

    # Allow a tiny difference caused by decimal arithmetic.
    mp2_check_passed = (
        abs(mp2_original_average - mp2_second_average) < 0.000001
        and mp2_original_count == mp2_check_count
    )

    # Show both numbers and the result of the check.
    print(
        f"Checking {mp2_check_country_name}'s average GDP growth, "
        f"{start_year}–{end_year}"
    )
    print(f"Original average:      {mp2_original_average:.6f}%")
    print(f"Second average:        {mp2_second_average:.6f}%")
    print(f"Original years used:   {mp2_original_count}")
    print(f"Second years used:     {mp2_check_count}")

    if mp2_check_passed:
        print("PASS: The two averages and their year counts agree.")
    else:
        print("FAIL: The results differ and need investigation.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    One suggestion I did not accept as-is was the use of list and dictionary
    comprehensions. These put several steps into one line, but the assignment
    requires explicit `for` loops when processing lists. I also found loops
    easier to understand and explain.

    I asked for this part to be revised using separate steps. In Section 5,
    The Answer, Cell 1, the calculation now goes through the records, adds
    the available values, counts them, and divides the total by the count.
    Missing values are skipped instead of being counted as zero.

    I checked the revised cell against the assignment instructions to confirm
    that it uses explicit loops. Section 6 provides an additional check of
    the calculation by requesting each year's GDP growth separately and
    printing the new average beside the original average. This lets me check
    whether the change still produces the same result.
    """)
    return


if __name__ == "__main__":
    app.run()
