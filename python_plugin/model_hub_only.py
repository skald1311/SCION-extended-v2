import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
import math

import glob
import os

def train_model(x_file, y_file):
    # Load the data
    x = pd.read_csv(x_file, index_col=0)
    y = pd.read_csv(y_file, index_col=0).squeeze()

    # Trace
    target_gene_name = os.path.basename(y_file).split('_')[1].split('.')[0]
    print("Computing gene", target_gene_name)

    # Match parameters with R's randomForest
    num_inputs = x.shape[1]
    mtry = round(math.sqrt(num_inputs))  # K == "sqrt"

    # Train the model

    # model = RandomForestRegressor(n_estimators=1000,
    #                               max_depth=None,           # default of R's randomForest 
    #                               max_features=mtry,        # K = "sqrt"
    #                               n_jobs=-1,                 # num.cores = 1
    #                               verbose=0,                # trace = True      
    #                               min_samples_split=5,      # nodesize=5 (default of R)
    #                               random_state=2020)

    model = GradientBoostingRegressor(n_estimators=10000,
                                      learning_rate=0.001, # 0.001 for 10k, 0.01 for 1k, 0.1 for 100
                                      max_features=mtry,
                                      verbose=1,
                                      max_depth=None,
                                      min_samples_split=5,
                                      random_state=2020)
    
    model.fit(x, y)

    # Get feature importances
    feature_importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': x.columns,
        'Importance': feature_importances
    })

    # Extract target gene name from the file name
    # target_gene_name = os.path.basename(y_file).split('_')[1].split('.')[0]
    # print(f"Feature Importances for {target_gene_name}:")
    # print(feature_importance_df)

    # Return the trained model and the feature importance DataFrame
    return model, feature_importance_df

def main():
    output_dir = "cluster_networks"
    os.makedirs(output_dir, exist_ok=True)

    # Find all hub files
    x_hub_files = [f for f in glob.glob("../x_y_csv_cluster/x_*.csv") if "_hub" in f]
    y_hub_files = [f for f in glob.glob("../x_y_csv_cluster/y_*.csv") if "_hub" in f]

    # Sort the files to ensure corresponding pairs (matching order)
    x_hub_files.sort()
    y_hub_files.sort()

    results = []

    # loop through all pairs of x and y files and train models
    for x_file, y_file in zip(x_hub_files, y_hub_files):

        model, feature_importance_df = train_model(x_file, y_file)

        results.append({
            'x_file': x_file,
            'y_file': y_file,
            'model': model,
            'feature_importance': feature_importance_df
        })
    
    # Write output file
    hub_network = pd.DataFrame()
    for result in results:
            y_file = result['y_file']
            feature_importance_df = result['feature_importance']
            
            # Extract target gene name from the file name to use as a column
            target_gene_name = os.path.basename(y_file).split('_')[1].split('.')[0]
            
            # Add the target gene name as a new column in the feature importance DataFrame
            feature_importance_df['Target Gene'] = target_gene_name
            
            # Append this DataFrame to the main DataFrame
            hub_network = pd.concat([hub_network, feature_importance_df], ignore_index=True)

    # Scale
    hub_network['Importance'] = (hub_network['Importance'] - hub_network['Importance'].min()) / (hub_network['Importance'].max() - hub_network['Importance'].min())

    # Filter rows where Importance >= threshold
    threshold = 0.8
    trimmed_network = hub_network[hub_network['Importance'] >= threshold]

    # Export
    output_file = os.path.join(output_dir, f"network_hub.csv")
    trimmed_network.to_csv(output_file, index=False)

if __name__ == '__main__':
    main()