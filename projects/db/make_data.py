import csv
from pathlib import Path

import random
from datetime import datetime, timedelta

# Find the data folder beside this script.
project_folder = Path(__file__).parent
data_folder = project_folder / "data"
data_folder.mkdir(exist_ok=True)

# These are fictional names for our first sample.
member_names = [
    "Alex Rivera",
    "Jordan Lee",
    "Taylor Morgan",
    "Sam Patel",
    "Casey Brooks",
    "Jamie Chen",
    "Riley Davis",
    "Morgan Silva",
    "Avery Wilson",
    "Cameron Diaz",
]

members = []
member_number = 1

for member_name in member_names:
    member = {
        "member_id": member_number,
        "membership_number": "CF-" + str(member_number),
        "member_name": member_name,
        "email": "member" + str(member_number) + "@example.com",
    }

    members.append(member)
    member_number = member_number + 1

members_file = data_folder / "members.csv"

with members_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "member_id",
            "membership_number",
            "member_name",
            "email",
        ],
    )

    writer.writeheader()
    writer.writerows(members)

print("Created members.csv")
print("Number of members:", len(members))

# Create ten fictional coaches.
coach_names = [
    "Emma Torres",
    "Liam Carter",
    "Olivia Santos",
    "Noah Kim",
    "Sophia Bennett",
    "Ethan Costa",
    "Mia Thompson",
    "Lucas Martin",
    "Isabella Reed",
    "Daniel Park",
]

coaches = []
coach_number = 1

for coach_name in coach_names:
    coach = {
        "coach_id": coach_number,
        "coach_name": coach_name,
    }

    coaches.append(coach)
    coach_number = coach_number + 1

coaches_file = data_folder / "coaches.csv"

with coaches_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["coach_id", "coach_name"],
    )

    writer.writeheader()
    writer.writerows(coaches)

print("Created coaches.csv")
print("Number of coaches:", len(coaches))

# Create ten simple workout templates.
workouts = [
    {
        "workout_id": 1,
        "workout_name": "Row and Squat",
        "description": "Rowing and air squats",
    },
    {
        "workout_id": 2,
        "workout_name": "Bike and Press",
        "description": "Stationary cycling and dumbbell presses",
    },
    {
        "workout_id": 3,
        "workout_name": "Run and Swing",
        "description": "Running and kettlebell swings",
    },
    {
        "workout_id": 4,
        "workout_name": "Deadlift Practice",
        "description": "Deadlift technique and controlled sets",
    },
    {
        "workout_id": 5,
        "workout_name": "Bodyweight Circuit",
        "description": "Air squats, push-ups, and sit-ups",
    },
    {
        "workout_id": 6,
        "workout_name": "Rowing Intervals",
        "description": "Repeated rowing efforts with rest periods",
    },
    {
        "workout_id": 7,
        "workout_name": "Squat and Carry",
        "description": "Goblet squats and farmer carries",
    },
    {
        "workout_id": 8,
        "workout_name": "Jump and Step",
        "description": "Jump rope and box step-ups",
    },
    {
        "workout_id": 9,
        "workout_name": "Press and Pull",
        "description": "Dumbbell presses and ring rows",
    },
    {
        "workout_id": 10,
        "workout_name": "Mixed Conditioning",
        "description": "Cycling, rowing, and bodyweight movements",
    },
]

workouts_file = data_folder / "workouts.csv"

with workouts_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "workout_id",
            "workout_name",
            "description",
        ],
    )

    writer.writeheader()
    writer.writerows(workouts)

print("Created workouts.csv")
print("Number of workouts:", len(workouts))

# Keep random workout selections the same each time.
random.seed(6301)

# Define the 12-month period.
first_class_date = datetime(2025, 11, 1, 18, 0)
as_of = datetime(2026, 10, 31, 23, 59)

classes = []
class_number = 1
coach_index = 0
current_date = first_class_date

while current_date <= as_of:
    # Monday is 0, Wednesday is 2, and Friday is 4.
    if current_date.weekday() in [0, 2, 4]:
        selected_coach = coaches[coach_index]
        selected_workout = random.choice(workouts)

        gym_class = {
            "class_id": class_number,
            "coach_id": selected_coach["coach_id"],
            "workout_id": selected_workout["workout_id"],
            "start_time": current_date.strftime("%Y-%m-%d %H:%M:%S"),
            "capacity": 8,
            "standard_price": "25.00",
        }

        classes.append(gym_class)
        class_number = class_number + 1

        # Move to the next coach.
        coach_index = coach_index + 1

        # After the last coach, return to the first coach.
        if coach_index == len(coaches):
            coach_index = 0

    current_date = current_date + timedelta(days=1)

classes_file = data_folder / "classes.csv"

with classes_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "class_id",
            "coach_id",
            "workout_id",
            "start_time",
            "capacity",
            "standard_price",
        ],
    )

    writer.writeheader()
    writer.writerows(classes)

print("Created classes.csv")
print("Number of classes:", len(classes))
print("First class:", classes[0]["start_time"])
print("Last class:", classes[-1]["start_time"])

# Keep booking selections repeatable.
random.seed(6302)

# Leave the final member without bookings.
active_members = members[:-1]

bookings = []

for gym_class in classes:
    # Leave classes 1 and 2 without bookings.
    if gym_class["class_id"] not in [1, 2]:
        class_start = datetime.strptime(
            gym_class["start_time"],
            "%Y-%m-%d %H:%M:%S",
        )

        # Most classes have seven reservations and one cancellation.
        number_of_bookings = 8

        # These two classes deliberately exceed capacity.
        if gym_class["class_id"] in [3, 4]:
            number_of_bookings = 9

        selected_members = random.sample(
            active_members,
            number_of_bookings,
        )

        booking_position = 1

        for member in selected_members:
            status = random.choice(
                ["Attended", "Attended", "Attended", "No-show"]
            )
            agreed_charge = "25.00"

            # The eighth booking is cancelled in ordinary classes.
            if number_of_bookings == 8 and booking_position == 8:
                status = "Cancelled"
                agreed_charge = "0.00"

            days_before = random.randint(1, 2)
            booked_at = class_start - timedelta(days=days_before)

            # Deliberately create exactly two late bookings.
            if gym_class["class_id"] == 5:
                if booking_position in [1, 2]:
                    booked_at = class_start + timedelta(minutes=15)

            booking = {
                "member_id": member["member_id"],
                "class_id": gym_class["class_id"],
                "booked_at": booked_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "status": status,
                "agreed_charge": agreed_charge,
            }

            bookings.append(booking)
            booking_position = booking_position + 1

bookings_file = data_folder / "bookings.csv"

with bookings_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "member_id",
            "class_id",
            "booked_at",
            "status",
            "agreed_charge",
        ],
    )

    writer.writeheader()
    writer.writerows(bookings)

print("Created bookings.csv")
print("Number of bookings:", len(bookings))
print("Total activity rows:", len(classes) + len(bookings))

# Prepare counters for every member and class.
member_booking_counts = {}
class_booking_counts = {}
class_reserved_counts = {}
class_start_times = {}

for member in members:
    member_booking_counts[member["member_id"]] = 0

for gym_class in classes:
    class_id = gym_class["class_id"]

    class_booking_counts[class_id] = 0
    class_reserved_counts[class_id] = 0

    class_start_times[class_id] = datetime.strptime(
        gym_class["start_time"],
        "%Y-%m-%d %H:%M:%S",
    )

# Count bookings and identify late booking records.
late_booking_count = 0

for booking in bookings:
    member_id = booking["member_id"]
    class_id = booking["class_id"]

    member_booking_counts[member_id] += 1
    class_booking_counts[class_id] += 1

    if booking["status"] != "Cancelled":
        class_reserved_counts[class_id] += 1

    booking_time = datetime.strptime(
        booking["booked_at"],
        "%Y-%m-%d %H:%M:%S",
    )

    if booking_time > class_start_times[class_id]:
        late_booking_count += 1

# Find members and classes without bookings.
members_without_bookings = []

for member_id in member_booking_counts:
    if member_booking_counts[member_id] == 0:
        members_without_bookings.append(member_id)

classes_without_bookings = []
over_capacity_classes = []

for gym_class in classes:
    class_id = gym_class["class_id"]

    if class_booking_counts[class_id] == 0:
        classes_without_bookings.append(class_id)

    if class_reserved_counts[class_id] > gym_class["capacity"]:
        over_capacity_classes.append(class_id)

print()
print("DATA CHECKS")
print("Members without bookings:", members_without_bookings)
print("Classes without bookings:", classes_without_bookings)
print("Over-capacity classes:", over_capacity_classes)
print("Late booking records:", late_booking_count)

# Stop with an error if an expected result is wrong.
assert members_without_bookings == [10]
assert classes_without_bookings == [1, 2]
assert over_capacity_classes == [3, 4]
assert late_booking_count == 2

print("All four checks passed.")