import pandas as pd

def add_features(df):
    df["Last_Login"] = pd.to_datetime(df["Last_Login"])
    reference_date = df["Last_Login"].max()
    df["days_since_last_login"] = (reference_date - df["Last_Login"]).dt.days


    low_th = df["Watch_Time_Hours"].quantile(0.33)
    high_th = df["Watch_Time_Hours"].quantile(0.66)

    def engagement(hours):
        if hours < low_th:
            return "Low"
        elif hours < high_th:
            return "Medium"
        else:
            return "High"


    df["engagement_level"] = df["Watch_Time_Hours"].apply(engagement)

    return df


def customer_type(row):
    if row['engagement_level'] == 'High' and row['days_since_last_login'] < 60:
        return 'Loyal'

    elif (row['engagement_level'] in ['Medium','High']) and \
         (60 < row['days_since_last_login'] <= 120):
        return 'Dormant'

    else:
        return 'Risky'
    
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def run_kmeans(df):
    X = df[["Watch_Time_Hours", "days_since_last_login"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=2, random_state=42)

    df['ml_cluster'] = kmeans.fit_predict(X_scaled)

    return df, kmeans