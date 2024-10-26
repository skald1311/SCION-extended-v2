import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

import glob
import os

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

def train_model(x_file, y_file):
    # Load the data
    x = pd.read_csv(x_file, index_col=0)
    y = pd.read_csv(y_file, index_col=0).squeeze()

    # Train the model

    #model = RandomForestRegressor(n_estimators=100, max_depth=None, random_state=42)
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=None, random_state=42)
    
    model.fit(x, y)

    # Get feature importances
    feature_importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': x.columns,
        'Importance': feature_importances
    })

    # Extract target gene name from the file name
    target_gene_name = os.path.basename(y_file).split('_')[1].split('.')[0]
    print(f"Feature Importances for {target_gene_name}:")
    print(feature_importance_df)

    # Return the trained model and the feature importance DataFrame
    return model, feature_importance_df

def main():
    # Find all x and y files
    x_files = glob.glob("../x_y_csv_cluster/x_*.csv")
    y_files = glob.glob("../x_y_csv_cluster/y_*.csv")

    # Sort the files to ensure corresponding pairs (matching order)
    x_files.sort()
    y_files.sort()

    # List to store models and feature importance dataframes
    results = []

    # Loop through all pairs of x and y files and train models
    for x_file, y_file in zip(x_files, y_files):
        model, feature_importance_df = train_model(x_file, y_file)
        results.append({
            'x_file': x_file,
            'y_file': y_file,
            'model': model,
            'feature_importance': feature_importance_df
        }
        )
        print("-----------------------------------")

    imList = pd.DataFrame()
    for result in results:
        y_file = result['y_file']
        feature_importance_df = result['feature_importance']
        
        # Extract target gene name from the file name to use as a column
        target_gene_name = os.path.basename(y_file).split('_')[1].split('.')[0]
        
        # Add the target gene name as a new column in the feature importance DataFrame
        feature_importance_df['Target Gene'] = target_gene_name
        
        # Append this DataFrame to the main DataFrame
        imList = pd.concat([imList, feature_importance_df], ignore_index=True)

    # Export all feature importances to a single CSV file
    output_file = "imListPython.csv"
    imList.to_csv(output_file, index=False)

if __name__ == '__main__':
    main()