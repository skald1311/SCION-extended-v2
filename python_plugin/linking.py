import pandas as pd
import os

working_dir = "cluster_networks/"  # Replace with the correct path
os.chdir(working_dir)

network_data = pd.read_csv("network_hub.txt", sep="\t")

cluster_files = [f for f in os.listdir() if f.startswith("imList_cluster_") and f.endswith(".csv")]

importance_dict = {}

# Loop through each cluster file and update the dictionary
for cluster_file in cluster_files:
    cluster_data = pd.read_csv(cluster_file)
    # Iterate over each row and add Feature-Target Gene pair to the dictionary
    for _, row in cluster_data.iterrows():
        feature_target_pair = (row['Feature'], row['Target Gene'])
        importance_dict[feature_target_pair] = row['Importance']

# Scale
min_importance = min(importance_dict.values())
max_importance = max(importance_dict.values())
for key, val in importance_dict.items():
    importance_dict[key] = (val - min_importance) / (max_importance - min_importance)

network_hub = pd.read_csv('network_hub.txt', sep='\t')
for _, row in network_hub.iterrows():
    feature_target_pair = (row['Regulator'], row['Target'])
    # if the pair exists in the dictionary, update the Importance value with Weight
    if feature_target_pair in importance_dict:
        importance_dict[feature_target_pair] = row['Weight']
    else:
        # if the pair does not exist in the dictionary, add it with the Weight as the Importance
        importance_dict[feature_target_pair] = row['Weight']

final_data = pd.DataFrame(importance_dict.items(), columns=['Feature-Target Gene', 'Importance'])
final_data[['Feature', 'Target Gene']] = pd.DataFrame(final_data['Feature-Target Gene'].tolist(), index=final_data.index)
final_data.drop(columns=['Feature-Target Gene'], inplace=True)
final_data = final_data[['Feature', 'Importance', 'Target Gene']]
final_data.to_csv('final_combined_data.csv', index=False)