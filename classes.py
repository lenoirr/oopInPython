from datetime import date
from dataclasses import dataclass



# ---------------------------------------------DATA CLASS--------------------------------------------------------------------------------

#

@dataclass      # this structure automatically create the __intit__, and __repr__
class Project:  # can do this if you want to add slots!
    __slots__ = ["name", "payment","client"]
    name: str    # called type hinting which is a good idea
    payment: str
    client: str

    def notify_client(self):    # you can even write methods!
        print(f"Notifying the client about the progress of the {self.name}.....")
# ----------------------------------------------------------------------------------------------------------------------------------------


# class Project:
#     def __init__(self,name, payment, client):
#         self.name = name
#         self.payment = payment
#         self.client = client


class Employee:
    
    __slots__ = ("name","age","position","_salary","_annual_salary", "project") # SLOTS: optional feature to optimize memory allocation for new class instances (really important with alot of instances)
    # provides instances with faster attribute access

    @classmethod
    def new_employee(cls, name, dob, pos, project):     # alternative constructor
        now = date.today()
        age = now.year - dob.year - ((now.month,now.day) < (dob.month, dob.day))
        return cls(name,age,pos,cls.minimum_wage,project)   #instantiates a new employee instance and returns it

    @classmethod        # for methods that do not do work on an instances of the class(static in C#)
    def change_minimum_wage(cls,new_wage):      # first parameter is the class itself cls is short for class
        if new_wage > 3000:
            raise ValueError("Company can't afford that")
        else:
            cls.minimum_wage = new_wage # using cls instead of Employee to keep dynamic

    minimum_wage = 1000 # static Variables across all instances of the class, found with Employee.minimum_wage or through an instance

    def __init__ (self, name, age, position, salary, project):    # self is the new empty object passed for the __new__ function that is called on the creation of an object of this class
        self.name = name
        self.age = age
        self.position = position
        self._salary = salary    # I wish :(
        self._annual_salary = None
        self.project = project
        
    def __str__ (self):     # This function is called when print(class instance)
        return f"\nEMPLOYEE DETAILS:{self.name} is {self.age} year old. Employee is a {self.position} with the salary of ${self._salary} and is working on {self.project}\n"
    
    def __repr__ (self):    # code used to return a string to create another instance - mine isn't working cuz I lazy
        return f"Employee({self.name},{self.age}, {self.position}, {self._salary})"
    
    # ----------------------------------------------------------------------------------------PROPERTIES FOR INPUT AND OUTPUT VALIDATION AND SECURITY ---------------------------------------------------------------------#
    # Allows ability to program write validation and read trandformation. Also allows read only and write only variables - not shown here tho (look that shit up cuh)

    @property           # Property Decorator - GETTER FUNCTION makes this method act like a property (removes the need for () when calling)
    def salary(self):
        return self._salary
    
    @salary.setter      # decorator references the method from getter(salary) and . setter (requires the getter)
    def salary(self,salary): 
        if salary < Employee.minimum_wage:
            raise ValueError('Minimum wage is 1000')
        self._annual_salary = None          # Forces recalculation of aFnnual salary when called next after changed salary 
        self._salary = salary

    @property           # this is a computed property: only does computation when called (can save processing)
    def annual_salary(self):    
        if self._annual_salary is None:     # "Cashing" - save computation be avoiding recalculation when not required
            self._annual_salary =  self._salary * 12
        return self._annual_salary
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def increase_salary(self,percent):
        self._salary += self._salary * (percent/100)

class SlotsInspectorMixin:  # mix in class used to be mixin into another last kinda like inheritance. 
    __slots__ = ()
    def has_slots(self):
        return hasattr(self,"__slots__")    # checks if this instance of the class uses slots
    
class Tester(Employee): # inherited class

    def run_tests(self):
        print(f"Testing is started by {self.name}")
        print("Tests are done.")

class Developer(SlotsInspectorMixin, Employee): # order here matters with inheritance hierarchy
    __slots__ = ("framework")
    def __init__(self,name,age, position, salary, project, framework): # adding additional attribute to child class
        super().__init__(name,age,position,salary, project)   # calls method from parent class
        self.framework = framework

    def increase_salary(self, percent, bonus):
        super().increase_salary(percent)
        self.salary += bonus 

    def test_def (val):
        print(val)

employee1_project = Project("Misinformation Media", "Propaganda", "U.S. Government")
employee1 = Developer("Ryan Lenoir", 22, "Engineer", 120000, employee1_project,"Flask")
employee2 = Tester("Gage Elenbass",69,"Engineer", 10000, employee1_project)

print("Hello World!")

#print(employee1)
#print(employee1.__repr__())
#print(employee2.salary)
#employee2.increase_salary(20)
#print(employee2.salary)
#employee2.run_tests()

#print(employee1)
#print(employee1.__dict__)      # should return an error if this instance is only relying on slots
#print(employee1.has_slots())
#print(Developer.__mro__)# returns the method resoltuion order (order in which methods will be searched for inside this inheritence tree)


# MMLLC FUNCTIONALITY THAT IS WEIRD TO ME
#Developer.test_def(3)   # not performing work on an instance of the class at all - which I guess is fine for grouping of function in some cases?
#Employee.change_minimum_wage(2000)
#print (Employee.minimum_wage)

# e = Employee.new_employee("Mary",date(1991,8,12), "Engineer")
# print(e.name)
# print(e.age)
# print(e.salary)

print(employee1_project.__repr__)

