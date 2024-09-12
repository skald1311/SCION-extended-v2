import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor  # Or GradientBoostingClassifier for classification
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Load the data for one of your x and y
x = pd.read_csv('x_AT1G01060.csv', index_col=0)
y = pd.read_csv('y_AT1G01060.csv', index_col=0).squeeze()

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train a Gradient Boosting Regressor
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
model.fit(x_train, y_train)

# Get feature importances
feature_importances = model.feature_importances_

# Create a DataFrame for easy viewing and saving
feature_importance_df = pd.DataFrame({
    'Feature': x.columns,
    'Importance': feature_importances
})

# Optionally, print the results
target_gene_name = "y_AT1G01060.csv".split('_')[1].split('.')[0]  # Extract gene name from file
print(f"Feature Importances for {target_gene_name}:")
print(feature_importance_df)