from datetime import datetime
from housing import models as housing_models
from employee import models as emp_models

def update_emp_info(employee, hostel_id):
    if hostel_id:
        employee.emp_info = hostel_id
        employee.save()

def deactivate_role(emp_hostel_alloc):
    emp_hostel_alloc.active = False
    emp_hostel_alloc.role_end_date = datetime.now()
    # emp_hostel_alloc.save() 

def assign_new_role(hostel, employee, added_by, role):
    new_role = housing_models.HostelEmployeeAlloc(
        hostel = hostel,
        hostel_code = hostel.hostel_id,
        employee = employee,
        employee_code = employee.employee_id,
        role = role,
        timestamp = datetime.now(),
        role_end_date = None,
        added_by = added_by,
        active = True,
        comment = ""
    )
    new_role.save()
        