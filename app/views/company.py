from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required

from app.models import Company
from app.forms import CompanyCreationForm, CompanyForm

company_blueprint = Blueprint("company", __name__)


@company_blueprint.route("/companies")
@login_required
def companies():
    companies = Company.query.all()
    return render_template("/company/companies.html", companies=companies)


@company_blueprint.route("/company/<int:id>", methods=["GET", "POST"])
@login_required
def company_profile(id):
    company: Company = Company.query.get(id)
    form = CompanyForm()
    if form.validate_on_submit():
        company.title = form.title.data,
        company.location = form.location.data,
        company.save()

        flash("Company has been successfully updated", "info")
        return redirect(url_for("company.companies"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    elif request.method == "GET":
        form.title.data = company.title
        form.location.data = company.location
    return render_template("company/company_creation_profile.html", form=form, company_id=company.id)


@company_blueprint.route("/company/creation", methods=["GET", "POST"])
@login_required
def company_creation():
    form = CompanyCreationForm()
    if form.validate_on_submit():
        company = Company(
            title=form.title.data,
            location=form.location.data,
        )
        company.save()
        flash("Creation successful. The new company is created.", "success")
        return redirect(url_for("company.companies"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("company/company_creation_profile.html", form=form)


@company_blueprint.route("/company/deletion/<int:id>")
@login_required
def company_deletion(id):
    company: Company = Company.query.get(id)
    company.delete()
    return redirect(url_for('company.companies'))
