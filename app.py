from flask import Flask, render_template
import pandas as pd
import sqlite3

app = Flask(__name__)

# Initialize database with data from the CSV
def init_database():
    conn = sqlite3.connect("data/data.db")
    df = pd.read_csv("data/diabetes.csv")
    df.to_sql("diabetes", conn, if_exists="replace", index=False)
    conn.close()

# Initialize the database
init_database()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    # Dataset information
    dataset_info = {
        "source": "Diabetes Dataset from Kaggle",
        "link": "https://www.kaggle.com/datasets/mathchi/diabetes-data-set",
        "variables": [
            {"name": "Pregnancies", "description": "Number of pregnancies."},
            {"name": "Glucose", "description": "Plasma glucose concentration after a 2-hour test."},
            {"name": "BloodPressure", "description": "Diastolic blood pressure (mm Hg)."},
            {"name": "SkinThickness", "description": "Triceps skin fold thickness (mm)."},
            {"name": "Insulin", "description": "2-Hour serum insulin (mu U/ml)."},
            {"name": "BMI", "description": "Body mass index (weight in kg/(height in m)^2)."},
            {"name": "DiabetesPedigreeFunction", "description": "Likelihood of diabetes based on family history."},
            {"name": "Age", "description": "Age in years."},
            {"name": "Outcome", "description": "Diabetes diagnosis outcome (1: Yes, 0: No)."}
        ]
    }
    return render_template("about.html", dataset_info=dataset_info)

@app.route("/data")
def data():
    conn = sqlite3.connect("data/data.db")
    df = pd.read_sql("SELECT * FROM diabetes LIMIT 10", conn)
    conn.close()
    return render_template("data.html", tables=(df.to_html(classes="table table-striped", index=False)))

if __name__ == "__main__":
    app.run(debug=True)
