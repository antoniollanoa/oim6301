import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import matplotlib.pyplot as plt

    print("DuckDB version:", duckdb.__version__)
    return duckdb, mo, plt


@app.cell
def _(mo):
    # Find the folder containing this notebook.
    project_folder = mo.notebook_dir()

    # Define the database and CSV locations.
    database = project_folder / "database.duckdb"
    data_folder = project_folder / "data"

    print("Project folder:", project_folder)
    print("Data folder exists:", data_folder.exists())

    for _file_name in [
        "members.csv",
        "coaches.csv",
        "workouts.csv",
        "classes.csv",
        "bookings.csv",
    ]:
        print(_file_name, "found:", (data_folder / _file_name).exists())
    return data_folder, database


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1. The Tables
    """)
    return


@app.cell
def _(data_folder, database, duckdb):
    # Remove the previous generated database before rebuilding.
    if database.exists():
        database.unlink()

    # Create tables, load data, create the view, and close the connection.
    with duckdb.connect(database) as _con:
        _con.execute("""
            CREATE TABLE members (
                member_id INTEGER PRIMARY KEY,
                membership_number VARCHAR NOT NULL UNIQUE,
                member_name VARCHAR NOT NULL,
                email VARCHAR NOT NULL
            )
        """)

        _con.execute("""
            CREATE TABLE coaches (
                coach_id INTEGER PRIMARY KEY,
                coach_name VARCHAR NOT NULL
            )
        """)

        _con.execute("""
            CREATE TABLE workouts (
                workout_id INTEGER PRIMARY KEY,
                workout_name VARCHAR NOT NULL,
                description VARCHAR NOT NULL
            )
        """)

        _con.execute("""
            CREATE TABLE classes (
                class_id INTEGER PRIMARY KEY,
                coach_id INTEGER NOT NULL REFERENCES coaches(coach_id),
                workout_id INTEGER NOT NULL REFERENCES workouts(workout_id),
                start_time TIMESTAMP NOT NULL,
                capacity INTEGER NOT NULL CHECK (capacity > 0),
                standard_price DECIMAL(10, 2) NOT NULL
                    CHECK (standard_price >= 0)
            )
        """)

        _con.execute("""
            CREATE TABLE bookings (
                member_id INTEGER REFERENCES members(member_id),
                class_id INTEGER REFERENCES classes(class_id),
                booked_at TIMESTAMP NOT NULL,
                status VARCHAR NOT NULL DEFAULT 'Booked',
                agreed_charge DECIMAL(10, 2) NOT NULL,
                PRIMARY KEY (member_id, class_id),
                CHECK (
                    status IN ('Booked', 'Attended', 'No-show', 'Cancelled')
                ),
                CHECK (agreed_charge >= 0),
                CHECK (status != 'Cancelled' OR agreed_charge = 0)
            )
        """)

        # Load reference tables before tables that depend on them.
        _con.execute(
            "COPY members FROM ? (HEADER, DELIMITER ',')",
            [str(data_folder / "members.csv")],
        )

        _con.execute(
            "COPY coaches FROM ? (HEADER, DELIMITER ',')",
            [str(data_folder / "coaches.csv")],
        )

        _con.execute(
            "COPY workouts FROM ? (HEADER, DELIMITER ',')",
            [str(data_folder / "workouts.csv")],
        )

        _con.execute(
            "COPY classes FROM ? (HEADER, DELIMITER ',')",
            [str(data_folder / "classes.csv")],
        )

        _con.execute(
            "COPY bookings FROM ? (HEADER, DELIMITER ',')",
            [str(data_folder / "bookings.csv")],
        )

        # Save a reusable class booking and attendance report.
        _con.execute("""
            CREATE VIEW class_booking_summary AS
            SELECT
                c.class_id,
                c.start_time,
                c.capacity,
                COUNT(b.member_id) AS total_bookings,
                SUM(
                    CASE
                        WHEN b.status != 'Cancelled' THEN 1
                        ELSE 0
                    END
                ) AS reserved_places,
                SUM(
                    CASE
                        WHEN b.status = 'Attended' THEN 1
                        ELSE 0
                    END
                ) AS attended_count
            FROM classes AS c
            LEFT JOIN bookings AS b
                ON c.class_id = b.class_id
            GROUP BY
                c.class_id,
                c.start_time,
                c.capacity
        """)

        print("Database rebuilt, all five CSV files loaded, and view created.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2. The Data

    The data was generated by `make_data.py` and saved in five CSV files
    inside the `data` folder. All people and business records are fictional.

    The dataset covers November 1, 2025, through October 31, 2026.
    The `as_of` date is October 31, 2026.

    The gym schedules one class at 6 p.m. every Monday, Wednesday, and
    Friday. Each class has a capacity of eight and a standard price of $25.

    ### Dataset size

    - 10 members
    - 10 coaches, including part-time and substitute coaches
    - 10 workout templates
    - 156 scheduled classes
    - 1,234 bookings

    Classes and bookings together contain 1,390 activity records,
    exceeding the required minimum of 1,000.

    ### Repeatable generation

    The script uses fixed random seeds: 6301 for workout selection and
    6302 for bookings. Running the same script again produces the same data.

    ### Records with no related activity

    - Member 10 has no bookings.
    - Classes 1 and 2 have no bookings.

    These records let us check that queries include members and classes
    even when they have no related bookings.

    ### Deliberate rule violations

    1. Classes 3 and 4 each have nine non-cancelled bookings despite a
       capacity of eight. Each class exceeds capacity by one reservation.
       These are the only two classes that break the capacity rule.

    2. Exactly two bookings for class 5 were recorded on November 12, 2025,
       at 6:15 p.m., after the class started at 6 p.m. Their composite keys are:

       - `member_id = 9`, `class_id = 5`
       - `member_id = 2`, `class_id = 5`

       These are the only two booking records that break the booking-time rule.

    The table constraints allow these records to load because checking
    these rules requires other rows or another table. Queries will identify
    the exceptions.

    ### Attendance and charges

    Bookings use the final statuses Attended, No-show, and Cancelled because
    the scheduled classes are in the past. Booked remains an allowed status
    for future reservations.

    Cancelled bookings have a zero charge and do not reserve a place.
    Other bookings have an agreed charge of $25.

    For this project, attended-booking revenue means the sum of agreed
    charges for bookings marked Attended. It does not represent verified
    cash payments, because payments are outside the project scope.

    ### Checks performed before loading

    The generation script checks that:

    - Member 10 is the only member without bookings.
    - Classes 1 and 2 are the only classes without bookings.
    - Classes 3 and 4 are the only over-capacity classes.
    - Exactly two booking records were created after their class started.

    All four checks passed before the CSV files were loaded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. A Look at the Data
    """)
    return


@app.cell
def _(ask):
    status_counts = ask("""
        SELECT
            status,
            COUNT(*) AS booking_count
        FROM bookings
        GROUP BY status
        ORDER BY status
    """)

    status_counts
    return (status_counts,)


@app.cell
def _(plt, status_counts):
    status_figure = plt.figure(figsize=(7, 4))

    status_bars = plt.bar(
        status_counts["status"].to_list(),
        status_counts["booking_count"].to_list(),
        color="red",
    )

    plt.bar_label(status_bars, padding=3)

    plt.title("CrossFit Class Booking Outcomes")
    plt.xlabel("Booking Status")
    plt.ylabel("Number of Bookings")
    plt.margins(y=0.15)
    plt.tight_layout()

    status_figure
    return


@app.cell
def _(mo):
    mo.md("""
    Most bookings resulted in attendance, while smaller groups were
    cancelled or became no-shows. This is a reasonable general pattern
    for our fictional gym, although the proportions are simulated rather
    than estimated from a real gym's records.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 4. Row Counts
    """)
    return


@app.cell
def _(ask):
    row_counts = ask("""
        SELECT 'members' AS table_name, COUNT(*) AS row_count
        FROM members

        UNION ALL

        SELECT 'coaches', COUNT(*)
        FROM coaches

        UNION ALL

        SELECT 'workouts', COUNT(*)
        FROM workouts

        UNION ALL

        SELECT 'classes', COUNT(*)
        FROM classes

        UNION ALL

        SELECT 'bookings', COUNT(*)
        FROM bookings

        ORDER BY table_name
    """)

    row_counts
    return (row_counts,)


@app.cell
def _(row_counts):
    expected_row_counts = {
        "bookings": 1234,
        "classes": 156,
        "coaches": 10,
        "members": 10,
        "workouts": 10,
    }

    for _row in row_counts.to_dicts():
        _table_name = _row["table_name"]
        _actual_count = _row["row_count"]
        _expected_count = expected_row_counts[_table_name]

        print(
            _table_name,
            "| Expected:", _expected_count,
            "| Actual:", _actual_count,
        )

        assert _actual_count == _expected_count

    print("All five database row counts match.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 5. A Row It Refuses
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO classes (
                    class_id,
                    coach_id,
                    workout_id,
                    start_time,
                    capacity,
                    standard_price
                )
                VALUES (
                    9999,
                    1,
                    1,
                    TIMESTAMP '2026-10-31 18:00:00',
                    0,
                    25.00
                )
            """)

    except duckdb.ConstraintException as _error:
        print("The database refused the invalid class:")
        print(_error)
    return


@app.cell
def _(ask):
    ask("""
        SELECT COUNT(*) AS invalid_class_count
        FROM classes
        WHERE class_id = 9999
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    The database rejected a class with capacity zero because the Classes
    table requires capacity to be greater than zero. A follow-up query
    confirmed that class 9999 was not inserted.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 6. Answers You Already Knew
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    **Expected answer:** Member 10 is the only member without bookings.
    """)
    return


@app.cell
def _(ask):
    members_without_bookings_result = ask("""
        SELECT
            m.member_id,
            m.member_name
        FROM members AS m
        LEFT JOIN bookings AS b
            ON m.member_id = b.member_id
        WHERE b.member_id IS NULL
        ORDER BY m.member_id
    """)

    members_without_bookings_result
    return (members_without_bookings_result,)


@app.cell
def _(members_without_bookings_result):
    assert members_without_bookings_result["member_id"].to_list() == [10]

    print("Member check passed: only member 10 has no bookings.")
    return


@app.cell
def _(mo):
    mo.md("""
    **Expected answer:** Classes 1 and 2 are the only classes without bookings.
    """)
    return


@app.cell
def _(ask):
    classes_without_bookings_result = ask("""
        SELECT
            c.class_id,
            c.start_time
        FROM classes AS c
        LEFT JOIN bookings AS b
            ON c.class_id = b.class_id
        WHERE b.class_id IS NULL
        ORDER BY c.class_id
    """)

    classes_without_bookings_result
    return (classes_without_bookings_result,)


@app.cell
def _(classes_without_bookings_result):
    assert classes_without_bookings_result["class_id"].to_list() == [1, 2]

    print("Class check passed: only classes 1 and 2 have no bookings.")
    return


@app.cell
def _(mo):
    mo.md("""
    **Expected answer:** Exactly two bookings were made after their class
    started. Both belong to class 5 and were recorded at 6:15 p.m. on
    November 12, 2025.
    """)
    return


@app.cell
def _(ask):
    late_bookings_result = ask("""
        SELECT
            b.member_id,
            b.class_id,
            b.booked_at,
            c.start_time
        FROM bookings AS b
        JOIN classes AS c
            ON b.class_id = c.class_id
        WHERE b.booked_at > c.start_time
        ORDER BY b.member_id
    """)

    late_bookings_result
    return (late_bookings_result,)


@app.cell
def _(late_bookings_result):
    assert late_bookings_result.height == 2
    assert late_bookings_result["class_id"].to_list() == [5, 5]

    print("Late-booking check passed: exactly two records, both for class 5.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 7. A View

    The gym owner can use `class_booking_summary` to review bookings,
    reserved places, and attendance for each class. The query below
    shows the final calendar week covered by our dataset.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT *
        FROM class_booking_summary
        WHERE start_time >= TIMESTAMP '2026-10-26 00:00:00'
          AND start_time < TIMESTAMP '2026-11-02 00:00:00'
        ORDER BY start_time
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT *
        FROM class_booking_summary
        WHERE class_id IN (1, 2)
        ORDER BY class_id
    """)
    return


@app.cell
def _(ask):
    capacity_violations = ask("""
        SELECT
            class_id,
            capacity,
            reserved_places,
            reserved_places - capacity AS excess_places
        FROM class_booking_summary
        WHERE reserved_places > capacity
        ORDER BY class_id
    """)

    capacity_violations
    return (capacity_violations,)


@app.cell
def _(capacity_violations):
    assert capacity_violations["class_id"].to_list() == [3, 4]
    assert capacity_violations["excess_places"].to_list() == [1, 1]

    print("Capacity check passed: classes 3 and 4 each exceed capacity by one.")
    return


if __name__ == "__main__":
    app.run()
