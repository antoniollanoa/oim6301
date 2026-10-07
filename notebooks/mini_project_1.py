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
    # 📘Mini Project 1: CrossFit WOD Pacing Strategy Tool
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Context: CrossFit is a fitness program that combines strength, cardio, and bodyweight exercises. A WOD (Workout of the Day) is a specific workout completed for time or for as many rounds as possible within a set time. This project creates a pacing tool that calculates how fast an athlete needs to complete each round to reach a target and compares that pace with their actual performance.
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


@app.cell
def _(target_rounds, time_cap_minutes):
    time_cap_seconds = time_cap_minutes * 60
    required_pace = time_cap_seconds / target_rounds

    print(f"Total available time: {time_cap_seconds} seconds")
    print(f"Required pace: {required_pace:.2f} seconds per round")
    return required_pace, time_cap_seconds


@app.cell
def _(required_pace, round_times, time_cap_seconds):
    cumulative_time = 0
    completed_rounds = 0
    total_round_time = 0
    first_behind_round = 0

    print(
        f"{'Round':>5} "
        f"{'Round Time':>12} "
        f"{'Total Time':>12} "
        f"{'Target Time':>13} "
        f"{'Difference':>12} "
        f"{'Status':>10}"
    )

    print("-" * 70)

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
    return (
        completed_rounds,
        cumulative_time,
        first_behind_round,
        total_round_time,
    )


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
    return (average_round_time,)


@app.cell
def _(
    average_round_time,
    completed_rounds,
    first_behind_round,
    required_pace,
    target_rounds,
    workout_name,
):
    if completed_rounds >= target_rounds:
        print(
            f"The athlete achieved the target of {target_rounds} rounds of "
            f"{workout_name}. The required pace was {required_pace:.2f} seconds "
            f"per round, while the actual average pace was "
            f"{average_round_time:.2f} seconds per round."
        )
    else:
        print(
            f"The athlete did not achieve the target of {target_rounds} rounds of "
            f"{workout_name}. The athlete completed {completed_rounds} full rounds. "
            f"The required pace was {required_pace:.2f} seconds per round, while "
            f"the actual average pace was {average_round_time:.2f} seconds per round."
        )

    if first_behind_round > 0:
        print(f"The athlete first fell behind the target pace during round {first_behind_round}.")
    else:
        print("The athlete never fell behind the target cumulative pace.")
    return


@app.cell
def _():
    expected_pace = 80

    check_time = 20 * 60
    calculated_pace = check_time / 15

    print(f"Expected pace:   {expected_pace:.2f} seconds")
    print(f"Calculated pace: {calculated_pace:.2f} seconds")
    return


@app.cell
def _(round_times):
    expected_round_3_total = 216
    calculated_round_3_total = round_times[0] + round_times[1] + round_times[2]

    print(f"Expected time after round 3:   {expected_round_3_total} seconds")
    print(f"Calculated time after round 3: {calculated_round_3_total} seconds")
    return


if __name__ == "__main__":
    app.run()
