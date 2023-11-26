<?php
// Prepare our SQL, preparing the SQL statement will prevent SQL injection.
if (
    $stmt = $con->prepare('select course.courseId, 
                                  course.name, 
                                  course.description,
                                  course.startDate,
                                  course.endDate,
                                  course.startTime, 
                                  course.endTime,  
                                  course.location,
                                  course.prefix,
                                  course.daysOfWeek,
                                  professor.userId,
                                  professor.firstName,
                                  professor.lastName,
                                  user.userEmail,
                                  professor.phone
                            from course 
                              inner join student_course on student_course.courseId = course.courseId
                              inner join student on student.userId = student_course.userId
                              inner join professor_course on professor_course.courseId = course.courseId
                              inner join professor on professor_course.userId = professor.userId 
                              inner join user on professor.userId = user.userId
                            where student.userId = ?')
) {
    $stmt->bind_param('s', $_SESSION['id']);

    if ($stmt->execute()) {
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            $rows = $result->fetch_all(MYSQLI_ASSOC);
            $todayCourse_array = array();

            // Get the current day of the week (e.g., "Monday")
            $currentDay = date('l');
            $currentDate = date('Y-m-d');

            foreach ($rows as $row) {
                // Check if the current day is in the daysOfWeek string
                // and if the current date is within the range of startDate and endDate
                if (
                    strpos($row['daysOfWeek'], $currentDay) !== false &&
                    ($currentDate >= $row['startDate'] && $currentDate <= $row['endDate'])
                ) {
                    $todayCourse_array[] = $row;
                }
            }
        }
    } else {
        echo 'Error executing the query: ' . $stmt->error;
    }

    $stmt->close();
} else {
    echo 'Error preparing the statement: ' . $con->error;
}
?>