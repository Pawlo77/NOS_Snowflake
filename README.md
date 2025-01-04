# NOS_Snowflake
Network Operating Systems course for DS studies in Winter 2024/25

A **Streamlit-based web application** for predicting the **Miles Per Gallon (MPG)** of a vehicle using a trained machine learning model hosted in Snowflake. The application dynamically adjusts its styling to reflect the efficiency of the predicted MPG value.

Full project developement history is [here](./project_history.pdf). Full project report is [here](./raport.pdf).

---

## **Features**
- **Dynamic Input Interface**: Allows users to input key vehicle parameters like cylinders, displacement, horsepower, weight, acceleration, model year, and origin.
- **Real-time Prediction**: Uses a trained model stored in Snowflake's model registry to predict MPG.
- **Adaptive Styling**: The result card's background color changes based on the predicted MPG:
  - **Green**: High efficiency (MPG > 30).
  - **Yellow**: Moderate efficiency (20 ≤ MPG ≤ 30).
  - **Red**: Low efficiency (MPG < 20).
- **Streamlit GUI**: A user-friendly and interactive interface for data input and prediction.

---

## **Technologies Used**
- **Python**
- **Streamlit**: For creating the web application.
- **Snowflake**:
  - **Snowpark**: For managing data and model operations.
  - **Model Registry**: For hosting the machine learning model.
- **Joblib**: For loading the trained model locally (if applicable).
- **Pandas**: For handling data.
