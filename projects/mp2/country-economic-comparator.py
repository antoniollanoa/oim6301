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
        indicators,
        output_file,
        records_per_page,
        request_timeout,
        start_year,
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
        _country_text = ";".join(country_codes)
        _url = (
            f"{api_url}/country/{_country_text}"
            f"/indicator/{indicator_code}"
        )

        _records = []
        _page = 1
        _pages = 1
        _total = 0

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
            _response.raise_for_status()
            _data = _response.json()

            if len(_data) != 2 or not isinstance(_data[1], list):
                raise ValueError("The API did not return a list of records.")

            _pages = int(_data[0]["pages"])
            _total = int(_data[0]["total"])

            for _record in _data[1]:
                _records.append(_record)

            _page += 1

        if len(_records) != _total:
            raise ValueError("The number of fetched records is incorrect.")

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

    _expected_records = (
        len(countries) * (end_year - start_year + 1)
    )

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

        if len(_indicator_records) != _expected_records:
            raise ValueError(
                f"Expected {_expected_records} records for "
                f"{indicators[_indicator_code]}, "
                f"but received {len(_indicator_records)}."
            )

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
    mp2_output_path.parent.mkdir(parents=True, exist_ok=True)

    with mp2_output_path.open("w", encoding="utf-8") as _file:
        mp2_json.dump(
            mp2_fetched_records,
            _file,
            indent=2,
            allow_nan=False,
        )

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


if __name__ == "__main__":
    app.run()
