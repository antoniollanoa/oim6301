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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer
    """)
    return


if __name__ == "__main__":
    app.run()
