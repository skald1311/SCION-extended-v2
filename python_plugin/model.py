import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import math

import glob
import os

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

def train_model(x_file, y_file):
    # Load the data
    x = pd.read_csv(x_file, index_col=0)
    y = pd.read_csv(y_file, index_col=0).squeeze()

    # Match parameters with R's randomForest
    num_inputs = x.shape[1]
    mtry = round(math.sqrt(num_inputs))  # K == "sqrt"

    # Train the model

    model = RandomForestRegressor(n_estimators=10000,
                                  max_depth=None,           # default of R's randomForest 
                                  max_features=mtry,        # K = "sqrt"
                                  n_jobs=1,                 # num.cores = 1
                                  verbose=1,                # trace = True
                                  #min_samples_leaf=5,       
                                  min_samples_split=5,      # nodesize=5 (default of R)
                                  random_state=2020)
    #model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=None, random_state=42)
    
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

def find_hub_genes(cluster_network):
    """Find hub gene(s) with the highest outdegree in the given cluster network DataFrame."""
    # Count occurrences of each regulator in the 'Feature' (Regulator) column
    regulator_counts = cluster_network['Feature'].value_counts()
    
    # Find the maximum outdegree
    max_outdegree = regulator_counts.max()
    
    # Identify hub gene(s) (genes with the highest outdegree)
    hubs = regulator_counts[regulator_counts == max_outdegree].index.tolist()
    
    return hubs

def main():
    output_dir = "cluster_networks"
    os.makedirs(output_dir, exist_ok=True)

    # Find all x and y files, not including the hub files
    x_files = [f for f in glob.glob("../x_y_csv_cluster/x_*.csv") if "_hub" not in f]
    y_files = [f for f in glob.glob("../x_y_csv_cluster/y_*.csv") if "_hub" not in f]

    # Sort the files to ensure corresponding pairs (matching order)
    x_files.sort()
    y_files.sort()

    cluster_results = {}
    all_hubs = set()

    # loop through all pairs of x and y files and train models
    for x_file, y_file in zip(x_files, y_files):
        # extract cluster number
        cluster_number = os.path.basename(x_file).split('_')[-1].split('.')[0]

        model, feature_importance_df = train_model(x_file, y_file)

        if cluster_number not in cluster_results:
            cluster_results[cluster_number] = []

        cluster_results[cluster_number].append({
            'x_file': x_file,
            'y_file': y_file,
            'model': model,
            'feature_importance': feature_importance_df
        })
        print("-----------------------------------")

    # Write separate output files for each cluster
    for cluster_number, results in cluster_results.items():
        imList = pd.DataFrame()
        for result in results:
            y_file = result['y_file']
            feature_importance_df = result['feature_importance']
            
            # Extract target gene name from the file name to use as a column
            target_gene_name = os.path.basename(y_file).split('_')[1].split('.')[0]
            
            # Add the target gene name as a new column in the feature importance DataFrame
            feature_importance_df['Target Gene'] = target_gene_name
            
            # Append this DataFrame to the main DataFrame for this cluster
            imList = pd.concat([imList, feature_importance_df], ignore_index=True)

        # Export the feature importances for the current cluster to a separate CSV file
        output_file = os.path.join(output_dir, f"imList_cluster_{cluster_number}.csv")
        imList.to_csv(output_file, index=False)
        print(f"Exported feature importances for cluster {cluster_number} to {output_file}")

        # find hub genes
        hubs = find_hub_genes(imList)
        for hub in hubs:
            all_hubs.add(hub)
    
    hubs_df = pd.DataFrame(all_hubs)
    hubs_df.to_csv(os.path.join(output_dir, "all_hub_genes.csv"), index=False)


if __name__ == '__main__':
    main()