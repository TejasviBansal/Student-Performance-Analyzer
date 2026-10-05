def averageCalculator(lis, no_of_students):
    if no_of_students == 0:
        return 0.0
    
    total=0
    for i in lis:
        total +=i

    return round(total/no_of_students, 2)

def grade(marks, assignment_score):
    composite_score = round((marks*0.7)+(assignment_score*0.3), 2)

    if composite_score >= 85:
        grade = 'A'
    elif composite_score >= 70:
        grade = 'B'
    elif composite_score >= 55:
        grade = 'C'
    elif composite_score >= 40:
        grade = 'D'
    else:
        grade = 'E'

    return grade

def status(marks, attendance):
    if marks >= 40 and attendance >= 75:
        return "Pass"
    else:
        return "Fail"

def studentReport(student_data, no_of_students):

    print("-"*60)
    print("STUDENT REPORT")    
    print("-"*60)
    
    print("-"*20 + "Summary Statistics" + "-"*20)

    print("Total enrolled students: ", no_of_students)
    print("Average exam marks: ", averageCalculator(student_data["marks"], no_of_students))
    print("Average assignment: ", averageCalculator(student_data["assignment_score"], no_of_students))
    print("Average attendance: ", averageCalculator(student_data["attendance"], no_of_students))

    print("-"*20 + "Student Status & Grades" + "-"*20)
    print(f"{'Name':<12} | {'Marks':<8} | {'Attend%':<10} | {'Assign':<8} | {'Grade':<8} | {'Status':<10}")
    print("-" * 75)
    for i in range(no_of_students):
        print(
            f"{student_data['names'][i]:<12} | "
            f"{student_data['marks'][i]:<8} | "
            f"{student_data['attendance'][i]:<10} | "
            f"{student_data['assignment_score'][i]:<8} | "
            f"{grade(student_data['marks'][i], student_data['assignment_score'][i]):<8} | "
            f"{status(student_data['marks'][i], student_data['attendance'][i]):<10}"
        )

    print("-"*20 + "Top Performers" + "-"*20)

    top_score = -1
    top_students = []
    for i in range(no_of_students):
        composite_score = round((student_data['marks'][i] * 0.7) + (student_data['assignment_score'][i] * 0.3), 2)

        if composite_score > top_score:
            top_score = composite_score
            top_students = [student_data['names'][i]]

        elif composite_score == top_score:
            top_students.append(student_data['names'][i])

    for student in top_students:
        print(student)

    

def studentDetails():
    student_data = {
        "names":[],
        "marks":[],
        "attendance":[],
        "assignment_score":[]
    }

    print("-"*60)
    print("ENTER STUDENT DETAILS")
    print("-"*60)

    no_of_students = int(input("Enter number of students: "))

    for i in range(no_of_students):
        student_data["names"].append(input("Enter the student name: ").strip())
        student_data["marks"].append(float(input("Enter the student marks: ")))
        student_data["attendance"].append(float(input("Enter the student attendance: ")))
        student_data["assignment_score"].append(float(input("Enter the student assignment score: ")))

    studentReport(student_data, no_of_students)

if __name__ == "__main__":
    studentDetails()