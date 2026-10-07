import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

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


if __name__ == "__main__":
    app.run()
