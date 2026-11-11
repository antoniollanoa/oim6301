import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb

    as_of = "2026-10-31"
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, mo


@app.cell
def _(ask):
    ask("SHOW TABLES")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # CrossFit Gym — Part B

    ## 3. Reading It Back

    I predict that joining Coaches, Classes, and Bookings will produce **1,236 rows** before filtering or grouping. Each of the 1,234 bookings contributes one row, and the left join keeps one extra row for each of the two classes without bookings. Every coach teaches at least one class, so there are no additional rows for coaches without classes.
    """)
    return


if __name__ == "__main__":
    app.run()
