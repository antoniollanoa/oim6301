# CrossFit Gym Class Bookings and Attendance

## 1. The Scenario

I chose Option E: Your Own Domain.

This project represents a fictional CrossFit gym that currently records members, coaches, workouts, scheduled classes, and bookings in spreadsheets.

The gym owner and front-desk staff need an organized way to see who booked each class, record attendance, identify classes with no bookings, and check whether bookings exceed class capacity.

To keep the project simple, the gym charges per class. Monthly memberships, payments, workout scores, and online booking are outside the scope.

### What the gym records today

- Members: a membership number, name, and email address.
- Coaches: a coach identifier and name.
- Workouts: a workout identifier, name, and short description.
- Classes: a class identifier, coach, workout, start date and time, capacity, and standard price.
- Bookings: the member, class, booking date, booking status, and agreed charge.

### Business rules

1. Each member has a unique membership number. Each member can have zero or more bookings.
2. Each class has exactly one coach and one workout. A coach can teach many classes, and a workout can be used in many classes.
3. Each booking belongs to exactly one member and one class.
4. A member can have only one booking record for a particular class. If the booking changes, that record is updated.
5. Each class must have a capacity greater than zero.
6. Class prices and booking charges cannot be negative.
7. Booking status must be Booked, Attended, No-show, or Cancelled. New bookings default to Booked.
8. A cancelled booking has a charge of zero and does not count toward class capacity.
9. Booked, Attended, and No-show bookings count as places reserved for the class. Their combined count must not exceed class capacity.
10. A booking must be made no later than the class start time.
11. A class can have no bookings. Attendance is recorded by changing an existing booking's status, rather than creating a separate attendance record.

### Eight business questions

1. How many bookings does each class have, including classes with no bookings?
2. Which members have never booked a class?
3. Which class start hours have the most attended bookings?
4. For each coach, how many attended bookings and how much revenue from attended bookings are associated with their classes? This question uses Coaches, Classes, and Bookings.
5. For each workout, how many attended bookings and how much revenue from attended bookings are associated with its classes? This question uses Workouts, Classes, and Bookings.
6. Which members have the most no-shows?
7. Which booking records were created after their class started? (checks a rule)
8. Which classes have more non-cancelled bookings than their capacity? (checks a rule)

For revenue questions, revenue means the sum of agreed charges for bookings marked Attended.

## 2. The ERD

```mermaid
erDiagram
    MEMBERS ||--o{ BOOKINGS : makes
    CLASSES ||--o{ BOOKINGS : receives
    COACHES ||--o{ CLASSES : teaches
    WORKOUTS ||--o{ CLASSES : uses

    MEMBERS {
        INTEGER member_id PK
        VARCHAR membership_number UK
        VARCHAR member_name
        VARCHAR email
    }

    COACHES {
        INTEGER coach_id PK
        VARCHAR coach_name
    }

    WORKOUTS {
        INTEGER workout_id PK
        VARCHAR workout_name
        VARCHAR description
    }

    CLASSES {
        INTEGER class_id PK
        INTEGER coach_id FK
        INTEGER workout_id FK
        TIMESTAMP start_time
        INTEGER capacity
        DECIMAL standard_price
    }

    BOOKINGS {
        INTEGER member_id PK, FK
        INTEGER class_id PK, FK
        TIMESTAMP booked_at
        VARCHAR status
        DECIMAL agreed_charge
    }
```

## 3. What One Row Means

- **Members:** One row represents one person registered with the gym.
- **Coaches:** One row represents one coach who can teach classes.
- **Workouts:** One row represents one reusable workout template.
- **Classes:** One row represents one scheduled class taught by one coach and using one workout.
- **Bookings:** One row represents one member's reservation for one class, including its current attendance or cancellation status.

## 4. Design Choices

### 1. Choosing the member key

I chose an invented `member_id` as the primary key instead of the gym’s membership number. This keeps the links between tables stable if the gym changes its membership numbering system. The membership number is still unique, so two members cannot share it.

### 2. Optional relationships

A member can have no bookings because someone may register before booking their first class. A class can also have no bookings because staff may schedule it before anyone reserves a place. Keeping these records helps the gym identify members who have not participated and classes with no bookings.

### 3. Rules that require other rows

Class capacity cannot be checked using one booking row alone. We must count all non-cancelled bookings for the class and compare that count with the class’s capacity. We must also compare each booking’s date and time with the start time stored in its class record. These rules require queries because a simple constraint on one booking row cannot check them.

### 4. Something I checked in the design

I checked the two-column primary key in Bookings using a small example. Member 1 can book classes 101 and 102, and member 2 can also book class 101. However, member 1 cannot have a second booking for class 101. This matches the rule that each member can have only one booking record per class.
