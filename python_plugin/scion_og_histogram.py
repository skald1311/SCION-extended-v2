import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("FINAL_NETWORK.txt", sep='\t')

# Create a histogram of the 'Importance' column
plt.figure(figsize=(8,6))
plt.hist(df['Weight'], bins=10, edgecolor='black')

plt.xlabel('Edge Weight')
plt.ylabel('Frequency')
plt.title('Histogram of Edge Weight')  # Feature Importance == Edge weight

plt.savefig("hist_og_scion_rf_100.png", dpi=300)  # You can adjust dpi for resolution
plt.show()