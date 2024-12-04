import pandas as pd
import json
import unittest


# Function to load weights from JSON file
def load_weights(filepath="weights.json"):
    try:
        with open(filepath, "r") as file:
            weights = json.load(file)
        return weights
    except FileNotFoundError:
        raise FileNotFoundError(f"Cannot find the weights file: {filepath}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in weights file: {filepath}")

    # Dynamically identify numeric columns and normalize them
def process_data(file_path, weights):
    # Load the Excel file
    with pd.ExcelFile(file_path) as data:
        df = data.parse("Sheet1")

    # Rename columns for clarity (update names if necessary)
    df.columns = [
        "Algorithm",
        "Sequential Compression Ratio",
        "Sequential Write Transfer Speed (MB/s)",
        "Sequential Write IOPS",
        "Sequential Read Transfer Speed (MB/s)",
        "Sequential Read IOPS",
        "Sequential Read/Write Transfer Speed (MB/s)",
        "Sequential Read/Write IOPS",
        "Random Compression Ratio",
        "Random Write Transfer Speed (MB/s)",
        "Random Write IOPS",
        "Random Read Transfer Speed (MB/s)",
        "Random Read IOPS",
        "Random Read/Write Transfer Speed (MB/s)",
        "Random Read/Write IOPS",
    ]


    # Filter rows with actual algorithm data
    df_filtered = df.iloc[1:].copy()

    # Convert all columns except "Algorithm" to numeric, handling non-numeric entries
    for col in df_filtered.columns:
        if col != "Algorithm":
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors="coerce")

    # Normalize all columns that have weights assigned
    for metric in weights.keys():
        column_name = metric
        if column_name in df_filtered.columns:
            max_value = df_filtered[column_name].max()
            if max_value > 0:  # Avoid division by zero
                df_filtered[f"Normalized {metric}"] = df_filtered[column_name] / max_value
            else:
                logging.warning("Column '{column_name}' has no valid values for normalization.")
        else:
            logging.warning("Column '{column_name}' not found in the dataset.")

    # Filter weights to only include metrics present in the DataFrame
    valid_metrics = {
        metric: weight
        for metric, weight in weights.items()
        if f"Normalized {metric}" in df_filtered.columns
    }

    # Calculate the overall score
    df_filtered["Score"] = sum(
        df_filtered[f"Normalized {metric}"] * weight
        for metric, weight in valid_metrics.items()
    )

    # Sort algorithms by score
    df_sorted = df_filtered.sort_values(by="Score", ascending=False)

    return df_sorted


# Unit tests
class TestCompressionComparison(unittest.TestCase):
    def test_weights_loading(self):
        weights = load_weights("weights.json")
        # Check for all expected keys
        expected_keys = [
            "Sequential Compression Ratio",
            "Sequential Write Transfer Speed (MB/s)",
            "Sequential Write IOPS",
            "Sequential Read Transfer Speed (MB/s)",
            "Sequential Read IOPS",
            "Sequential Read/Write Transfer Speed (MB/s)",
            "Sequential Read/Write IOPS",
            "Random Compression Ratio",
            "Random Write Transfer Speed (MB/s)",
            "Random Write IOPS",
            "Random Read Transfer Speed (MB/s)",
            "Random Read IOPS",
            "Random Read/Write Transfer Speed (MB/s)",
            "Random Read/Write IOPS"
        ]

        for key in expected_keys:
            self.assertIn(key, weights, f"Missing key in weights: {key}")

    def test_weights_values(self):
        weights = load_weights("weights.json")
        # Ensure weights are numeric
        for key, value in weights.items():
            self.assertIsInstance(
                value, (int, float),
                f"Weight for {key} is not numeric: {value}"
            )

    def test_process_data_custom_weights(self):
        # Test if process_data works with a fully customized weights.json
        weights = load_weights("weights.json")
        df_sorted = process_data("compression algorithms filtered.xlsx", weights)
        # Verify the output contains expected columns
        self.assertIn("Algorithm", df_sorted.columns)
        self.assertIn("Score", df_sorted.columns)
        self.assertGreater(df_sorted["Score"].iloc[0], 0)


    def test_process_data_scores(self):
        weights = load_weights("weights.json")
        df_sorted = process_data("compression algorithms filtered.xlsx", weights)
        scores = df_sorted["Score"].tolist()
        self.assertEqual(sorted(scores, reverse=True), scores)  # Ensure sorted order



if __name__ == "__main__":
    # Load weights
    weights = load_weights("weights.json")

    # Process data and calculate scores
    file_path = "compression algorithms filtered.xlsx"
    try:
        df_sorted = process_data(file_path, weights)

        # Print top recommendations
        print("Top Compression Algorithms:")
        print(df_sorted[["Algorithm", "Sequential Compression Ratio", "Random Compression Ratio", "Score"]].head(5))

        # Save results to a CSV file
        df_sorted.to_csv("compression_algorithms_results.csv", index=False)
        print("\nResults saved to 'compression_algorithms_results.csv'")

    except Exception as e:
        print(f"Error: {e}")

    # Run unit tests
    print("\nRunning unit tests...\n")
    unittest.main(exit=False)
