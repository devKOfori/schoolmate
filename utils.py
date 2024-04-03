from datetime import datetime

def update_emp_info(employee, hostel_id):
    if hostel_id:
        employee.emp_info = hostel_id
        employee.save()

def deactivate_role(emp_hostel_alloc):
    emp_hostel_alloc.active = False
    emp_hostel_alloc.role_end_date = datetime.now()
    emp_hostel_alloc.save() 