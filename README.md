# **Local Food Waste Management (LFWM)**

A data-driven project to **reduce food wastage** by connecting food providers with receivers using **SQL analytics, EDA, and AI-powered predictions**.

https://local-food-waste-management.streamlit.app/

---

## **📌 Project Overview**

Food wastage is a critical global issue, with tons of edible food discarded daily while millions go hungry.
The **Local Food Waste Management System** aims to bridge this gap by creating a platform where **restaurants, events, and individuals can donate surplus food**, and **NGOs or individuals in need can claim it**.

This project combines:
✔ A **Streamlit Web App** for user interaction
✔ **SQLite Database** for managing food listings and claims
✔ **SQL Queries & Analytics** for insights
✔ **Exploratory Data Analysis (EDA)** for patterns and trends
✔ **Machine Learning Model** for predicting claim success

---

## **🛠 Tech Stack**

* **Python 3**
* **Streamlit** (UI)
* **SQLite** (Database)
* **Pandas, Matplotlib, Seaborn** (Data Analysis & Visualization)
* **Scikit-learn** (Machine Learning)
* **SQL** (Data Queries & Reporting)

---

## **📂 Project Structure**

```
├── app.py                # Streamlit web application
├── Local_Food_Waste_Management.ipynb  # EDA, SQL queries, ML model notebook
├── food.db               # SQLite database (upload separately)
├── requirements.txt      # Required Python libraries
└── README.md             # Project documentation
```

---

## **✨ Features**

✔ **Food Listings & Claims** – Providers can add surplus food; receivers can claim it.
✔ **Advanced Filtering** – Search by city, food type, provider type, and meal type.
✔ **SQL Analytics** – Insights like:

* Providers & receivers by location
* Food expiring soon
* Most donated food items
* Claim success distribution
  ✔ **EDA & Visualizations** – Univariate, Bivariate, and Multivariate analysis.
  ✔ **AI Prediction Model** – Predicts claim completion likelihood using Logistic Regression.
  ✔ **Interactive Dashboard** – Real-time charts and reports using Streamlit.

---

## **📊 Key Insights**

* **Top contributing cities** and providers
* **Most popular food types and meal categories**
* **Trends in claim success and pending claims**
* **Identification of unclaimed or soon-to-expire items**

---

## **🤖 AI Model**

* **Algorithm:** Logistic Regression
* **Goal:** Predict probability of successful claim completion
* **Features:** Quantity, Provider Type, Location, Food Type, Meal Type


---


## **🚀 How to Run**

### **Option 1: Run Streamlit App**

```bash
pip install -r requirements.txt
streamlit run app.py
```

### **Option 2: Run EDA & Model in Jupyter/Colab**

* Open `Local_Food_Waste_Management.ipynb`
* Upload `food.db` when prompted
* Execute all cells for analysis, visualizations, and model training

---

## **🔮 Future Enhancements**

✔ **Geolocation-based matching**
✔ **Push notifications for new listings**
✔ **Mobile app integration**
✔ **Real-time food tracking**

---
