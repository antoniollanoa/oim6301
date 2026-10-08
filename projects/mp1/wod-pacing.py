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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    This tool is designed for CrossFit athletes who want to improve their performance during AMRAP workouts (as many rounds as possible within a set time). It helps them understand how fast they need to complete each round to reach their goal and whether they should adjust their pace to avoid getting tired too quickly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Workout Inputs and Round Times`
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
    # Initialize all tracking variables to zero before analyzing the workout
    cumulative_time = 0       # Total time spent completing rounds so far
    completed_rounds = 0      # Number of rounds completed within the 20-minute limit
    total_round_time = 0      # Sum of all individual round times
    first_behind_round = 0    # First round where the athlete falls behind the target pace

    # Print the table headers to organize the workout results
    # The numbers after > define the space reserved for each column
    # The > symbol aligns the text to the right
    print(
        f"{'Round':>5} "
        f"{'Round Time':>12} "
        f"{'Total Time':>12} "
        f"{'Target Time':>13} "
        f"{'Difference':>12} "
        f"{'Status':>10}"
    )

    # Print a horizontal line to separate the headers from the results
    print("-" * 70)

    # Loop through every round, starting at round 1
    # len(round_times) counts how many rounds are stored in the list
    for round_number in range(1, len(round_times) + 1):

        # Get the time for the current round from the list
        # Subtract 1 because Python list indexes start at 0
        round_time = round_times[round_number - 1]

        # Add the current round time to the total elapsed workout time
        cumulative_time = cumulative_time + round_time

        # Add the current round time to calculate the average later
        total_round_time = total_round_time + round_time

        # Calculate when the athlete should finish this round
        # Example: Round 3 should finish at 3 * 80 = 240 seconds
        target_time = round_number * required_pace

        # Compare actual elapsed time with the target time
        # Negative difference means ahead; positive means behind
        difference = cumulative_time - target_time

        # Determine whether the athlete is ahead, behind, or on pace
        if cumulative_time < target_time:
            status = "Ahead"

        elif cumulative_time > target_time:
            status = "Behind"

            # Record the first round where the athlete falls behind
            # Only update this variable if no previous round was behind
            if first_behind_round == 0:
                first_behind_round = round_number

        else:
            status = "On pace"

        # Count the round only if it finishes within the workout time limit
        # For Cindy, the time limit is 1,200 seconds (20 minutes)
        if cumulative_time <= time_cap_seconds:
            completed_rounds = round_number

        # Print the results for the current round as one table row
        # .2f displays numbers with two decimal places
        # > aligns the values to the right for a cleaner table
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
    return (average_round_time,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Workout Performance Evaluation and Conclusion`
    """)
    return


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Required Pace Calculation Verification`
    """)
    return


@app.cell
def _(required_pace):
    # Manual answer: 1,200 seconds / 15 rounds = 80.
    expected_pace = 80

    # Compare with the result from Section 4.
    print(f"Expected pace:    {expected_pace:.2f} seconds per round")
    print(f"Main calculation: {required_pace:.2f} seconds per round")

    if expected_pace == required_pace:
        print("Verification passed: Both values match.")
    else:
        print("Verification failed: The values are different.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Independent Total Workout Time Verification`
    """)
    return


@app.cell
def _(cumulative_time, round_times):
    # Calculate the total workout time independently
    manual_total = sum(round_times)

    # Display both results to compare them
    print(f"Independent total: {manual_total} seconds")
    print(f"Main loop total:   {cumulative_time} seconds")

    # Check whether both calculations match
    if manual_total == cumulative_time:
        print("Verification passed: Both totals match.")
    else:
        print("Verification failed: The totals are different.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    The AI suggested calculating the total workout time by adding each round's time using a loop. Although the AI's calculation was correct, I wanted to verify it independently before relying on the results. To do this, I used Python's built-in `sum()` function to add all 15 round times directly from the list, instead of using the loop from my main analysis. I then created a separate Python cell to compare the total calculated using `sum()` with the cumulative time calculated by the original loop. Both methods produced the same result of 1,224 seconds, confirming that the AI's calculation was correct. This verification is shown in the **Independent Total Workout Time Verification** cell of my Marimo notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    For the Going Further section, I decided to explore how different pacing strategies could affect an athlete's performance during the Cindy workout. I compared two strategies: aggressive and controlled. In the aggressive strategy, the athlete starts by completing rounds quickly but gradually takes more time as the workout continues. In the controlled strategy, the athlete maintains a more consistent pace from the beginning to the end.

    To compare both strategies, I created two lists with different round times and used Python loops to calculate the average time per round, the total workout time, and the number of rounds completed within the 20-minute limit. The results showed that the aggressive strategy completed 13 rounds, while the controlled strategy completed 15 rounds. This helped me understand that starting a workout too fast may cause an athlete to slow down significantly in later rounds. On the other hand, maintaining a steady pace can help the athlete manage their energy and complete more rounds.

    This comparison goes beyond the main task because instead of only analyzing one workout performance, I tested two different approaches to see which one produced better results. The code and results can be found in the **Going Further – Pacing Strategy Comparison** section of my Marimo notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `1. Define Aggressive and Controlled Pacing Strategies`
    """)
    return


@app.cell
def _():
    aggressive_times = [
        60, 62, 65, 68, 72,
        76, 82, 88, 95, 102,
        110, 118, 125, 130, 135
    ]

    controlled_times = [
        76, 77, 77, 78, 78,
        79, 79, 80, 80, 80,
        81, 81, 82, 82, 83
    ]
    return aggressive_times, controlled_times


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `2. Aggressive vs. Controlled Pacing Performance Comparison`
    """)
    return


@app.cell
def _(aggressive_times, controlled_times, time_cap_seconds):
    # Initialize the tracking variables for the aggressive strategy
    aggressive_total = 0     # Total time spent completing all aggressive rounds
    aggressive_rounds = 0    # Number of rounds completed within the time limit

    # Loop through each round time in the aggressive strategy list
    for aggressive_round_time in aggressive_times:

        # Add the current round time to the total elapsed time
        aggressive_total = aggressive_total + aggressive_round_time

        # Check if the round was completed within the 20-minute time limit
        if aggressive_total <= time_cap_seconds:

            # Count the round only if it was completed within the time limit
            aggressive_rounds = aggressive_rounds + 1


    # Initialize the tracking variables for the controlled strategy
    controlled_total = 0     # Total time spent completing all controlled rounds
    controlled_rounds = 0    # Number of rounds completed within the time limit

    # Loop through each round time in the controlled strategy list
    for controlled_round_time in controlled_times:

        # Add the current round time to the total elapsed time
        controlled_total = controlled_total + controlled_round_time

        # Check if the round was completed within the 20-minute time limit
        if controlled_total <= time_cap_seconds:

            # Count the round only if it was completed within the time limit
            controlled_rounds = controlled_rounds + 1


    # Calculate the average time per round for both strategies
    # Divide the total time by the number of rounds in each list
    aggressive_average = aggressive_total / len(aggressive_times)
    controlled_average = controlled_total / len(controlled_times)

    # Print the table headers to organize the comparison results
    # < aligns text to the left, while > aligns text to the right
    # The numbers define the space reserved for each column
    print(
        f"{'Strategy':<15} "
        f"{'Avg. Round':>12} "
        f"{'Total Time':>12} "
        f"{'Rounds in Cap':>15}"
    )

    # Print a horizontal line to separate the headers from the results
    print("-" * 58)

    # Print the aggressive strategy results
    # .2f displays the average round time with two decimal places
    print(
        f"{'Aggressive':<15} "
        f"{aggressive_average:>12.2f} "
        f"{aggressive_total:>12} "
        f"{aggressive_rounds:>15}"
    )

    # Print the controlled strategy results using the same table format
    # This makes it easier to compare both strategies side by side
    print(
        f"{'Controlled':<15} "
        f"{controlled_average:>12.2f} "
        f"{controlled_total:>12} "
        f"{controlled_rounds:>15}"
    )
    return aggressive_rounds, controlled_rounds


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `3. Pacing Strategy Results and Conclusion`
    """)
    return


@app.cell
def _(aggressive_rounds, controlled_rounds):
    print(
        f"The aggressive strategy completed {aggressive_rounds} rounds "
        f"within the 20-minute limit, while the controlled strategy "
        f"completed {controlled_rounds} rounds."
    )

    if aggressive_rounds > controlled_rounds:
        print("The aggressive strategy completed more rounds.")
    elif controlled_rounds > aggressive_rounds:
        print("The controlled strategy completed more rounds.")
    else:
        print("Both strategies completed the same number of rounds.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `4. Pacing Strategy Comparison Visualization`
    """)
    return


@app.cell
def _(aggressive_times, controlled_times):
    # Import the library for creating graphs
    import matplotlib.pyplot as plt

    # Create the round numbers
    graph_round_numbers = list(range(1, len(aggressive_times) + 1))

    # Plot both pacing strategies
    plt.plot(graph_round_numbers, aggressive_times, label="Aggressive")
    plt.plot(graph_round_numbers, controlled_times, label="Controlled")

    # Add the graph title and labels
    plt.title("Aggressive vs. Controlled Pacing")
    plt.xlabel("Round Number")
    plt.ylabel("Time per Round (seconds)")

    # Display the legend and grid
    plt.legend()
    plt.grid(True)

    # Show the graph
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I also created a line graph to compare how the round times change under both pacing strategies. The graph shows that the aggressive strategy starts with faster rounds but becomes much slower toward the end. In comparison, the controlled strategy maintains a more consistent pace throughout the workout. This helps explain why managing pace is important during a 20-minute AMRAP workout.
    """)
    return


if __name__ == "__main__":
    app.run()
