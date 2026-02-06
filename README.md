# Streaming Customer Segmentation & Retention Dashboard

An end-to-end analytics dashboard that segments streaming users into **Loyal, Dormant, and Risky** groups and recommends **targeted discounts** using business rules + K-Means behavioral clustering.

---

## Project Objective

To help a streaming platform:

* Identify users likely to churn
* Segment customers based on engagement & recency
* Recommend which users should receive retention discounts
* Provide an interactive dashboard for marketing teams

---

## Approach

### 1. Feature Engineering

Created behavioral features from raw data:

* **days_since_last_login** – recency indicator
* **engagement_level** – derived from watch hours (quantile based)
* Customer profile: country, subscription type

### 2. Business Rule Segmentation

Users classified as:

* **Loyal** – High engagement & active within 60 days
* **Dormant** – Medium/High engagement but inactive 60–120 days
* **Risky** – Low engagement or inactive >120 days

### 3. ML Validation (K-Means)

* Unsupervised clustering on:

  * Watch_Time_Hours
  * days_since_last_login
* Used to validate whether natural behavior groups align with rule-based segments.

### 4. Discount Strategy

Target group:

* Dormant users
* Risky users with Medium engagement

Success metrics:

* Renewal rate
* Watch time increase
* Improvement in last login within 30 days

---

## Dashboard Features

* Upload any streaming user CSV
* Segment distribution charts
* Engagement comparison
* K-Means cluster visualization
* Discount target table
* One-click CSV download
* Country & plan filters

---

## Tech Stack

* Python
* Pandas
* Scikit-learn
* Streamlit
* Plotly

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Key Learnings

* Avoided data leakage by separating rules from ML
* Derived thresholds from data quantiles
* Combined business logic with ML validation
* Built deployable analytics product instead of toy model

---

## Future Improvements

* Add real churn labels when available
* A/B test discount effectiveness
* Automated daily pipeline
* Multi-genre engagement features
