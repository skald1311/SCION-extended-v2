import pandas as pd

def find_top_pairs_text_file(txt_file_path, top_n=25):
    data = pd.read_csv(txt_file_path, sep="\t")
    
    # sort by Weight column
    sorted_data = data.sort_values(by="Weight", ascending=False)
    
    # select the top N rows
    top_pairs = sorted_data.head(top_n)
    
    return top_pairs

def find_top_pairs_csv_file(csv_file, top_n=25):
    data = pd.read_csv(csv_file)
    
    # sort by Importance column
    sorted_data = data.sort_values(by="Importance", ascending=False)
    
    # select the top N rows
    top_pairs = sorted_data.head(top_n)
    
    return top_pairs

def top_hits_common(files):
    """
    Compares the base list in 'top_hits_original.csv' with the other two files
    to find how many and which pairs are common.

    Parameters:
        files (list): List of file paths where the first file is the base list, 
                      and the remaining files are compared against it.

    Returns:
        dict: A dictionary containing the counts and details of common pairs for each file.
    """
    # Read the base list (top_hits_original.csv)
    base_file = files[0]
    base_data = pd.read_csv(base_file)
    base_pairs = set(zip(base_data['Regulator'], base_data['Target']))
    #print(base_pairs)
    results = {}
    for compare_file in files[1:]:
        compare_data = pd.read_csv(compare_file)
        compare_pairs = set(zip(compare_data['Feature'], compare_data['Target Gene']))
        #print(compare_pairs)

        # find common pairs
        common_pairs = base_pairs & compare_pairs

        results[compare_file] = {
            'common_count': len(common_pairs),
            'common_pairs': list(common_pairs)
        }

    return results

def main():
    """
    TXT: Output 25 top pairs of .txt file
    """
    # file_path = "output/raw_weight/threshold/original/original_rf_10000.txt"

    # # Find the top 25 highest weight pairs
    # top_pairs = find_top_pairs_text_file(file_path, top_n=25)
    # output_file = "top_hits_original.csv"
    # top_pairs.to_csv(output_file, index=False)
    # print(f"Top 25 pairs saved to {output_file}")

    """
    CSV: Output 25 top pairs of .csv file
    """
    # csv_file = "output/raw_weight/threshold/gbt/threshold_gbt_10000.csv"
    # top_pairs = find_top_pairs_csv_file(csv_file, top_n=25)
    # output_file = "top_hits_python_gbt.csv"
    # top_pairs.to_csv(output_file, index=False)
    # print(f"Top 25 pairs saved to {output_file}")

    """
    Find common pairs among top hits
    """
    files = [
    ('output/top_hits/10k/top_hits_original.csv'),  # keep original pipeline top hits in 1st position
    ('output/top_hits/10k/top_hits_python_rf.csv'),
    ('output/top_hits/10k/top_hits_python_gbt.csv')
    ]
    common = top_hits_common(files)
    print(common)

if __name__ == '__main__':
    main()