# =========================================
# IMPORT LIBRARIES
# =========================================

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

# =========================================
# LOAD CLEANED DATASET
# =========================================

df = pd.read_excel("Threat_Dataset_Cleaned_Data.xlsx")

print("\nDATASET LOADED SUCCESSFULLY\n")

# =========================================
# HANDLE MISSING VALUES
# =========================================

df.replace([np.inf, -np.inf], np.nan, inplace=True)

df.fillna(0, inplace=True)

print("MISSING VALUES REMOVED\n")

# =========================================
# CREATE LABEL
# =========================================

df['Label'] = np.where(
    
    (
        (df['Flow Duration'] > df['Flow Duration'].quantile(0.60)) &
        (df['Total Fwd Packets'] > df['Total Fwd Packets'].median())
    ),
    
    'ATTACK',
    
    'BENIGN'
)

print("LABEL CREATED\n")

# =========================================
# SELECT FEATURES
# =========================================

X = df[[
    
    'Flow Packets/s',
    'Flow IAT Mean',
    'Packet Length Mean',
    'Average Packet Size',
    'Flow Bytes/s'
]]

y = df['Label']

# =========================================
# LABEL ENCODING
# =========================================

le = LabelEncoder()

y = le.fit_transform(y)

# =========================================
# FEATURE SCALING
# =========================================

scaler = StandardScaler()

X = scaler.fit_transform(X)

# =========================================
# SPLIT DATASET
# =========================================

X_train, X_test, y_train, y_test = train_test_split(
    
    X,
    y,
    test_size=0.3,
    random_state=42
)

print("DATA SPLIT COMPLETED\n")

# =========================================
# RANDOM FOREST MODEL
# =========================================

model = RandomForestClassifier(
    
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("MODEL TRAINED SUCCESSFULLY\n")

# =========================================
# PREDICTION
# =========================================

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("MODEL ACCURACY :", round(accuracy * 100, 2), "%")

# =========================================
# SAVE MODEL
# =========================================

joblib.dump(model, "best_model.pkl")

joblib.dump(scaler, "scaler.pkl")

print("\nMODEL SAVED SUCCESSFULLY")