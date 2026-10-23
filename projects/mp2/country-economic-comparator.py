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

        for _indicator_code in indicators:
            _total = 0
            _count = 0

            for _record in mp2_fetched_records:
                if (
                    _record["countryiso3code"] == _country_code
                    and _record["indicator"]["id"] == _indicator_code
                    and _record["value"] is not None
                ):
                    _total += _record["value"]
                    _count += 1

            if _count == 0:
                raise ValueError(
                    f"No available {indicators[_indicator_code]} "
                    f"data for {_country_name}."
                )

            _averages[_indicator_code] = _total / _count
            _counts[_indicator_code] = _count

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
                _squared_difference_total += _difference ** 2

        _growth_sd = (
            _squared_difference_total / _counts[gdp_indicator]
        ) ** 0.5

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

    mp2_growth_country = ""
    mp2_inflation_country = ""
    mp2_unemployment_country = ""
    mp2_stability_country = ""

    for _country_name, _result in mp2_country_results.items():
        _growth = _result["gdp_growth"]
        _inflation = _result["inflation"]
        _unemployment = _result["unemployment"]
        _stability = _result["growth_sd"]

        if mp2_best_growth is None or _growth > mp2_best_growth:
            mp2_best_growth = _growth
            mp2_growth_country = _country_name
        elif _growth == mp2_best_growth:
            mp2_growth_country += f" and {_country_name}"

        if (
            mp2_lowest_inflation is None
            or _inflation < mp2_lowest_inflation
        ):
            mp2_lowest_inflation = _inflation
            mp2_inflation_country = _country_name
        elif _inflation == mp2_lowest_inflation:
            mp2_inflation_country += f" and {_country_name}"

        if (
            mp2_lowest_unemployment is None
            or _unemployment < mp2_lowest_unemployment
        ):
            mp2_lowest_unemployment = _unemployment
            mp2_unemployment_country = _country_name
        elif _unemployment == mp2_lowest_unemployment:
            mp2_unemployment_country += f" and {_country_name}"

        if (
            mp2_lowest_growth_sd is None
            or _stability < mp2_lowest_growth_sd
        ):
            mp2_lowest_growth_sd = _stability
            mp2_stability_country = _country_name
        elif _stability == mp2_lowest_growth_sd:
            mp2_stability_country += f" and {_country_name}"

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


if __name__ == "__main__":
    app.run()
