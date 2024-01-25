from rolepermissions.roles import AbstractUserRole

class Instructor(AbstractUserRole):
    available_permissions = {
        'create_medical_course': True,
    }

class Student(AbstractUserRole):
    available_permissions = {
        'edit_patient_file': True,
    }