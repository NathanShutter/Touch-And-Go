<?php

session_start();

if (!isset($_SESSION['loggedin']) || $_SESSION['userType'] != 'admin') {
    include 'logout.php';
    exit();
}

require 'db_connection.php';

// Get user's name based on what account type they are, as well as userId

switch (true) {
    case $_SESSION['userType'] == 'student':
        // Prepare our SQL, preparing the SQL statement will prevent SQL injection.
        if ($stmt = $con->prepare('SELECT userId FROM user WHERE userEmail = ?')) {
            $stmt->bind_param('s', $_SESSION['email']);
            $stmt->execute();
            $stmt->store_result();
            if ($stmt->num_rows > 0) {
                $stmt->bind_result($_SESSION['userId']);
                $stmt->fetch();
            }
            $stmt->close();
        }

        if ($stmt = $con->prepare('SELECT firstName, lastName FROM student WHERE userId = ?')) {
            $stmt->bind_param('i', $_SESSION['userId']);
            $stmt->execute();
            $stmt->store_result();
            if ($stmt->num_rows > 0) {
                $stmt->bind_result($_SESSION['firstName'], $_SESSION['lastName']);
                $stmt->fetch();
            }
            $stmt->close();
        }
        break;

    case $_SESSION['userType'] == 'professor':
        // Prepare our SQL, preparing the SQL statement will prevent SQL injection.
        if ($stmt = $con->prepare('SELECT userId FROM user WHERE userEmail = ?')) {
            $stmt->bind_param('s', $_SESSION['email']);
            $stmt->execute();
            $stmt->store_result();
            if ($stmt->num_rows > 0) {
                $stmt->bind_result($_SESSION['userId']);
                $stmt->fetch();
            }
            $stmt->close();
        }

        if ($stmt = $con->prepare('SELECT firstName, lastName FROM professor WHERE userId = ?')) {
            $stmt->bind_param('i', $_SESSION['userId']);
            $stmt->execute();
            $stmt->store_result();
            if ($stmt->num_rows > 0) {
                $stmt->bind_result($_SESSION['firstName'], $_SESSION['lastName']);
                $stmt->fetch();
            }
            $stmt->close();
        }

        break;

    case $_SESSION['userType'] == 'admin':
        // Prepare our SQL, preparing the SQL statement will prevent SQL injection.
        if ($stmt = $con->prepare('SELECT userId FROM user WHERE userEmail = ?')) {
            $stmt->bind_param('s', $_SESSION['email']);
            $stmt->execute();
            $stmt->store_result();
            if ($stmt->num_rows > 0) {
                $stmt->bind_result($_SESSION['userId']);
                $stmt->fetch();
            }
            $stmt->close();
        }

        if ($stmt = $con->prepare('SELECT firstName, lastName FROM admin WHERE userId = ?')) {
            $stmt->bind_param('i', $_SESSION['userId']);
            $stmt->execute();
            $stmt->store_result();
            if ($stmt->num_rows > 0) {
                $stmt->bind_result($_SESSION['firstName'], $_SESSION['lastName']);
                $stmt->fetch();
            }
            $stmt->close();
        }

        break;
    default:
        include 'logout.php';
        break;
}

?>
<!DOCTYPE html>

<html lang="en"> <!-- start of html tag -->

<head> <!-- start of head tag -->
    <!-- set charset -->
    <meta charset="utf-8">
    <!-- set title -->
    <title>Courses</title>
    <!-- link external style.css sheet -->
    <link rel="stylesheet" type="text/css" href="../styles.css">

    <!-- start of style tag -->
    <style>
        /* start of style rules for h3 tag */
        h3 {
            color: #10222E;
            /* make color blue */
            font-size: 24pt;
            /* make font size 24 pt */
            text-align: center;
            /* center align text */
            margin-top: 5%;
            /* make margin-top 5% */
        }

        #fakeNav a:hover {
            background-color: #0f222e;
        }

        form.create_course {
            max-width: 800px;
            margin: auto;
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }

        form.create_course label {
            display: block;
            margin-top: 10px;
        }

        form.create_course fieldset {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
        }

        form.create_course legend {
            font-weight: bold;
        }

        form.create_course input[type="text"],
        form.create_course input[type="checkbox"],
        form.create_course input[type="time"],
        form.create_course input[type="date"] {
            width: auto;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-top: 5px;
            box-sizing: border-box;
        }

        form.create_course input[type="text"],
        form.create_course input[type="time"],
        form.create_course input[type="date"] {
            width: 50%;
        }

        form.create_course input[type="submit"],
        form.create_course input[type="reset"] {
            width: 100%;
            padding: 15px 0;
            font-size: 18px;
            border: 0;
            color: #fff;
            cursor: pointer;
            border-radius: 5px;
            transition: background 0.3s ease-in-out;
            margin-top: 20px;
        }

        form.create_course input[type="submit"] {
            background: #4CAF50;
        }

        form.create_course input[type="submit"]:hover {
            background: #397d13;
        }

        form.create_course input[type="reset"] {
            background: #FF6347;
        }

        form.create_course input[type="reset"]:hover {
            background: #8b0000;
        }
    </style> <!-- end of style tag -->

<body> <!-- start of body tag -->

    <!-- The following code was created on October 30, 2023, using 
    information from the following link:
    https://www.w3schools.com/css/css_navbar_horizontal.asp -->

    <ul> <!-- start of ul for menu bar -->
        <!-- list home.php link -->
        <li><a class="link" href="adminHome.php">Home</a></li>
        <!-- list schedule.php link -->
        <li><a class="link" href="#">Courses</a></li>
        <!-- list analytics.php link -->
        <li id="fakeNav"><a></a></li>
        <!-- list Touch & Go logo -->
        <li><img src="../newLogo.png" alt="Touch and Go Logo" height="60"></li>
        <!-- list contact.php link -->
        <li id="fakeNav"><a></a></li>
        <!-- list help.php link -->
        <li id="fakeNav"><a></a></li>
        <!-- list logout.php link -->
        <li><a class='link' href="logout.php">Logout</a></li>
    </ul> <!-- end of ul for menu bar -->

    <!-- this ends the code that was created using information from the 
    following link:
    https://www.w3schools.com/css/css_navbar_horizontal.asp -->

    <!-- home header -->
    <h1>Courses</h1>

    <h3 class="center">Create Course</h3>
    <form class="create_course" method="post" action="addCourse.php">
        <label for="prefix">Course Prefix:</label>
        <input type="text" maxlength="6" name="prefix" required>

        <label for="name">Course Name:</label>
        <input type="text" name="name" required>

        <label for="description">Description</label>
        <input type="text" name="description">

        <label for="location">Location:</label>
        <input type="text" maxlength="5" name="location" required>

        <label for="startDate">Start Date</label>
        <input type="date" name="startDate" value="2023-08-28">

        <label for="endDate">End Date</label>
        <input type="date" name="endDate" value="2023-12-16">

        <fieldset>
            <legend>Days of the Week:</legend>
            <input type="checkbox" name="daysOfWeek[]" value="Monday"> Monday
            <input type="checkbox" name="daysOfWeek[]" value="Tuesday"> Tuesday
            <input type="checkbox" name="daysOfWeek[]" value="Wednesday"> Wednesday
            <input type="checkbox" name="daysOfWeek[]" value="Thursday"> Thursday
            <input type="checkbox" name="daysOfWeek[]" value="Friday"> Friday
            <input type="checkbox" name="daysOfWeek[]" value="Saturday"> Saturday
            <input type="checkbox" name="daysOfWeek[]" value="Sunday"> Sunday
        </fieldset>

        <label for="startTime">Start Time:</label>
        <input type="time" name="startTime" placeholder="HH:MM AM/PM" required>

        <label for="endTime">End Time:</label>
        <input type="time" name="endTime" placeholder="HH:MM AM/PM" required>

        <input type="submit" value="Create Course">
        <input type="reset" value="Clear">
    </form>

    <h3 class="center">Edit Courses</h3>

    <h3 class="center">Edit students in course</h3>

    <h3 class="center">Edit Professor in course</h3>

</body>

</html>