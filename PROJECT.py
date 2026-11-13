import json 
from abc import ABC,abstractmethod
from pathlib import Path

database ="school_data.json"
data={"Students":[],"Teachers":[]}

if Path(database).exists():
    with open(database,"r") as f:
        content=f.read()
        if content:
            data=json.loads(content)

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)


class Persons(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email:
            return True
        else:
            return False

class Student(Persons):

    def get_roles(self):
        return "Student"

    def register(self):
        name=input("Enter Your Name:")
        age=int(input("Enter Your Age:"))
        email=input("Enter Your Email:")
        roll_no=int(input("Enter Your Roll Number:"))

        if not Persons.validate_email(email):
            print("Invalid Email")
            return

        for i in data["Students"]:
            if i["roll_no"]==roll_no:
                print("Student Already Exists!")
                return

        data["Students"].append({
            "name":name,
            "age":age,
            "email":email,
            "roll_no":roll_no,
            "grades":{}
        })

        save()
        print(f"Student Name Registered")

    
    def show_details(self):
        roll_no =int(input("Enter Your Roll Number:"))
        for s in data["Students"]:
            if s["roll_no"]==roll_no:
                grades=s["grades"]
                avg=sum(grades.values())/len(grades) if grades else 0

                print(f"Name: {s["name"]}")
                print(f"Roll Number: {s["roll_no"]}")
                print(f"Grades: {s["grades"]}")
                print(f"Average: {avg:1f}")
                return


    def add_grades(self):
        roll_no =int(input("Tell The Roll Number in which you want to Add Grades:"))
        subject=input("Enter The Subject Name:")
        marks=int(input("Enter The Obtained Marks:"))

        for i in data["Students"]:
            if i["roll_no"] == roll_no:
                i["grades"][subject]=marks
                save()
                print(f"Grades Added Successfully")
                return
        print(f"Student Not Found:(")


class Teacher(Persons):

    def get_roles(self):
        return "Teachers"

    def register(self):
        name=input("Enter Your Name:")
        age=int(input("Enter Your Age:"))
        email=input("Enter Your Email:")
        subject=input("Enter Your Subject:")
        employee_id=int(input("Enter Your Employee_ID Number:"))
    
        if not Persons.validate_email(email):
            print("Invalid Email")
            return
    
        for i in data["Teachers"]:
            if i["employee_id"]==employee_id:
                print("Student Already Exists!")
                return
    
        data["Teachers"].append({
            "name":name,
            "age":age,
            "email":email,
            "employee_id":employee_id,
            "subject":subject
        })

        save()
        print(f"Teacher Name Registered")
            
    def show_details(self):
        employee_id =int(input("Enter Your Employee ID:"))
        for t in data["Teachers"]:
            if t["employee_id"]==employee_id:

                print(f"Name: {t["name"]}")
                print(f"Employee Id: {t["employee_id"]}")
                print(f"Subject: {t["subject"]}")
                return
            print(f"Teacher Not Found")
    


stud=Student()
teach=Teacher()

print(f"Press 1 to Register a Student")
print(f"Press 2 to Register a Teacher")
print(f"Press 3 to Add Students Grades")
print(f"Press 4 to Students Details")
print(f"Press 5 to Teachers Details")

choice=int(input("Enter Your Choice:"))

if choice==1:
    stud.register()

elif choice==2:
    teach.register()

elif choice==3:
    stud.add_grades()

elif choice==4:
    stud.show_details()

elif choice==5:
    teach.show_details()

