
from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the serialized ML pipeline
model = joblib.load("superkart_model.joblib")


def prepare_input(df):
    """
    Apply the same feature engineering used during model development.
    """
    df = df.copy()

    # Standardize Product_Sugar_Content
    df["Product_Sugar_Content"] = (
        df["Product_Sugar_Content"]
        .replace("reg", "Regular")
    )

    # Create Store_Age using the same reference year used during training
    if "Store_Establishment_Year" in df.columns:
        df["Store_Age"] = 2009 - df["Store_Establishment_Year"]
        df.drop(columns=["Store_Establishment_Year"], inplace=True)

    # Product_Id was excluded during model development
    if "Product_Id" in df.columns:
        df.drop(columns=["Product_Id"], inplace=True)

    # Remove target if supplied in a batch file
    if "Product_Store_Sales_Total" in df.columns:
        df.drop(columns=["Product_Store_Sales_Total"], inplace=True)

    return df


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SuperKart Sales Prediction API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:
        input_data = request.get_json()

        df = pd.DataFrame([input_data])
        df = prepare_input(df)

        prediction = model.predict(df)[0]

        return jsonify({
            "predicted_sales": float(prediction)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
