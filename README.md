# stroke-prediction-app
# Stroke Prediction App

Simple Flask application with authentication and patient CRUD for the Stroke Prediction Dataset.

## Setup

1. Create a virtual environment:
   - Windows: `python -m venv venv && venv\\Scripts\\activate`
   - macOS/Linux: `python -m venv venv && source venv/bin/activate`

2. Install dependencies: `pip install -r requirements.txt`

3. Run the app:
   - `python run.py`

4. Import sample data (optional):
   - `python scripts/import_data.py --db sqlite:///instance/app.db --file data/stroke_data.csv`

## Testing

Run tests with: `pytest`

## Structure

- `app/` Flask application modules
- `instance/` SQLite database location
- `scripts/` data import utility
- `tests/` pytest tests
- `docs/` security notes

