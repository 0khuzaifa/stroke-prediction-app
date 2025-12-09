from app.extensions import db
from app.models import Patient


def login(client):
    client.post("/auth/register", data={"username": "u", "email": "u@e.com", "password": "p"})
    client.post("/auth/login", data={"username": "u", "password": "p"})


def test_crud_flow(client):
    login(client)
    r = client.post("/patients/create", data={
        "patient_id": "1",
        "gender": "Male",
        "age": "60",
        "hypertension": "0",
        "ever_married": "Yes",
        "work_type": "Private",
        "residence_type": "Urban",
        "avg_glucose_level": "100.5",
        "bmi": "30.1",
        "smoking_status": "never smoked",
        "stroke": "0",
    }, follow_redirects=True)
    assert r.status_code == 200
    assert b"Patients" in r.data

    r = client.get("/patients/")
    assert b"Male" in r.data

    from flask import current_app
    with client.application.app_context():
        p = Patient.query.filter_by(patient_id=1).first()
    r = client.post(f"/patients/{p.id}/edit", data={
        "gender": "Female",
        "age": "61",
        "hypertension": "1",
        "ever_married": "Yes",
        "work_type": "Private",
        "residence_type": "Urban",
        "avg_glucose_level": "110.5",
        "bmi": "31.1",
        "smoking_status": "smokes",
        "stroke": "0",
    }, follow_redirects=True)
    assert r.status_code == 200
    assert b"Patient" in r.data

    r = client.post(f"/patients/{p.id}/delete", follow_redirects=True)
    assert r.status_code == 200
    with client.application.app_context():
        assert Patient.query.filter_by(patient_id=1).first() is None
