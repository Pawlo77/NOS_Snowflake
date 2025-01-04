import os

import pandas as pd
import streamlit as st
from snowflake.ml._internal.utils import identifier
from snowflake.ml.registry import Registry
from snowflake.snowpark import Session

# Retrieve Snowflake connection parameters from environment variables
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")

# If any of the required environment variables are missing, raise an error
if not all([user, password, account, warehouse, database, schema]):
    raise ValueError("Missing one or more Snowflake connection environment variables.")

# Set up Snowflake session configuration
connection_parameters = {
    "user": user,
    "password": password,
    "account": account,
    "warehouse": warehouse,
    "database": database,
    "schema": schema,
}

sp_session = Session.builder.configs(connection_parameters).create()
db = identifier._get_unescaped_name(sp_session.get_current_database())
schema = identifier._get_unescaped_name(sp_session.get_current_schema())
native_registry = Registry(session=sp_session, database_name=db, schema_name=schema)

model_name = "MPG_PREDICTION"
version_name = "v0"

# Streamlit app title
st.title("MPG Prediction")


# Load the distinct values for categorical columns (CYLINDERS, MODEL_YEAR, ORIGIN)
@st.cache_data
def load_distinct_values(table_name="auto_mpg"):
    df = sp_session.table(table_name)
    distinct_values = {
        "CYLINDERS": df.select("CYLINDERS")
        .distinct()
        .to_pandas()["CYLINDERS"]
        .tolist(),
        "MODEL_YEAR": df.select("MODEL_YEAR")
        .distinct()
        .to_pandas()["MODEL_YEAR"]
        .tolist(),
        "ORIGIN": df.select("ORIGIN").distinct().to_pandas()["ORIGIN"].tolist(),
    }
    return distinct_values


def preprocess_input_data(
    displacement,
    horsepower,
    weight,
    acceleration,
    selected_cylinders,
    selected_model_year,
    selected_origin,
):
    # Fetch means and standard deviations from Snowflake
    means_df = sp_session.table("TRAIN_MEANS").to_pandas()
    stddev_df = sp_session.table("TRAIN_STDDEVS").to_pandas()

    # Extract means and stddevs for the relevant columns
    means = means_df.set_index("column")["mean"].to_dict()
    stddevs = stddev_df.set_index("column")["stddev"].to_dict()

    # Creating a dataframe for the input data
    input_data = pd.DataFrame(
        {
            "CYLINDERS": [selected_cylinders],
            "MODEL_YEAR": [selected_model_year],
            "ORIGIN": [selected_origin],
            "DISPLACEMENT": [displacement],
            "HORSEPOWER": [horsepower],
            "WEIGHT": [weight],
            "ACCELERATION": [acceleration],
        }
    )

    # Impute and standardize the input data using means and stddevs from Snowflake
    for col in ["DISPLACEMENT", "HORSEPOWER", "WEIGHT", "ACCELERATION"]:
        if col in means and col in stddevs:
            input_data[col] = (input_data[col] - means[col]) / stddevs[col]

    return input_data


# Load the trained model
@st.cache_resource
def load_model():
    return native_registry.get_model(model_name=model_name).version(version_name)


# Fetch distinct values for categorical columns
distinct_values = load_distinct_values()

# Display filters for categorical columns
selected_cylinders = st.selectbox("Select Cylinder Count", distinct_values["CYLINDERS"])
selected_model_year = st.selectbox("Select Model Year", distinct_values["MODEL_YEAR"])
selected_origin = st.selectbox("Select Origin", distinct_values["ORIGIN"])

# Numeric column input
displacement = st.number_input(
    "Displacement", min_value=0.0, max_value=1000.0, step=0.1
)
horsepower = st.number_input("Horsepower", min_value=0.0, max_value=500.0, step=0.1)
weight = st.number_input("Weight", min_value=500.0, max_value=5000.0, step=1.0)
acceleration = st.number_input("Acceleration", min_value=0.0, max_value=100.0, step=0.1)

# Preprocess the user input data
input_data = preprocess_input_data(
    displacement,
    horsepower,
    weight,
    acceleration,
    selected_cylinders,
    selected_model_year,
    selected_origin,
)

# Load the model
model = load_model()

# Predict MPG
if st.button("Predict"):
    # Make prediction using the loaded model
    prediction = model.run(input_data, function_name="predict")
    prediction = prediction["output_feature_0"].values[0]

    # Define background color based on MPG value
    if prediction < 20:
        bg_color = "#FFCCCC"  # Red for low MPG (inefficient)
    elif 20 <= prediction <= 30:
        bg_color = "#FFFFCC"  # Yellow for moderate MPG
    else:
        bg_color = "#CCFFCC"  # Green for high MPG (efficient)

    # Display the result with a styled card
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; 
                    background-color: {bg_color}; border: 2px solid #cce7ff;">
            <h3 style="color: #007BFF;">🚗 Predicted MPG</h3>
            <p style="font-size: 24px; font-weight: bold; color: #00376b;">
                {prediction:.2f}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
