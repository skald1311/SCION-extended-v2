import pandas as pd

# def apply_threshold(input_file, output_file, threshold):
#     """
#     Apply the threshold to filter rows based on the Importance column.

#     Parameters:
#     input_file (str): Path to the input CSV file.
#     threshold (float): Threshold value to filter the Importance column.

#     Returns:
#     None
#     """
#     data = pd.read_csv(input_file)
    
#     # Filter rows where Importance >= threshold
#     filtered_data = data[data['Importance'] >= threshold]
    
#     # Save the filtered DataFrame back to a CSV
#     filtered_data.to_csv(output_file, index=False)
#     print(f"Filtered data saved to {output_file}")

def apply_threshold(input_file, output_file, threshold):
    """
    Apply the threshold to filter rows based on the Weight column.

    Parameters:
    input_file (str): Path to the input TXT file.
    output_file (str): Path to the output CSV file.
    threshold (float): Threshold value to filter the Weight column.

    Returns:
    None
    """
    # Read the tab-separated file
    data = pd.read_csv(input_file, sep='\t')
    
    # Filter rows where Weight >= threshold
    filtered_data = data[data['Weight'] >= threshold]
    
    # Save the filtered DataFrame back to a CSV
    filtered_data.to_csv(output_file, index=False)
    print(f"Filtered data saved to {output_file}")

def main():
    input_file = "cluster_networks/python rf runs/10000/network_hub.txt"
    output_file = "hub_comparison/rf_08.csv"
    threshold = 0.8

    apply_threshold(input_file, output_file, threshold)

if __name__ == '__main__':
    main()