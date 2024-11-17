import pandas as pd

def apply_threshold(input_file, output_file, threshold):
    """
    Apply the threshold to filter rows based on the Importance column.

    Parameters:
    input_file (str): Path to the input CSV file.
    threshold (float): Threshold value to filter the Importance column.

    Returns:
    None
    """
    data = pd.read_csv(input_file)
    
    # Filter rows where Importance >= threshold
    filtered_data = data[data['Importance'] >= threshold]
    
    # Save the filtered DataFrame back to a CSV
    filtered_data.to_csv(output_file, index=False)
    print(f"Filtered data saved to {output_file}")

def main():
    input_file = "output/raw_weight/no_threshold/gbt/final_gbt_100.csv"
    output_file = "output/raw_weight/threshold/gbt/threshold_gbt_100.csv"
    threshold = 0.33

    apply_threshold(input_file, output_file, threshold)

if __name__ == '__main__':
    main()