import pandas as pd

# Load the Excel file
file_path = "./compression algorithms filtered.xlsx"
data = pd.ExcelFile(file_path)

# Load the first sheet and process it
df = data.parse('Sheet1')

# Rename columns for clarity
df.columns = [
    "Algorithm",
    "Compression Ratio",
    "Write Speed (MB/s)",
    "Write IOPS",
    "Read Speed (MB/s)",
    "Read IOPS",
    "Combined Speed (MB/s)",
    "Combined IOPS",
    "Random Compression Ratio",
    "Random Write Speed (MB/s)",
    "Random Write IOPS",
    "Random Read Speed (MB/s)",
    "Random Read IOPS",
    "Random Combined Speed (MB/s)",
    "Random Combined IOPS",
]

# Filter rows with actual algorithm data
df_filtered = df.iloc[1:].copy()

# Convert relevant columns to numeric
for col in [
    "Compression Ratio",
    "Random Compression Ratio",
    "Write Speed (MB/s)",
    "Read Speed (MB/s)",
    "Random Write Speed (MB/s)",
]:
    df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')

# Normalize Compression Ratio
df_filtered["Normalized Compression Ratio"] = (
    df_filtered["Compression Ratio"] / df_filtered["Compression Ratio"].max()
)

# Add an overall score (weighted focus on compression ratio, sequential and random IOPS)
weights = {
    "Compression Ratio": 0.65,
    "Sequential Write IOPS": 0.05,
    "Random Write IOPS": 0.05,
    "Sequential Read IOPS": 0.05,
    "Random Read IOPS": 0.20,
}

# Normalize the relevant IOPS columns
df_filtered["Normalized Sequential Write IOPS"] = (
    df_filtered["Write IOPS"] / df_filtered["Write IOPS"].max()
)
df_filtered["Normalized Random Write IOPS"] = (
    df_filtered["Random Write IOPS"] / df_filtered["Random Write IOPS"].max()
)
df_filtered["Normalized Sequential Read IOPS"] = (
    df_filtered["Read IOPS"] / df_filtered["Read IOPS"].max()
)
df_filtered["Normalized Random Read IOPS"] = (
    df_filtered["Random Read IOPS"] / df_filtered["Random Read IOPS"].max()
)

# Calculate the overall score
df_filtered["Score"] = (
    df_filtered["Normalized Compression Ratio"] * weights["Compression Ratio"]
    + df_filtered["Normalized Sequential Write IOPS"] * weights["Sequential Write IOPS"]
    + df_filtered["Normalized Random Write IOPS"] * weights["Random Write IOPS"]
    + df_filtered["Normalized Sequential Read IOPS"] * weights["Sequential Read IOPS"]
    + df_filtered["Normalized Random Read IOPS"] * weights["Random Read IOPS"]
)


# Sort algorithms by score
df_sorted = df_filtered.sort_values(by="Score", ascending=False)

# Print the top recommendations
print("Top Compression Algorithms:")
print(df_sorted[["Algorithm", "Compression Ratio", "Score"]].head(5))

# Save the results to a CSV file
df_sorted.to_csv("compression_algorithms_results.csv", index=False)
print("\nResults saved to 'compression_algorithms_results.csv'")
