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
    # 🥗 **Calorie Intake Tracker**
    """)
    return


@app.cell
def _():
    breakfast = 190+60
    breakfast
    return (breakfast,)


@app.cell
def _():
    snack_1 = 100
    snack_1
    return (snack_1,)


@app.cell
def _():
    lunch = 1000
    lunch
    return (lunch,)


@app.cell
def _():
    snack_2 = 250
    snack_2
    return (snack_2,)


@app.cell
def _():
    dinner = 250
    dinner
    return (dinner,)


@app.cell
def _(breakfast, dinner, lunch, snack_1, snack_2):
    total_calorie_intake = breakfast + snack_1 + lunch + snack_2 + dinner
    total_calorie_intake
    return (total_calorie_intake,)


@app.cell
def _():
    TDEE = 2600
    TDEE
    return (TDEE,)


@app.cell
def _(TDEE, total_calorie_intake):
    calorie_deficit = TDEE - total_calorie_intake
    calorie_deficit
    return


@app.cell
def _(TDEE, total_calorie_intake):
    percentage = round(total_calorie_intake / TDEE * 100) 
    print(f"{percentage}%")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---------------------------------------------------------------------------------------------------------------------------------------
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🎯 **Weight Tracker**
    """)
    return


@app.cell
def _():
    import pandas as pd
    import altair as alt
    from pathlib import Path
    from datetime import date

    return (pd,)


@app.cell
def _():
    weight_data = {
        "2026-10-11": 86.5,
        "2026-10-12": 85.9,
        "2026-10-13": 86.6
    }
    return (weight_data,)


@app.cell
def _(pd, weight_data):
    df = pd.DataFrame(
        weight_data.items(),
        columns=["Date", "Weight"]
    )

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    df["7-Day Average"] = (
        df["Weight"]
        .rolling(7, min_periods=1)
        .mean()
    )

    df
    return


@app.cell
def _():
    import matplotlib.pyplot as plt

    return (plt,)


@app.cell
def _(plt, weight_data):
    dates = list(weight_data.keys())
    weights = list(weight_data.values())

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(dates, weights, marker="o", color="blue")

    ax.set_title("My Daily Weight Progress")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")

    ax.set_ylim(0, 100)
    ax.grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()

    fig
    return


if __name__ == "__main__":
    app.run()
