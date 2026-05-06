from flask import Flask, render_template, request, jsonify
import joblib
import pickle
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from dash import dcc, html
import health_dashboard

app = Flask(__name__)

# Initialize Dash app
dash_app = health_dashboard.create_health_dashboard(app)

# Load models for diabetes, hypertension, stroke, and kidney disease predictions
models = {
    "diabetes": {
        "logistic_regression": joblib.load(r"ChronicCare+\models/Logistic_Regression_Diabetes_model.pkl"),
        "random_forest": joblib.load(r"ChronicCare+\models/Random_Forest_Diabetes_model.pkl"),
        "xgboost": joblib.load(r"ChronicCare+\models/XGBoost_Diabetes_model.pkl")
    },
    "hypertension": {
        "logistic_regression": joblib.load(r"ChronicCare+\models/Logistic_Regression_target_model.pkl"),
        "random_forest": joblib.load(r"ChronicCare+\models/Random_Forest_target_model.pkl"),
        "xgboost": joblib.load(r"ChronicCare+\models/XGBoost_target_model.pkl")
    },
    "stroke": {
        "logistic_regression": joblib.load(r"ChronicCare+\models/Logistic_Regression_stroke_model.pkl"),
        "random_forest": joblib.load(r"ChronicCare+\models/Random_Forest_stroke_model.pkl"),
        "xgboost": joblib.load(r"ChronicCare+\models/XGBoost_stroke_model.pkl")
    },
    "kidney": {
        "logistic_regression": joblib.load(r"ChronicCare+\models\Logistic_Regression_classification_model.pkl"),
        "random_forest": joblib.load(r"ChronicCare+\models/Random_Forest_classification_model.pkl"),
        "xgboost": joblib.load(r"ChronicCare+\models/XGBoost_classification_model.pkl")
    }
}


# Load SVC model
svc = pickle.load(open(r'ChronicCare+\models\svc.pkl', 'rb'))

def generate_graph(predictions):
    plt.figure(figsize=(6, 4))
    model_names = ["Logistic Regression", "Random Forest", "XGBoost"]
    plt.bar(model_names, predictions, color=["blue", "green", "orange"])
    plt.title("Model Predictions")
    plt.ylabel("Prediction Confidence")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return graph_url

# load databasedataset===================================
sym_des = pd.read_csv(r"datasets\symtoms_df.csv")
precautions = pd.read_csv(r"datasets\precautions_df.csv")
workout = pd.read_csv(r"datasets\workout_df.csv")
description = pd.read_csv(r"datasets\description.csv")
medications = pd.read_csv(r"datasets\medications.csv")
diets = pd.read_csv(r"datasets\diets.csv")

# Helper function
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = " ".join([w for w in workout[workout['disease'] == dis]['workout'].values])

    return desc, pre, med, die, wrkout

symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

# Model Prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/health_dashboard')
def health_dashboard():
    return dash_app.index()

@app.route("/predict/diabetes", methods=["GET", "POST"])
def predict_diabetes():
    if request.method == "POST":
        try:
            input_data = []
            fields = [
                "Age", "Sex", "HighChol", "CholCheck", "BMI", 
                "Smoker", "HeartDiseaseorAttack", "PhysActivity", 
                "Fruits", "Veggies", "HvyAlcoholConsump", "GenHlth", 
                "MentHlth", "PhysHlth", "DiffWalk", "Stroke", "HighBP"
            ]

            for field in fields:
                value = request.form.get(field, 0)
                value = float(value) if value else 0
                input_data.append(value)

            input_array = np.array(input_data).reshape(1, -1)

            # Get predictions from models
            diabetes_models = models["diabetes"]
            logistic_prediction = diabetes_models["logistic_regression"].predict_proba(input_array)[0][1]
            random_forest_prediction = diabetes_models["random_forest"].predict_proba(input_array)[0][1]
            xgboost_prediction = diabetes_models["xgboost"].predict_proba(input_array)[0][1]

            # Calculate confidence percentages
            logistic_confidence = round(logistic_prediction * 100, 2)
            random_forest_confidence = round(random_forest_prediction * 100, 2)
            xgboost_confidence = round(xgboost_prediction * 100, 2)


            # Generate a graph for comparison
            predictions = [logistic_prediction, random_forest_prediction, xgboost_prediction]
            graph_url = generate_graph(predictions)

            # Adjust threshold for positive diabetes prediction
            overall_prediction = sum([logistic_prediction > 0.3, random_forest_prediction > 0.3, xgboost_prediction > 0.3])
            diabetes_result = "Positive for Diabetes" if overall_prediction >= 2 else "Negative for Diabetes"

            return render_template(
                "diabetes_result.html",
                logistic_prediction=logistic_prediction,
                logistic_confidence=logistic_confidence,
                random_forest_prediction=random_forest_prediction,
                random_forest_confidence=random_forest_confidence,
                xgboost_prediction=xgboost_prediction,
                overall_prediction=overall_prediction,
                xgboost_confidence=xgboost_confidence,
                graph_url=graph_url,
                diabetes_result=diabetes_result
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return render_template("diabetes_form.html")

@app.route("/predict/hypertension", methods=["GET", "POST"])
def predict_hypertension():
    if request.method == "POST":
        try:
            input_data = [
                float(request.form.get("age", 0)),
                float(request.form.get("sex", 0)),
                int(request.form.get("cp", 0)),
                float(request.form.get("trestbps", 0)),
                float(request.form.get("chol", 0)),
                int(request.form.get("fbs", 0)),
                int(request.form.get("restecg", 0)),
                float(request.form.get("thalach", 0)),
                int(request.form.get("exang", 0)),
                float(request.form.get("oldpeak", 0)),
                int(request.form.get("slope", 0)),
                int(request.form.get("ca", 0)),
                int(request.form.get("thal", 0))
            ]
            input_array = np.array(input_data).reshape(1, -1)

            # Predict using models
            hypertension_models = models["hypertension"]
            logistic_prediction = hypertension_models["logistic_regression"].predict_proba(input_array)[0][1]
            random_forest_prediction = hypertension_models["random_forest"].predict_proba(input_array)[0][1]
            xgboost_prediction = hypertension_models["xgboost"].predict_proba(input_array)[0][1]

            # Calculate confidence percentages
            logistic_confidence = round(logistic_prediction * 100, 2)
            random_forest_confidence = round(random_forest_prediction * 100, 2)
            xgboost_confidence = round(xgboost_prediction * 100, 2)

            # Insights
            logistic_insights = "Logistic Regression: Blood pressure, cholesterol, and age are major contributors to hypertension risk."
            random_forest_insights = "Random Forest: Blood pressure and age are the strongest predictors."
            xgboost_insights = "XGBoost: Higher cholesterol and age elevate hypertension risk."

            # Generate graph
            predictions = [logistic_confidence, random_forest_confidence, xgboost_confidence]
            graph_url = generate_graph(predictions)

            # Determine overall hypertension prediction
            overall_prediction = sum([logistic_prediction > 0.3, random_forest_prediction > 0.3, xgboost_prediction > 0.3])
            hypertension_result = "Positive for Hypertension" if overall_prediction >= 2 else "Negative for Hypertension"

            return render_template(
                "hypertension_result.html",
                logistic_prediction=logistic_prediction,
                logistic_confidence=logistic_confidence,
                random_forest_prediction=random_forest_prediction,
                random_forest_confidence=random_forest_confidence,
                xgboost_prediction=xgboost_prediction,
                logistic_insights=logistic_insights,
                random_forest_insights=random_forest_insights,
                xgboost_insights=xgboost_insights,
                xgboost_confidence=xgboost_confidence,
                overall_prediction=overall_prediction,
                graph_url=graph_url,
                hypertension_result=hypertension_result
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return render_template("hypertension_form.html")

@app.route("/predict/stroke", methods=["GET", "POST"])
def predict_stroke():
    if request.method == "POST":
        try:
            input_data = [
                int(request.form.get("sex", 0)),
                float(request.form.get("age", 0)),
                int(request.form.get("hypertension", 0)),
                int(request.form.get("heart_disease", 0)),
                int(request.form.get("ever_married", 0)),
                int(request.form.get("work_type", 0)),
                int(request.form.get("Residence_type", 0)),
                float(request.form.get("avg_glucose_level", 0)),
                float(request.form.get("bmi", 0)),
                int(request.form.get("smoking_status", 0))
            ]
            input_array = np.array(input_data).reshape(1, -1)

            # Predict using models
            stroke_models = models["stroke"]
            logistic_prediction = stroke_models["logistic_regression"].predict_proba(input_array)[0][1]
            random_forest_prediction = stroke_models["random_forest"].predict_proba(input_array)[0][1]
            xgboost_prediction = stroke_models["xgboost"].predict_proba(input_array)[0][1]

            # Calculate confidence percentages
            logistic_confidence = round(logistic_prediction * 100, 2)
            random_forest_confidence = round(random_forest_prediction * 100, 2)
            xgboost_confidence = round(xgboost_prediction * 100, 2)

            # Insights
            logistic_insights = "Logistic Regression: Age and average glucose level are key predictors for stroke."
            random_forest_insights = "Random Forest: BMI and hypertension contribute significantly to stroke risk."
            xgboost_insights = "XGBoost: Smoking status and glucose levels are critical factors for stroke prediction."
   
            # Generate graph
            predictions = [logistic_confidence, random_forest_confidence, xgboost_confidence]
            graph_url = generate_graph(predictions)

            # Determine overall stroke prediction
            overall_prediction = sum([logistic_prediction > 0.5, random_forest_prediction <= 0.5, xgboost_prediction >= 0.9])
            stroke_result = "Positive for Stroke" if overall_prediction >= 2 else "Negative for Stroke"

            return render_template(
                "stroke_result.html",
                logistic_prediction=logistic_prediction,
                logistic_confidence=logistic_confidence,
                random_forest_prediction=random_forest_prediction,
                random_forest_confidence=random_forest_confidence,
                xgboost_prediction=xgboost_prediction,
                xgboost_confidence=xgboost_confidence,
                logistic_insights=logistic_insights,
                random_forest_insights=random_forest_insights,
                xgboost_insights=xgboost_insights,
                overall_prediction=overall_prediction,
                graph_url=graph_url,
                stroke_result=stroke_result
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return render_template("stroke_form.html")


@app.route('/predict/kidney', methods=['GET', 'POST'])
def predict_kidney():
    if request.method == 'POST':
        try:
            # Map categorical values to numeric
            rbc_map = {'normal': 0, 'abnormal': 1}
            pc_map = {'normal': 0, 'abnormal': 1}
            boolean_map = {'yes': 1, 'no': 0}
            pcc_map = {'present': 1, 'notpresent': 0}
            ba_map = {'present': 1, 'notpresent': 0}
            appet_map = {'good': 1, 'poor': 0}

            # Collect data from the form with proper mapping
            input_data = [
                float(request.form.get('age', 0)),
                float(request.form.get('bp', 0)),
                float(request.form.get('sg', 0)),
                float(request.form.get('al', 0)),
                float(request.form.get('su', 0)),
                rbc_map.get(request.form.get('rbc', 'normal'), 0),
                pc_map.get(request.form.get('pc', 'normal'), 0),
                pcc_map.get(request.form.get('pcc', 'notpresent'), 0),  
                ba_map.get(request.form.get('ba', 'notpresent'), 0),  
                float(request.form.get('bgr', 0)),
                float(request.form.get('bu', 0)),
                float(request.form.get('sc', 0)),
                float(request.form.get('sod', 0)),
                float(request.form.get('pot', 0)),
                float(request.form.get('hemo', 0)),
                float(request.form.get('pcv', 0)),
                float(request.form.get('wc', 0)),
                float(request.form.get('rc', 0)),
                boolean_map.get(request.form.get('htn', 'no'), 0),
                boolean_map.get(request.form.get('dm', 'no'), 0),
                boolean_map.get(request.form.get('cad', 'no'), 0),
                appet_map.get(request.form.get('appet', 'good'), 1),
                boolean_map.get(request.form.get('pe', 'no'), 0),
                boolean_map.get(request.form.get('ane', 'no'), 0)
            ]

            input_array = np.array(input_data).reshape(1, -1)

            # Predict using models
            kidney_models = models["kidney"]
            logistic_prediction = kidney_models["logistic_regression"].predict_proba(input_array)[0][1]
            random_forest_prediction = kidney_models["random_forest"].predict_proba(input_array)[0][1]
            xgboost_prediction = kidney_models["xgboost"].predict_proba(input_array)[0][1]

            # Calculate confidence percentages for each model
            logistic_confidence = round(logistic_prediction * 100, 2)
            random_forest_confidence = round(random_forest_prediction * 100, 2)
            xgboost_confidence = round(xgboost_prediction * 100, 2)

            # Generate graph
            predictions = [logistic_confidence, random_forest_confidence, xgboost_confidence]
            graph_url = generate_graph(predictions)

            # Determine overall kidney disease prediction
            overall_prediction = sum([logistic_prediction > 0.5, random_forest_prediction > 0.5, xgboost_prediction < 0.3])
            kidney_result = "Positive for Chronic Kidney Disease" if overall_prediction >= 2 else "Negative for Chronic Kidney Disease"

            logistic_insights = "Logistic Regression: Age and average glucose level are key predictors for stroke."
            random_forest_insights = "Random Forest: BMI and hypertension contribute significantly to stroke risk."
            xgboost_insights = "XGBoost: Smoking status and glucose levels are critical factors for stroke prediction."

            return render_template(
                'kidney_result.html',
                logistic_prediction=logistic_prediction,
                logistic_confidence=logistic_confidence,
                random_forest_prediction=random_forest_prediction,
                random_forest_confidence=random_forest_confidence,
                xgboost_prediction=xgboost_prediction,
                overall_prediction=overall_prediction,
                xgboost_confidence=xgboost_confidence,
                logistic_insights=logistic_insights,
                random_forest_insights=random_forest_insights,
                xgboost_insights=xgboost_insights,
                graph_url=graph_url,
                kidney_result=kidney_result
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return render_template('kidney_form.html')

@app.route("/recommendations", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        
        # Debugging print statement
        print(symptoms)

        if not symptoms or symptoms == "Symptoms":
            message = "Please either write symptoms or you have written misspelled symptoms"
            return render_template('indexx.html', message=message)
        else:
            # Split the user's input into a list of symptoms (assuming they are comma-separated)
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            # Remove any extra characters, if any
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]

            # Get predicted disease based on user symptoms
            predicted_disease = get_predicted_value(user_symptoms)

            # Get recommendations from helper function
            dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

            # Convert precautions into a list
            my_precautions = []
            for i in precautions[0]:
                my_precautions.append(i)

            # Render results on the recommendations page
            return render_template('indexx.html', predicted_disease=predicted_disease, 
                                   dis_des=dis_des, my_precautions=my_precautions, 
                                   medications=medications, my_diet=rec_diet, workout=workout)

    # Render the form page when GET request is made
    return render_template('indexx.html')


if __name__ == '__main__':
    app.run(debug=True)
