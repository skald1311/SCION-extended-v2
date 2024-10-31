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

def main():
    files = [
    ('output/raw_weight/original_no_threshold/orf 10000.txt', 'txt'),
    ('output/raw_weight/python_rf/rf 10000.csv', 'csv'),
    ('output/raw_weight/gbt/gbt 10000.csv', 'csv'),
    ('output/raw_weight/original_no_threshold/orf 1000.txt', 'txt'),
    ('output/raw_weight/python_rf/rf 1000.csv', 'csv'),
    ('output/raw_weight/gbt/gbt 1000.csv', 'csv'),
    ('output/raw_weight/original_no_threshold/orf 100.txt', 'txt'),
    ('output/raw_weight/python_rf/rf 100.csv', 'csv'),
    ('output/raw_weight/gbt/gbt 100.csv', 'csv')
    ]

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

if __name__ == '__main__':
    main()