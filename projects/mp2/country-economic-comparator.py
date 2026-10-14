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
        _url = (
            f"{api_url.rstrip('/')}/country/"
            f"{';'.join(country_codes)}/indicator/{indicator_code}"
        )

        _records = []
        _page = 1
        _pages = None
        _total = None

        while _pages is None or _page <= _pages:
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
            _payload = _response.json()

            if (
                not isinstance(_payload, list)
                or len(_payload) != 2
                or not isinstance(_payload[0], dict)
                or not isinstance(_payload[1], list)
            ):
                raise ValueError(
                    f"Unexpected response for {indicator_code}, page {_page}."
                )

            _metadata, _page_records = _payload
            _reported_page = int(_metadata["page"])
            _reported_pages = int(_metadata["pages"])
            _reported_total = int(_metadata["total"])

            if _reported_page != _page:
                raise ValueError("The API returned an unexpected page.")

            if _pages is None:
                _pages = _reported_pages
                _total = _reported_total

                if _pages < 1:
                    raise ValueError("The API reported no result pages.")

            elif _reported_pages != _pages or _reported_total != _total:
                raise ValueError("API totals changed during pagination.")

            for _page_record in _page_records:
                _records.append(_page_record)

            _page += 1

        if len(_records) != _total:
            raise ValueError(
                f"{indicator_code}: expected {_total} records, "
                f"received {len(_records)}."
            )

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
    economic_records = []
    mp2_fetch_summary = {}

    _country_codes = []
    for _country_code in countries:
        _country_codes.append(_country_code)

    _expected_per_indicator = (
        len(countries) * (end_year - start_year + 1)
    )

    for _indicator_code, _indicator_name in indicators.items():
        _raw_records = fetch_world_bank_records(
            base_url,
            _country_codes,
            _indicator_code,
            start_year,
            end_year,
            records_per_page,
            request_timeout,
        )

        _seen = {}
        _missing_count = 0

        for _record in _raw_records:
            _country_code = _record["countryiso3code"]
            _year = int(_record["date"])

            if _country_code not in countries:
                raise ValueError(f"Unexpected country: {_country_code}")

            if not start_year <= _year <= end_year:
                raise ValueError(f"Unexpected year: {_year}")

            if _record["indicator"]["id"] != _indicator_code:
                raise ValueError("The API returned an unexpected indicator.")

            _key = (_country_code, _year)

            if _key in _seen:
                raise ValueError(
                    f"Duplicate record: {_indicator_code}, {_key}"
                )

            _seen[_key] = True
            _value = _record["value"]

            if _value is None:
                _missing_count += 1

            mp2_fetched_records.append(_record)

            economic_records.append({
                "country_code": _country_code,
                "country": countries[_country_code],
                "year": _year,
                "indicator_code": _indicator_code,
                "indicator": _indicator_name,
                "value": _value,
            })

        if len(_seen) != _expected_per_indicator:
            raise ValueError(
                f"{_indicator_name}: expected {_expected_per_indicator} "
                f"country-year records, received {len(_seen)}."
            )

        mp2_fetch_summary[_indicator_name] = {
            "records": len(_raw_records),
            "missing_values": _missing_count,
        }

    mp2_fetch_summary
    return economic_records, mp2_fetched_records


@app.cell
def _(MP2Path, mp2_fetched_records, mp2_json, output_file):
    mp2_output_path = MP2Path(output_file)
    mp2_output_path.parent.mkdir(parents=True, exist_ok=True)

    with mp2_output_path.open("w", encoding="utf-8") as _json_file:
        mp2_json.dump(
            mp2_fetched_records,
            _json_file,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )

    print(
        f"Saved {len(mp2_fetched_records)} fetched records to "
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
    economic_records,
    end_year,
    gdp_indicator,
    indicators,
    inflation_indicator,
    start_year,
    unemployment_indicator,
):
    mp2_country_results = {}

    for _country_code, _country_name in countries.items():
        _values_by_indicator = {}

        for _indicator_code in indicators:
            _values_by_indicator[_indicator_code] = []

        for _record in economic_records:
            if (
                _record["country_code"] == _country_code
                and start_year <= _record["year"] <= end_year
                and _record["value"] is not None
            ):
                _values_by_indicator[_record["indicator_code"]].append(
                    _record["value"]
                )

        _averages = {}
        _counts = {}

        for _indicator_code, _values in _values_by_indicator.items():
            if not _values:
                raise ValueError(
                    f"No available data for {_country_name}: "
                    f"{indicators[_indicator_code]}"
                )

            _value_total = 0

            for _value in _values:
                _value_total += _value

            _averages[_indicator_code] = _value_total / len(_values)
            _counts[_indicator_code] = len(_values)

        _growth_values = _values_by_indicator[gdp_indicator]
        _growth_average = _averages[gdp_indicator]

        if len(_growth_values) < 2:
            raise ValueError(
                f"Not enough GDP growth data for {_country_name}."
            )

        _squared_difference_total = 0

        for _growth_value in _growth_values:
            _squared_difference_total += (
                _growth_value - _growth_average
            ) ** 2

        _growth_sd = (
            _squared_difference_total / len(_growth_values)
        ) ** 0.5

        mp2_country_results[_country_code] = {
            "country": _country_name,
            "gdp_growth": _growth_average,
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
    print("Period averages (%); GDP growth SD in percentage points")
    print()

    print(
        f"{'Country':<12}"
        f"{'GDP growth':>13}"
        f"{'Inflation':>13}"
        f"{'Unemployment':>15}"
        f"{'Growth SD':>12}"
        f"{'Years G/I/U':>15}"
    )
    print("-" * 80)

    for _result in mp2_country_results.values():
        _year_counts = (
            f"{_result['counts'][gdp_indicator]}/"
            f"{_result['counts'][inflation_indicator]}/"
            f"{_result['counts'][unemployment_indicator]}"
        )

        print(
            f"{_result['country']:<12}"
            f"{_result['gdp_growth']:>13.2f}"
            f"{_result['inflation']:>13.2f}"
            f"{_result['unemployment']:>15.2f}"
            f"{_result['growth_sd']:>12.2f}"
            f"{_year_counts:>15}"
        )

    print()
    print("Lower Growth SD means annual GDP growth fluctuated less.")
    return


@app.function
def mp2_find_leaders(results, metric, highest=False):
    _best_value = None
    _leader_names = []

    for _result in results.values():
        _value = _result[metric]

        if (
            _best_value is None
            or (highest and _value > _best_value)
            or (not highest and _value < _best_value)
        ):
            _best_value = _value
            _leader_names = [_result["country"]]

        elif _value == _best_value:
            _leader_names.append(_result["country"])

    if _best_value is None:
        raise ValueError("No results are available.")

    return " and ".join(_leader_names), _best_value


@app.cell
def _(end_year, mp2_country_results, start_year):
    mp2_growth_leaders, mp2_best_growth = mp2_find_leaders(
        mp2_country_results, "gdp_growth", highest=True
    )

    mp2_inflation_leaders, mp2_lowest_inflation = mp2_find_leaders(
        mp2_country_results, "inflation"
    )

    mp2_employment_leaders, mp2_lowest_unemployment = mp2_find_leaders(
        mp2_country_results, "unemployment"
    )

    mp2_stability_leaders, mp2_lowest_growth_sd = mp2_find_leaders(
        mp2_country_results, "growth_sd"
    )

    print(
        f"Across available observations from {start_year} to {end_year}, "
        f"{mp2_growth_leaders} recorded the highest average GDP growth "
        f"({mp2_best_growth:.2f}%), "
        f"{mp2_inflation_leaders} the lowest average inflation "
        f"({mp2_lowest_inflation:.2f}%), "
        f"{mp2_employment_leaders} the lowest average unemployment "
        f"({mp2_lowest_unemployment:.2f}%), and "
        f"{mp2_stability_leaders} the most stable GDP growth "
        f"(standard deviation {mp2_lowest_growth_sd:.2f} percentage points), "
        f"highlighting different economic strengths to consider "
        f"when evaluating business expansion."
    )
    return


if __name__ == "__main__":
    app.run()
