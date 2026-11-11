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

    return as_of, ask, mo


@app.cell
def _(ask):
    ask("SHOW TABLES")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 1. How many bookings does each class have?
    """)
    return


@app.cell
def _(ask):
    class_booking_counts = ask("""
        SELECT
            class_id,
            start_time,
            total_bookings
        FROM class_booking_summary
        ORDER BY start_time, class_id
    """)

    class_booking_counts
    return (class_booking_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counting all booking records, including cancellations, 152 classes had eight bookings each, classes 3 and 4 had nine each, and classes 1 and 2 had none.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2. Which members have never booked a class?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            m.member_id,
            m.member_name
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
        WHERE b.member_id IS NULL
        ORDER BY m.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One member has never booked a class. Cameron Diaz (member 10) has zero booking records.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3. Which days of the week have the most attended bookings?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            dayname(c.start_time) AS weekday,
            COUNT(*) AS attended_bookings
        FROM classes AS c
        JOIN bookings AS b
            ON c.class_id = b.class_id
        WHERE b.status = 'Attended'
        GROUP BY dayname(c.start_time)
        ORDER BY attended_bookings DESC, weekday
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Monday had the most attended bookings over the full dataset, with 290, followed by Wednesday with 284 and Friday with 276.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 4. How many attended bookings and how much revenue did each coach's classes generate?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            co.coach_id,
            co.coach_name,
            COUNT(CASE WHEN b.status = 'Attended' THEN 1 END)
                AS attended_bookings,
            SUM(CASE WHEN b.status = 'Attended' THEN b.agreed_charge ELSE 0 END)
                AS attended_revenue
        FROM coaches AS co
        LEFT JOIN classes AS c
            ON co.coach_id = c.coach_id
        LEFT JOIN bookings AS b
            ON c.class_id = b.class_id
        GROUP BY co.coach_id, co.coach_name
        ORDER BY attended_bookings DESC, co.coach_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Emma Torres and Olivia Santos tied for the highest attendance and attended-booking revenue, with 90 attended bookings and $2,250 in agreed charges each. Across all ten coaches, the gym recorded 850 attended bookings and $21,250 in agreed charges for those bookings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 5. How many attended bookings and how much revenue did each workout generate?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            w.workout_id,
            w.workout_name,
            COUNT(CASE WHEN b.status = 'Attended' THEN 1 END)
                AS attended_bookings,
            SUM(CASE WHEN b.status = 'Attended' THEN b.agreed_charge ELSE 0 END)
                AS attended_revenue
        FROM workouts AS w
        LEFT JOIN classes AS c
            ON w.workout_id = c.workout_id
        LEFT JOIN bookings AS b
            ON c.class_id = b.class_id
        GROUP BY w.workout_id, w.workout_name
        ORDER BY attended_bookings DESC, w.workout_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Row and Squat had the highest total attendance and attended-booking revenue, with 106 attended bookings and $2,650 in agreed charges. Rowing Intervals followed with 100 attended bookings and $2,500.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 6. Which members have the most no-shows?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            m.member_id,
            m.member_name,
            COUNT(*) AS no_show_count
        FROM members AS m
        JOIN bookings AS b
            ON m.member_id = b.member_id
        WHERE b.status = 'No-show'
        GROUP BY m.member_id, m.member_name
        ORDER BY no_show_count DESC, m.member_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Riley Davis had the most no-shows, with 31, followed by Avery Wilson with 29. Morgan Silva and Taylor Morgan tied at 27 each.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 7. Which bookings were recorded after their class started?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            b.member_id,
            b.class_id,
            b.booked_at,
            c.start_time
        FROM bookings AS b
        JOIN classes AS c
            ON b.class_id = c.class_id
        WHERE b.booked_at > c.start_time
        ORDER BY b.class_id, b.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two booking records broke the timing rule. Members 2 and 9 both booked class 5 at 6:15 p.m. on November 12, 2025, which was 15 minutes after the class started.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 8. Which classes exceeded their booking capacity?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            class_id,
            start_time,
            capacity,
            reserved_places,
            reserved_places - capacity AS places_over_capacity
        FROM class_booking_summary
        WHERE reserved_places > capacity
        ORDER BY class_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Classes 3 and 4 were the only classes over capacity. Each had nine non-cancelled bookings for eight available places, so each exceeded capacity by one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 9. Which former attendees have not attended in the last 30 days?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            m.member_id,
            m.member_name,
            MAX(CAST(c.start_time AS DATE)) AS last_attended
        FROM members AS m
        JOIN bookings AS b
            ON m.member_id = b.member_id
        JOIN classes AS c
            ON b.class_id = c.class_id
        WHERE b.status = 'Attended'
          AND CAST(c.start_time AS DATE) <= DATE '{as_of}'
        GROUP BY m.member_id, m.member_name
        HAVING MAX(CAST(c.start_time AS DATE))
            < DATE '{as_of}' - INTERVAL '29 days'
        ORDER BY last_attended, m.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of October 31, 2026, zero former attendees qualified for outreach. All nine members who had ever attended a class attended at least once between October 2 and October 31.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 10. What percentage of bookings were cancelled each month?
    """)
    return


@app.cell
def _(ask):
    monthly_cancellations = ask("""
        SELECT
            strftime(c.start_time, '%Y-%m') AS class_month,
            COUNT(*) AS total_bookings,
            COUNT(CASE WHEN b.status = 'Cancelled' THEN 1 END)
                AS cancelled_bookings,
            ROUND(
                100.0 * COUNT(CASE WHEN b.status = 'Cancelled' THEN 1 END)
                / COUNT(*),
                2
            ) AS cancellation_pct
        FROM classes AS c
        JOIN bookings AS b
            ON c.class_id = b.class_id
        GROUP BY class_month
        ORDER BY class_month
    """)

    monthly_cancellations
    return (monthly_cancellations,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Grouping bookings by the month the class took place, November 2025 had the lowest cancellation rate at 9.76% (8 of 82 bookings). The other 11 months each had a cancellation rate of 12.50%.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right

    I checked Question 1 by adding the booking counts for all classes and comparing the sum with a direct count of the Bookings table. I checked Question 10 by adding the monthly cancellation counts and comparing the sum with a direct count of cancelled bookings.
    """)
    return


@app.cell
def _(ask, class_booking_counts, monthly_cancellations):
    direct_booking_counts = ask("""
        SELECT
            COUNT(*) AS all_bookings,
            COUNT(CASE WHEN status = 'Cancelled' THEN 1 END)
                AS cancelled_bookings
        FROM bookings
    """)

    bookings_from_classes = class_booking_counts["total_bookings"].sum()
    bookings_counted_directly = direct_booking_counts["all_bookings"][0]

    cancellations_from_months = monthly_cancellations["cancelled_bookings"].sum()
    cancellations_counted_directly = direct_booking_counts["cancelled_bookings"][0]

    print("Q1: Sum of class counts =", bookings_from_classes)
    print("Q1: Direct count =", bookings_counted_directly)

    print("Q10: Sum of monthly cancellation counts =", cancellations_from_months)
    print("Q10: Direct cancellation count =", cancellations_counted_directly)

    assert bookings_from_classes == bookings_counted_directly
    assert cancellations_from_months == cancellations_counted_directly

    print("Both checks passed.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent

    The agent originally suggested comparing attendance by class start hour. When we reviewed the dataset, we found that every class started at 6 p.m., so the query would return only one time slot. I changed Question 3 in the README to compare weekdays, which gave the gym a meaningful comparison across its three class days.

    I checked the result against counts from the CSV files. The **Question 3 SQL cell** shows 290 attended bookings on Monday, 284 on Wednesday, and 276 on Friday.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # CrossFit Gym — Part B

    ## 3. Reading It Back

    I predict that joining Coaches, Classes, and Bookings will produce **1,236 rows** before filtering or grouping. Each of the 1,234 bookings contributes one row, and the left join keeps one extra row for each of the two classes without bookings. Every coach teaches at least one class, so there are no additional rows for coaches without classes.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT COUNT(*) AS joined_rows
        FROM coaches AS co
        LEFT JOIN classes AS c
            ON co.coach_id = c.coach_id
        LEFT JOIN bookings AS b
            ON c.class_id = b.class_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My prediction matched the result. The joins returned 1,236 rows before grouping: 1,234 booking rows and two additional rows for classes without bookings.

    In the final Question 4 report, one row summarizes one coach’s classes. For example, Emma Torres’s row shows 90 attended bookings and $2,250 in agreed charges for those bookings across the classes she taught.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Going Further

    I charted the monthly cancellation rates from Question 10 to see how they changed over time.
    """)
    return


@app.cell
def _(monthly_cancellations):
    import matplotlib.pyplot as plt

    cancellation_figure, cancellation_axis = plt.subplots(figsize=(11, 4))

    cancellation_months = monthly_cancellations["class_month"].to_list()
    cancellation_rates = monthly_cancellations["cancellation_pct"].to_list()

    cancellation_axis.plot(
        cancellation_months,
        cancellation_rates,
        color="red",
        marker="o",
    )

    for _month, _rate in zip(cancellation_months, cancellation_rates):
        cancellation_axis.annotate(
            f"{_rate:.2f}%",
            (_month, _rate),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=12,
        )

    cancellation_axis.set_title("Monthly Class Booking Cancellation Rate")
    cancellation_axis.set_xlabel("Class month")
    cancellation_axis.set_ylabel("Bookings cancelled (%)")
    cancellation_axis.set_ylim(0, 15)
    cancellation_axis.tick_params(axis="x", labelrotation=45)
    cancellation_figure.tight_layout()

    cancellation_figure
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The chart shows that the cancellation rate rose from 9.76% in November 2025 to 12.50% in December and stayed at that level for the remaining months. The flat line reflects how I generated the data: ordinary classes have one cancelled booking out of eight. A gym manager could use this chart to spot changes in cancellation rates once real booking data is available.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Time Spent

    10 hours.
    """)
    return


if __name__ == "__main__":
    app.run()
