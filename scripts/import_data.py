import argparse
import pandas as pd

from app import create_app
from app.extensions import db
from app.models import Patient


def run(db_uri, file_path):
    app = create_app()
    if db_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    with app.app_context():
        db.create_all()
        df = pd.read_csv(file_path)
        if "bmi" in df.columns:
            median_bmi = df["bmi"].median(skipna=True)
            df["bmi"] = df["bmi"].fillna(median_bmi)
        for _, row in df.iterrows():
            pid = int(row["id"]) if "id" in df.columns else int(row["patient_id"])  
            if Patient.query.filter_by(patient_id=pid).first():
                continue
            p = Patient(
                patient_id=pid,
                gender=str(row["gender"]),
                age=float(row["age"]),
                hypertension=int(row["hypertension"]),
                ever_married=str(row["ever_married"]),
                work_type=str(row["work_type"]),
                residence_type=str(row["residence_type"]),
                avg_glucose_level=float(row["avg_glucose_level"]),
                bmi=float(row["bmi"]) if not pd.isna(row["bmi"]) else None,
                smoking_status=str(row["smoking_status"]),
                stroke=int(row["stroke"]),
            )
            db.session.add(p)
        db.session.commit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="sqlite:///instance/app.db")
    parser.add_argument("--file", default="data/stroke_data.csv")
    args = parser.parse_args()
    run(args.db, args.file)


if __name__ == "__main__":
    main()
