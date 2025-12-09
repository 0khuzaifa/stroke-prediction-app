from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required
from .extensions import db
from .models import Patient
from .ml import predict_risk

bp = Blueprint("patients", __name__)


def parse_int(name, value, allowed=None):
    try:
        v = int(value)
    except Exception:
        abort(400)
    if allowed is not None and v not in allowed:
        abort(400)
    return v


def parse_float(name, value, allow_null=False):
    if allow_null and (value is None or value == ""):
        return None
    try:
        return float(value)
    except Exception:
        abort(400)


@bp.route("/")
@login_required
def list_patients():
    page = request.args.get("page", 1, type=int)
    per_page = 20
    pagination = Patient.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("patients/list.html", pagination=pagination, patients=pagination.items)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_patient():
    if request.method == "POST":
        patient_id = parse_int("patient_id", request.form.get("patient_id"))
        gender = request.form.get("gender", "").strip()
        age = parse_float("age", request.form.get("age"))
        hypertension = parse_int("hypertension", request.form.get("hypertension"), allowed={0, 1})
        ever_married = request.form.get("ever_married", "").strip()
        work_type = request.form.get("work_type", "").strip()
        residence_type = request.form.get("residence_type", "").strip()
        avg_glucose_level = parse_float("avg_glucose_level", request.form.get("avg_glucose_level"))
        bmi = parse_float("bmi", request.form.get("bmi"), allow_null=True)
        smoking_status = request.form.get("smoking_status", "").strip()
        stroke = parse_int("stroke", request.form.get("stroke"), allowed={0, 1})
        if Patient.query.filter_by(patient_id=patient_id).first():
            return render_template("patients/form.html", error="Duplicate patient_id", patient=None)
        p = Patient(
            patient_id=patient_id,
            gender=gender,
            age=age,
            hypertension=hypertension,
            ever_married=ever_married,
            work_type=work_type,
            residence_type=residence_type,
            avg_glucose_level=avg_glucose_level,
            bmi=bmi,
            smoking_status=smoking_status,
            stroke=stroke,
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("patients.list_patients"))
    return render_template("patients/form.html", patient=None)


@bp.route("/<int:id>")
@login_required
def view_patient(id):
    p = Patient.query.get_or_404(id)
    return render_template("patients/view.html", patient=p, risk=None)


@bp.route("/<int:id>/predict", methods=["POST"])
@login_required
def predict_patient(id):
    p = Patient.query.get_or_404(id)
    data = {
        "age": p.age,
        "avg_glucose_level": p.avg_glucose_level,
        "bmi": p.bmi or 0.0,
        "hypertension": p.hypertension,
        "stroke": p.stroke,
    }
    score = predict_risk(data)
    return render_template("patients/view.html", patient=p, risk=score)


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(id):
    p = Patient.query.get_or_404(id)
    if request.method == "POST":
        p.gender = request.form.get("gender", "").strip()
        p.age = parse_float("age", request.form.get("age"))
        p.hypertension = parse_int("hypertension", request.form.get("hypertension"), allowed={0, 1})
        p.ever_married = request.form.get("ever_married", "").strip()
        p.work_type = request.form.get("work_type", "").strip()
        p.residence_type = request.form.get("residence_type", "").strip()
        p.avg_glucose_level = parse_float("avg_glucose_level", request.form.get("avg_glucose_level"))
        p.bmi = parse_float("bmi", request.form.get("bmi"), allow_null=True)
        p.smoking_status = request.form.get("smoking_status", "").strip()
        p.stroke = parse_int("stroke", request.form.get("stroke"), allowed={0, 1})
        db.session.commit()
        return redirect(url_for("patients.view_patient", id=p.id))
    return render_template("patients/form.html", patient=p)


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_patient(id):
    p = Patient.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for("patients.list_patients"))
