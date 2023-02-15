from flask import render_template, Blueprint, flash, request, redirect, url_for
from flask_login import login_required
from app.forms import AddEmployeeForm, EmployeeForm
from app.models import Employee, Company

employee_blueprint = Blueprint("employee", __name__)


@employee_blueprint.route("/employees", methods=["GET"])
@login_required
def employees():
    employees = Employee.query.all()
    return render_template("employee/employees.html", employees=employees)

@employee_blueprint.route("/employee/creation", methods=["GET", "POST"])
@login_required
def employee_creation():
    form = AddEmployeeForm()
    if form.validate_on_submit():
        employee = Employee(
            name=form.name.data,
            position=form.position.data,
            phone=form.phone.data,
            email=form.email.data,
            birthday=form.birthday.data,
            company_id=int(form.company_id.data.id),
        )
        employee.save()
        flash("Employee has been successfully added", "info")
        return redirect(url_for("employee.employees"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("employee/employee_creation_profile.html", form=form)

@employee_blueprint.route("/employee/deletion/<int:id>")
@login_required
def employee_deletion(id):
    employee_to_delete: Employee = Employee.query.get(id)
    employee_to_delete.delete()
    return redirect(url_for("employee.employees"))

@employee_blueprint.route("/employee/<int:id>", methods=["GET", "POST"])
@login_required
def employee_profile(id):
    employee: Employee = Employee.query.get(id)
    form = EmployeeForm()
    if form.validate_on_submit():
        employee.name = (form.name.data,)
        employee.position = (form.position.data,)
        employee.phone = (form.phone.data,)
        employee.email = (form.email.data,)
        employee.birthday = (form.birthday.data,)
        employee.company = (form.company_id.data,)
        employee.save()
        flash("Employee successfully updated", "info")
        return redirect(url_for("employee.employees"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    elif request.method == "GET":
        form.name.data = employee.name
        form.position.data = employee.position
        form.phone.data = employee.phone
        form.email.data = employee.email
        form.birthday.data = employee.birthday
        form.company_id.data = Company.query.filter_by(id=employee.company_id).first()
    return render_template("employee/employee_creation_profile.html", employee_id=employee.id, form=form)

@employee_blueprint.route("/company/<int:id>/employees", methods=["GET", "POST"])
@login_required
def company_employees(id):
    company_employees = Employee.query.filter_by(company_id=id)
    company = Company.query.get(id)
    return render_template("employee/employees.html", employees=company_employees, company=company)
