import pandas as pd

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
    base_pairs = set(zip(base_data['Feature'], base_data['Target Gene']))
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
    Find common pairs among top hits
    """
    files = [
    ('output/top_hits/10k/top_hits_python_rf.csv'),
    ('output/top_hits/10k/top_hits_python_gbt.csv')
    ]
    common = top_hits_common(files)
    print(common)

if __name__ == '__main__':
    main()