# ⚡ Energy Production Prediction — Combined Cycle Power Plant

<div align="center">

[![GitHub](https://img.shields.io/badge/Author-Syed%20Mohd%20Altamash-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/syedaltamash-analytics)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=for-the-badge)

</div>

---

A machine learning regression project that predicts the **hourly electrical energy output (MW)** of a Combined Cycle Power Plant based on ambient environmental conditions. The best model is deployed as an interactive **Streamlit web application**.

> 🏫 **Group 4** — Aravind Ajai · Aishwarya Ningam · Lokesh R · Naveen Kumar · Delvin James · **Syed Mohd Altamash** · Avanti Sudhir Joshi

---

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Data Visualizations](#data-visualizations)
- [Correlation Insights](#correlation-insights)
- [Models & Results](#models--results)
- [Streamlit App](#streamlit-app)
- [Conclusion](#conclusion)
- [Technologies Used](#technologies-used)
- [Author](#author)

---

## Overview

Combined-cycle power plants generate electricity by harnessing both **gas turbines** and **steam turbines** in a single cycle. Exhaust heat from the gas turbine powers the steam turbine, maximizing overall efficiency.

This project builds a predictive model for energy output using **6 years of operational sensor data**. By quantifying how ambient conditions influence production, the model enables **real-time, data-driven decisions** to maximize plant efficiency.

**Goals:**
- Predict hourly energy output (MW) from four sensor readings
- Compare 11 regression algorithms on accuracy and generalization
- Deploy the best model as a live Streamlit web app

---

## Dataset

**Source:** Combined Cycle Power Plant dataset — **9,568 observations** collected over 6 years

| Feature | Description | Unit |
|---|---|---|
| `temperature` | Ambient temperature | °C |
| `exhaust_vacuum` | Exhaust vacuum pressure | cm Hg |
| `amb_pressure` | Ambient pressure | mbar |
| `r_humidity` | Relative humidity | % |
| `energy_production` | **Target** — net hourly energy output | MW |

**Data Quality:**
- ✅ Zero missing values across all 5 columns
- 🔁 41 duplicate rows found and removed
- Final cleaned shape: **(9,527 × 5)**

---

## Project Structure

```
├── Regression_Project.ipynb        # Full analysis and modelling notebook
├── app.py                          # Streamlit web application
├── energy_model.pkl                # Saved Random Forest model
├── data/
│   └── energy_production_data.csv  # Source dataset (semicolon-delimited)
└── README.md
```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/syedaltamash-analytics/energy-production-prediction.git
   cd energy-production-prediction
   ```

2. **Install dependencies**
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn xgboost streamlit joblib
   ```

---

## Usage

### Run the Jupyter Notebook

Open `Regression_Project.ipynb` in Jupyter or Google Colab and run all cells to reproduce the full analysis.

### Launch the Streamlit App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`, enter the four sensor values, and click **Predict Energy Production**.

### Load the Saved Model Directly

```python
import joblib

model = joblib.load('energy_model.pkl')
prediction = model.predict([[temperature, exhaust_vacuum, amb_pressure, r_humidity]])
print(f"Predicted Output: {prediction[0]:.2f} MW")
```

---

## Workflow

```
Data Loading → EDA (shape, info, describe)
      ↓
Missing Value Check (none found) → Duplicate Removal (41 rows dropped)
      ↓
Data Visualization (Histogram, Boxplot, Pairplot, Heatmap, Scatter)
      ↓
Outlier Removal via IQR Method
      ↓
Train / Test Split  →  80% Training  |  20% Testing
      ↓
Train 11 Regression Models → Evaluate (R², MAE, RMSE)
      ↓
Best Model Saved (joblib) → Streamlit App Deployment
```

---

## Data Visualizations

Five visualization types were used during EDA:

| Visualization | What It Reveals |
|---|---|
| **Histogram + KDE** | Distribution shape — temperature is bell-shaped; exhaust vacuum is bimodal |
| **Box Plot** | Spread and outlier positions for each feature |
| **Pairplot** | Pairwise relationships — clear negative trend between temperature and energy output |
| **Correlation Heatmap** | Exact correlation coefficients between all variable pairs |
| **Scatter Plots** | Direct relationship between energy production and each individual feature |

---

## Correlation Insights

Key findings from the **Correlation Matrix Heatmap**:

| Feature Pair | Correlation | Interpretation |
|---|---|---|
| Temperature ↔ Energy Production | **−0.95** | Strong negative — higher temp reduces output |
| Exhaust Vacuum ↔ Energy Production | **−0.87** | Strong negative — higher vacuum reduces output |
| Ambient Pressure ↔ Energy Production | **+0.52** | Moderate positive — higher pressure increases output |
| Relative Humidity ↔ Energy Production | **+0.39** | Weak positive — slight increase with humidity |
| Temperature ↔ Exhaust Vacuum | **+0.84** | Strong positive — both rise together |

> **Temperature** and **exhaust vacuum** are the dominant predictors of energy output.

---

## Models & Results

11 regression models were trained and evaluated on R², MAE, and RMSE:

| Model | Train R² | Test R² | Train MAE | Test MAE |
|---|---|---|---|---|
| Linear Regression | 0.9284 | 0.9283 | 3.6213 | 3.6441 |
| Ridge Regression | 0.9284 | 0.9283 | 3.6213 | 3.6441 |
| Lasso Regression | — | — | — | — |
| Elastic Net | 0.9279 | 0.9278 | 3.6418 | 3.6635 |
| **🥇 XGBoost** | **0.9878** | **0.9647** | **1.3643** | **2.2316** |
| **🥈 Random Forest** | **0.9945** | **0.9617** | **0.8852** | **2.3406** |
| **🥉 Bagging Regressor** | **0.9923** | **0.9588** | **0.9987** | **2.4380** |
| K-Nearest Neighbors | 0.9647 | 0.9468 | 2.3378 | 2.8719 |
| Gradient Boosting | 0.9539 | 0.9461 | 2.8113 | 2.9774 |
| Decision Tree | 1.0000 ⚠️ | 0.9327 | 0.0000 | 2.9695 |
| AdaBoost | 0.8977 | 0.8892 | 4.4668 | 4.5934 |

> ⚠️ **Decision Tree** — perfect Train R² of 1.0000 is a classic sign of **overfitting**.
> ⚠️ **AdaBoost** — weakest generalization with the highest MAE on both sets.

---

## Streamlit App

The deployed app uses the saved **Random Forest model** to make real-time predictions with a custom UI.

**Input Parameters:**

| Field | Sample Value |
|---|---|
| Temperature (°C) | 25.06 |
| Exhaust Vacuum (cm Hg) | 59.00 |
| Ambient Pressure (mbar) | 1013.00 |
| Relative Humidity (%) | 50.00 |

**Output:**
```
⚡ Predicted Energy Production: 447.82 MW
```

The app also renders:
- A **radar chart** showing the relative scale of all four input values
- An **energy gauge** (arc meter) visualizing output in the 0–600 MW range

---

## Conclusion

- **XGBoost** achieves the best test performance — R²: 0.9647, MAE: 2.23 MW.
- **Random Forest** is a close second and is the deployed model — R²: 0.9617, MAE: 2.34 MW.
- **Linear Regression** is a strong, stable baseline with zero overfitting (train ≈ test).
- **Decision Tree** perfectly memorizes training data but generalizes poorly.
- **AdaBoost** is the weakest fit for this continuous-output regression task.
- **Temperature** (−0.95) and **exhaust vacuum** (−0.87) are the most powerful predictors.

---

## Technologies Used

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat)
![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0?style=flat)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=flat&logo=googlecolab&logoColor=black)

---

## 👤 Author

<div align="center">

### Syed Mohd Altamash

*Data Science & Machine Learning Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-syedaltamash--analytics-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/syedaltamash-analytics)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Syed%20Mohd%20Altamash-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/syedaltamash-analytics)

</div>

