# ChronicCare+ 🏥

A comprehensive **AI-powered healthcare application** for predicting chronic diseases and providing personalized health recommendations.

## 📋 Overview

ChronicCare+ is an intelligent health monitoring system that leverages machine learning to:
- Predict **Diabetes**, **Hypertension**, **Stroke**, and **Kidney Disease**
- Diagnose diseases based on symptoms using an SVC classifier
- Provide personalized **medications**, **diets**, **workouts**, and **precautions**
- Track health parameters through an interactive dashboard
- Offer expert medical recommendations and guidance

## ✨ Features

### Disease Prediction Models
- **Multiple ML Algorithms**: Logistic Regression, Random Forest, and XGBoost
- **Accurate Predictions**: Ensemble models for robust disease risk assessment
- **Comparative Analysis**: View predictions from different models side-by-side

### Health Diagnosis System
- **Symptom-Based Diagnosis**: AI-powered disease identification from symptoms
- **Comprehensive Disease Coverage**: 41+ diseases across various categories
- **Detailed Recommendations**: 
  - Disease descriptions
  - Precautionary measures
  - Medication suggestions
  - Dietary recommendations
  - Workout plans

### Interactive Dashboard
- **Real-time Health Monitoring**: Track key health metrics
- **Health Parameters**: BMI, Insulin, Cholesterol, Creatinine, Blood Pressure, Glucose
- **Visual Analytics**: Charts and graphs for health insights

### User-Friendly Web Interface
- Separate forms for diabetes, hypertension, stroke, and kidney disease prediction
- Instant results with prediction confidence
- About, Blog, and Contact sections
- Developer information page

## 🏗️ Project Structure

```
ChronicCare/
├── ChronicCare+/                 # Main Flask application
│   ├── app.py                    # Main Flask app with disease prediction APIs
│   ├── main.py                   # Disease diagnosis system
│   ├── health_assistant.py       # AI assistant features
│   ├── health_dashboard.py       # Interactive health dashboard
│   ├── models/                   # Pre-trained ML models
│   │   ├── Logistic_Regression_*_model.pkl
│   │   ├── Random_Forest_*_model.pkl
│   │   ├── XGBoost_*_model.pkl
│   │   └── svc.pkl               # Symptom-based disease classifier
│   ├── static/
│   │   └── css/                  # Styling
│   └── templates/                # HTML templates
│       ├── index.html            # Home page
│       ├── diabetes_form.html    # Diabetes prediction form
│       ├── hypertension_form.html
│       ├── stroke_form.html
│       ├── kidney_form.html
│       ├── *_result.html         # Results pages
│       └── ...
├── datasets/                     # Training and reference data
│   ├── diabetes_data.csv
│   ├── hypertension_data.csv
│   ├── kidney_disease.csv
│   ├── stroke_data.csv
│   ├── symtoms_df.csv
│   ├── precautions_df.csv
│   ├── medications.csv
│   ├── diets.csv
│   ├── workout_df.csv
│   └── ...
├── medicine recommendation/      # Medicine recommendation module
├── Chronic model pkl.ipynb       # Model training notebook
└── README.md                     # This file
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **Dash**: Interactive dashboard framework
- **scikit-learn**: Machine learning models
- **XGBoost**: Gradient boosting
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Joblib**: Model serialization
- **Pickle**: Model persistence

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling
- **JavaScript**: Interactivity
- **Bootstrap**: Responsive design (implied)

### Data Science
- **Jupyter Notebook**: Model training and experimentation

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip or conda
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SubashinS/ChronicCare.git
cd ChronicCare
```

2. **Create a virtual environment** (recommended)
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n chroniccare python=3.9
conda activate chroniccare
```

3. **Install dependencies**
```bash
pip install flask dash scikit-learn xgboost pandas numpy joblib plotly
```

4. **Download Models and Datasets**
   - The pre-trained models (`.pkl` files) and datasets (`.csv` files) are excluded from the repository due to size limits
   - Download them from the project's data repository or train them using the provided notebook
   - Place models in `ChronicCare+/models/`
   - Place datasets in `datasets/`

5. **Configure file paths** (if needed)
   - Update dataset paths in `main.py` and `app.py`
   - Adjust model paths if moving files

### Running the Application

#### Option 1: Run the Main Flask App
```bash
cd ChronicCare+
python app.py
```
Access at `http://localhost:5000`

#### Option 2: Run the Diagnosis System
```bash
python main.py
```

#### Option 3: Run with Dashboard
```bash
python app.py
```
Access dashboard at `http://localhost:5000/health_dashboard/`

## 📊 How to Use

### Disease Risk Prediction
1. Navigate to the disease prediction form (Diabetes, Hypertension, Stroke, or Kidney Disease)
2. Enter your health metrics
3. View predictions from multiple ML models
4. See comparative analysis of model predictions

### Symptom-Based Diagnosis
1. Use the diagnosis feature
2. Select your symptoms
3. AI identifies potential diseases
4. View detailed recommendations including:
   - Disease description
   - Precautionary measures
   - Medication suggestions
   - Dietary recommendations
   - Exercise routines

### Health Dashboard
1. Access the interactive health dashboard
2. Select health parameters to monitor
3. View visual analytics and trends

## 📈 Models Included

### Diabetes Prediction
- Logistic Regression
- Random Forest
- XGBoost

### Hypertension Prediction
- Logistic Regression
- Random Forest
- XGBoost

### Stroke Prediction
- Logistic Regression
- Random Forest
- XGBoost

### Kidney Disease Prediction
- Logistic Regression
- Random Forest
- XGBoost

### Disease Diagnosis (from symptoms)
- Support Vector Classifier (SVC)

## 📚 Training Data

The project includes comprehensive datasets:
- **Diabetes Data**: Glucose levels, BMI, health metrics
- **Hypertension Data**: Blood pressure readings, heart rate data
- **Stroke Data**: Medical history, lifestyle factors
- **Kidney Disease Data**: Creatinine, urine analysis
- **Symptom Data**: 131 symptoms across 41+ diseases
- **Medical Database**: Medications, diets, precautions, workouts

## 🔧 Configuration

### Model Paths
Models are loaded from `ChronicCare+/models/` directory. Update paths in:
- `ChronicCare+/app.py` - Disease prediction models
- `ChronicCare+/main.py` - Diagnosis and recommendation models

### Dataset Paths
Datasets are loaded from `datasets/` directory. Adjust paths in:
- `ChronicCare+/main.py` - CSV file locations

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**Important**: This application is for educational and informational purposes only. It is **NOT a substitute for professional medical advice**. 

- Always consult a qualified healthcare professional for medical diagnosis and treatment
- Do not rely solely on this application for health decisions
- In case of medical emergencies, contact a healthcare provider immediately
- The predictions made by this system are based on machine learning models and may not be 100% accurate

## 👨‍💻 Author

**Subashin S**
- GitHub: [@SubashinS](https://github.com/SubashinS)
- Repository: [ChronicCare](https://github.com/SubashinS/ChronicCare)

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

## 🙏 Acknowledgments

- Healthcare datasets from Kaggle and UCI Machine Learning Repository
- Machine learning libraries: scikit-learn, XGBoost
- Flask and Dash frameworks for web development
- Contributors and supporters

---

**Last Updated**: May 2026

**Version**: 1.0.0
