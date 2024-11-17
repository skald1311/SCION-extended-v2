import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def find_common_pairs(files):
    # Initialize a set for common pairs
    common_pairs = None

    for file_path, file_type in files:
        # Read pairs from the current file
        pairs = set()
        # print(file_path)
        if file_type == 'txt':
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split('\t')
                    if len(parts) >= 3:
                        pair = f"{parts[0]}-{parts[2]}"
                        pairs.add(pair)
                        
        elif file_type == 'csv':
            df = pd.read_csv(file_path, header=None)
            for _, row in df.iterrows():
                if len(row) >= 3:
                    pair = f"{row[0]}-{row[2]}"
                    pairs.add(pair)
        # print(len(pairs))
        # print("-------------------------")
        # Initialize common_pairs with pairs from the first file
        if common_pairs is None:
            common_pairs = pairs
        else:
            # Find the intersection of pairs across files
            common_pairs &= pairs

    # Output the common pairs
    # print("Common pairs across all files:")
    # print(common_pairs)
    # print(len(common_pairs))
    return common_pairs

def build_common_heatmap(files):
    common_pairs = find_common_pairs(files)

    # Initialization
    # Format: {"AT4G36730-AT1G07010": [0.21, 0.30, 0.18]}
    pair_values = {}
    for pair in common_pairs:
        pair_values[pair] = []
        
    for file_path, file_type in files:
        file_pairs = {}
        # Read the file and gather values for each pair
        if file_type == 'txt':
            with open(file_path, 'r') as file:
                next(file)
                for line in file:
                    parts = line.strip().split('\t')
                    if len(parts) >= 4:
                        pair = f"{parts[0]}-{parts[2]}"
                        value = float(parts[3])
                        if pair in common_pairs:
                            file_pairs[pair] = value 
        elif file_type == 'csv':
            df = pd.read_csv(file_path, header=0)
            for _, row in df.iterrows():
                if len(row) >= 3:
                    pair = f"{row.iloc[0]}-{row.iloc[2]}"
                    value = float(row.iloc[1])
                    if pair in common_pairs:
                        file_pairs[pair] = value
        # Append values to each common pair in pair_values
        for pair in common_pairs:
            pair_values[pair].append(file_pairs.get(pair, None))
    # print pair_values
    # for key, val in pair_values.items():
    #     print(key, ": ", val)
    
    pair_df = pd.DataFrame.from_dict(pair_values, orient='index', columns=[os.path.splitext(os.path.basename(file[0]))[0] for file in files])

    # pair_df.to_csv("output/heatmap/pair_values.csv", index=True)

    correlation_matrix = pair_df.corr()
    plt.figure(figsize=(12, 8))

    # for correlation matrix:
    # sns.heatmap(correlation_matrix, annot=True, cmap='cividis', vmin=-1, vmax=1)

    # for pairs matrix
    sns.heatmap(pair_df, annot=False, cmap='cividis', vmin=0, vmax=1)
    plt.title("Heatmap")
    plt.xlabel("Models and Size")
    plt.ylabel("Regulatory Pairs")
    plt.yticks(fontsize=10)
    plt.xticks(fontsize=10)
    plt.tight_layout()
    plt.show()

def find_all_pairs(files):
    all_pairs = set()

    for file_path, file_type in files:
        if file_type == 'txt':
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split('\t')
                    if len(parts) >= 3:
                        pair = f"{parts[0]}-{parts[2]}"
                        all_pairs.add(pair)
                        
        elif file_type == 'csv':
            df = pd.read_csv(file_path, header=None)
            for _, row in df.iterrows():
                if len(row) >= 3:
                    pair = f"{row[0]}-{row[2]}"
                    all_pairs.add(pair)

    return all_pairs

def build_all_heatmap(files):
    all_pairs = find_all_pairs(files)

    pair_values = {pair: [0] * len(files) for pair in all_pairs}
    
    for file_idx, (file_path, file_type) in enumerate(files):
        file_pairs = {}
        if file_type == 'txt':
            with open(file_path, 'r') as file:
                next(file)
                for line in file:
                    parts = line.strip().split('\t')
                    if len(parts) >= 4:
                        pair = f"{parts[0]}-{parts[2]}"
                        value = float(parts[3])
                        file_pairs[pair] = value 
        elif file_type == 'csv':
            df = pd.read_csv(file_path, header=0)
            for _, row in df.iterrows():
                if len(row) >= 3:
                    pair = f"{row.iloc[0]}-{row.iloc[2]}"
                    value = float(row.iloc[1])
                    file_pairs[pair] = value
        # update values for each pair in pair_values
        for pair in all_pairs:
            if pair in file_pairs:
                pair_values[pair][file_idx] = file_pairs[pair]
    
    # create DataFrame
    pair_df = pd.DataFrame.from_dict(
        pair_values, 
        orient='index', 
        columns=[os.path.splitext(os.path.basename(file[0]))[0] for file in files]
    )

    # pair_df.to_csv("output/heatmap/all-threshold/pair_values.csv", index=True)

    # for correlation matrix:
    correlation_matrix = pair_df.corr()

    # make heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='cividis', vmin=-1, vmax=1)
    #sns.heatmap(pair_df, annot=False, cmap='cividis', vmin=0, vmax=1)
    plt.xlabel("Models and Size")
    plt.ylabel("Regulatory Pairs")
    plt.yticks(fontsize=10)
    plt.xticks(fontsize=10)
    plt.tight_layout()
    # plt.savefig(os.path.dirname("output/heatmap/all-threshold/all_pairs_corr_heatmap.png"), dpi=300)
    plt.show()

def main():
    files = [
    ('output/raw_weight/threshold/original/original_rf_10000.txt', 'txt'),
    ('output/raw_weight/threshold/python_rf/threshold_rf_10000.csv', 'csv'),
    ('output/raw_weight/threshold/gbt/threshold_gbt_10000.csv', 'csv'),

    ('output/raw_weight/threshold/original/original_rf_1000.txt', 'txt'),
    ('output/raw_weight/threshold/python_rf/threshold_rf_1000.csv', 'csv'),
    ('output/raw_weight/threshold/gbt/threshold_gbt_1000.csv', 'csv'),

    ('output/raw_weight/threshold/original/original_rf_100.txt', 'txt'),
    ('output/raw_weight/threshold/python_rf/threshold_rf_100.csv', 'csv'),
    ('output/raw_weight/threshold/gbt/threshold_gbt_100.csv', 'csv')
    ]

    build_all_heatmap(files)

if __name__ == '__main__':
    main()