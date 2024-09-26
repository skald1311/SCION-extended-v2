import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# Load the data for one of x and y
x = pd.read_csv('x_AT1G51140.csv', index_col=0)
y = pd.read_csv('y_AT1G51140.csv', index_col=0).squeeze()

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train a Gradient Boosting Regressor
# n_estimators: number of trees
# Set random state to get reproducible results
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
model.fit(x_train, y_train)

# Visualization of decision tree
# estimator = model.estimators_[0, 0]  # [1, 0] for 2nd tree, and so on...
# plt.figure(figsize=(20, 10))
# plot_tree(estimator, filled=True, feature_names=x_train.columns)
# plt.show()

# Get feature importances
feature_importances = model.feature_importances_

feature_importance_df = pd.DataFrame({
    'Feature': x.columns,
    'Importance': feature_importances
})

target_gene_name = "y_AT1G01060.csv".split('_')[1].split('.')[0]  # Extract target gene name from file
print(f"Feature Importances for {target_gene_name}:")
print(feature_importance_df)