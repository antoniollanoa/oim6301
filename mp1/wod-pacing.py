# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📘 Mini Project 1: CrossFit WOD Pacing Strategy Tool

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tool is designed for CrossFit athletes who want to improve their performance during AMRAP workouts (as many rounds as possible within a set time). It helps them understand how fast they need to complete each round to reach their goal and whether they should adjust their pace to avoid getting tired too quickly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `How I Would Solve It`

    1. First, I would enter the workout name, time limit, target number of rounds, and the time taken to complete each round.

    2. Next, I would calculate the average time needed per round to reach the target.

    3. Then, I would use a loop to go through each round and add its time to the total time.

    4. After each round, I would compare the total time with the time the athlete should have taken to stay on pace.

    5. I would check whether the athlete is ahead, behind, or exactly on pace.

    6. Next, I would count how many full rounds the athlete completed within the time limit.

    7. Finally, I would print a table with the results and explain whether the athlete reached the target.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `What does your loop carry from one step to the next?`

    The loop carries the total time the athlete has spent completing the workout. It starts at zero and adds the time taken to complete each new round. For example, if the first round takes 70 seconds and the second takes 72 seconds, the total time becomes 142 seconds. The loop continues adding each round's time to the previous total and compares it with the target time to determine whether the athlete is ahead or behind the required pace.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Which check will you use in Section 6, and which two numbers should agree?`

    I will use two checks to make sure the program calculates the results correctly.

    First, I will check the required pace to complete 15 rounds of Cindy in 20 minutes. I know that 20 minutes equals 1,200 seconds, so the expected pace is 80 seconds per round. The manually calculated pace and the pace calculated by Python should both be 80 seconds.

    Second, I will check whether the program correctly adds the time spent completing each round. For example, if the first three rounds take 70, 72, and 74 seconds, the expected total time after round 3 is 216 seconds. I will compare this with the total time calculated by the Python loop. Both numbers should be exactly 216 seconds, confirming that the program correctly tracks the total workout time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    workout_name = "Cindy"
    time_cap_minutes = 20
    target_rounds = 15

    movements = [
        ("Pull-ups", 5),
        ("Push-ups", 10),
        ("Air squats", 15)
    ]

    round_times = [
        70, 72, 74, 75, 76,
        78, 80, 81, 83, 84,
        86, 88, 90, 92, 95
    ]
    return (
        movements,
        round_times,
        target_rounds,
        time_cap_minutes,
        workout_name,
    )


@app.cell
def _(movements, target_rounds, time_cap_minutes, workout_name):
    print(f"Workout: {workout_name}")
    print(f"Time cap: {time_cap_minutes} minutes")
    print(f"Target: {target_rounds} rounds")
    print()

    print("Movements:")
    for movement, reps in movements:
        print(f"{movement}: {reps} reps")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `1. Calculate Required Pace per Round`
    """)
    return


@app.cell
def _(target_rounds, time_cap_minutes):
    time_cap_seconds = time_cap_minutes * 60
    required_pace = time_cap_seconds / target_rounds

    print(f"Total available time: {time_cap_seconds} seconds")
    print(f"Required pace: {required_pace:.2f} seconds per round")
    return required_pace, time_cap_seconds


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `2. Round-by-Round Pacing Analysis`
    """)
    return


@app.cell
def _(required_pace, round_times, time_cap_seconds):
    # Initialize all tracking variables to zero
    cumulative_time = 0
    completed_rounds = 0
    total_round_time = 0
    first_behind_round = 0

    # Define table column headers and their widths
    print(
        f"{'Round':>5} "
        f"{'Round Time':>12} "
        f"{'Total Time':>12} "
        f"{'Target Time':>13} "
        f"{'Difference':>12} "
        f"{'Status':>10}"
    )

    # Print separator line for table formatting
    print("-" * 70)

    # Define round_time
    for round_number in range(1, len(round_times) + 1):
        round_time = round_times[round_number - 1]

        cumulative_time = cumulative_time + round_time
        total_round_time = total_round_time + round_time

        target_time = round_number * required_pace
        difference = cumulative_time - target_time

        if cumulative_time < target_time:
            status = "Ahead"
        elif cumulative_time > target_time:
            status = "Behind"
            if first_behind_round == 0:
                first_behind_round = round_number
        else:
            status = "On pace"

        if cumulative_time <= time_cap_seconds:
            completed_rounds = round_number

        print(
            f"{round_number:>5} "
            f"{round_time:>12.2f} "
            f"{cumulative_time:>12.2f} "
            f"{target_time:>13.2f} "
            f"{difference:>12.2f} "
            f"{status:>10}"
        )
    return completed_rounds, cumulative_time, total_round_time


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `3. Workout Performance Summary`
    """)
    return


@app.cell
def _(
    completed_rounds,
    cumulative_time,
    required_pace,
    round_times,
    target_rounds,
    time_cap_seconds,
    total_round_time,
):
    average_round_time = total_round_time / len(round_times)
    time_difference = time_cap_seconds - cumulative_time

    print(f"Required average pace: {required_pace:.2f} seconds per round")
    print(f"Actual average pace:   {average_round_time:.2f} seconds per round")
    print(f"Target rounds:         {target_rounds}")
    print(f"Completed rounds:      {completed_rounds}")
    print(f"Total time:            {cumulative_time} seconds")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
