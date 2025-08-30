# 💎 Gemstone Price Prediction – End-to-End ML Project  

[![Build Status](https://github.com/AdMub/Gemstone-Price-Prediction-End-to-End-Projects/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/AdMub/Gemstone-Price-Prediction-End-to-End-Projects/actions)  
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)  
[![Azure](https://img.shields.io/badge/Deployed%20on-Azure-0089D6?logo=microsoft-azure)](https://portal.azure.com)  
[![AWS](https://img.shields.io/badge/Deployed%20on-AWS-FF9900?logo=amazon-aws)](https://aws.amazon.com)  

---

## 📌 Project Overview  
This is a **full end-to-end Machine Learning project** that predicts the 💎 **price of gemstones/diamonds** based on multiple features.  

The project demonstrates the **complete ML lifecycle**:  
- Data ingestion, preprocessing & feature engineering  
- Exploratory Data Analysis (EDA)  
- Model training & selection with multiple ML algorithms  
- Workflow automation with **DVC** & **Apache Airflow**  
- CI/CD deployment with **GitHub Actions → Azure & AWS**  
- Containerized with **Docker & Docker Compose**  
- Web app frontend built with **Flask, HTML, CSS, JS**  

---

## 📊 Dataset Description  
The dataset contains **10 independent variables** and **1 target variable** (`price`).  

| Column   | Description |
|----------|-------------|
| id       | Unique identifier of each diamond |
| carat    | Weight of the diamond |
| cut      | Quality of the diamond cut |
| color    | Diamond color grade |
| clarity  | Diamond clarity grade |
| depth    | Height of the diamond (mm) |
| table    | Flat top surface width (%) |
| x        | Diamond length (mm) |
| y        | Diamond width (mm) |
| z        | Diamond depth (mm) |
| price    | 💰 Target variable – Price of the diamond |

---

## ⚙️ Tech Stack  
- **Languages & Frameworks**: Python, Flask, HTML, CSS, JS  
- **ML Libraries**: scikit-learn, XGBoost, pandas, numpy  
- **Modeling Techniques**:  
  - Preprocessing: `OrdinalEncoder`, `StandardScaler`, `ColumnTransformer`, `SimpleImputer`  
  - ML Models: `LinearRegression`, `Ridge`, `Lasso`, `ElasticNet`, `RandomForestRegressor`, `AdaBoostRegressor`, `XGBRegressor`  
  - Evaluation: `r2_score`  
- **MLOps Tools**: DVC, Apache Airflow, Tox (flake8, pytest)  
- **CI/CD & Deployment**: GitHub Actions, Azure App Service, AWS Elastic Beanstalk  
- **Containerization**: Docker, Docker Compose  

---

## 🚀 Features  
✅ End-to-End ML Pipeline  
✅ Automated Data Versioning (DVC)  
✅ Orchestrated with Apache Airflow  
✅ Multiple Regression Models → Best Model Selection  
✅ Logging & Custom Exception Handling  
✅ Testing with Unit & Integration Tests (`pytest -v`)  
✅ Code Quality enforced with `flake8` via **tox.ini**  
✅ Containerized using Docker + Docker Compose  
✅ CI/CD with GitHub Actions → Deploy to Azure & AWS  

---

## 🏗️ Architecture  

<img width="46527" height="771" alt="ml_pipeline_diagram" src="https://github.com/user-attachments/assets/590bf7a5-3685-4f81-918a-47537c9bbaa0" />


---

## 🌐 Web Application (Flask)  
The web app has three main pages:  
- **Home Page** 🏠 – Introduction & navigation

<img width="1912" height="905" alt="home" src="https://github.com/user-attachments/assets/bcdbad35-faad-4228-b961-a1afb35c131e" />

  
- **Form Page** 📝 – Input diamond features

<img width="1912" height="907" alt="form" src="https://github.com/user-attachments/assets/30772138-452a-4abf-a07d-6fb299fea040" />

  
- **Result Page** 📈 – Predicted diamond price

<img width="1920" height="790" alt="result" src="https://github.com/user-attachments/assets/46d4ba1f-1570-4622-9cbe-cdb438b0e417" />


---

## 🔧 Setup & Installation  

### 1️⃣ Clone the repo  
```bash
git clone https://github.com/AdMub/Gemstone-Price-Prediction-End-to-End-Projects.git
cd Gemstone-Price-Prediction-End-to-End-Projects
```

### 2️⃣ Create virtual environment & install requirements
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 3️⃣ Run with Docker
```bash
docker-compose up --build
```

### 4️⃣ Run locally
```bash
python app.py
```
App will be available at: `http://127.0.0.1:8000`


---

## 🧪 Testing & Linting

Run **unit & integration tests:**
```bash
pytest -v tests/unit
pytest -v tests/integration
```

Run **linting** with `flake8` (via tox):
```bash
tox
```

---

## 📦 CI/CD
- GitHub Actions for build, test, lint & deployment
- Deployments to Azure App Service & AWS Elastic Beanstalk
- Dockerized for consistent environment


---


## 📈 Results & Performance  

We compared multiple regression models to predict gemstone prices.  

**Models evaluated:**  
`LinearRegression, Ridge, Lasso, ElasticNet, RandomForest, AdaBoost, XGBoost`  

| Model             | MSE           | MAE        | R² Score |
|-------------------|---------------|------------|----------|
| LinearRegression  | 1.013246e+06  | 671.59     | 0.9373   |
| Lasso             | 1.013790e+06  | 673.00     | 0.9373   |
| Ridge             | 1.013256e+06  | 671.61     | 0.9373   |
| ElasticNet        | 2.298790e+06  | 1053.42    | 0.8577   |
| RandomForest      | 3.683084e+05  | 309.22     | 0.9772   |
| XGBoost           | 3.427367e+05  | 296.96     | **0.9788** |

### 🏆 Best Performing Model  
- **XGBoost Regressor**  
- Achieved the highest **R² Score = 0.9788**, with the lowest MAE and MSE among all models.  
- Metrics considered: **R² Score, MAE, MSE**. 

---


## 🛡️ Logging & Error Handling
- Custom **logging module** to track pipeline execution
- Centralized **custom exception handling** for debugging


---

## 👨‍💻 Author  

**Mubarak Adisa**  

🎓 Civil Engineering @ University of Ibadan | Computer Science @ University of the People  
🌍 Passionate about AI, Data Science & MLOps  

🔗 **Connect with me:**  
- [GitHub](https://github.com/AdMub)  
- [LinkedIn](https://www.linkedin.com/in/https://www.linkedin.com/in/mubarak-adisa-334a441b6/)  
