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
    # CrossFit Gym — Part B

    ## 3. Reading It Back

    I predict that joining Coaches, Classes, and Bookings will produce **1,236 rows** before filtering or grouping. Each of the 1,234 bookings contributes one row, and the left join keeps one extra row for each of the two classes without bookings. Every coach teaches at least one class, so there are no additional rows for coaches without classes.
    """)
    return


if __name__ == "__main__":
    app.run()
