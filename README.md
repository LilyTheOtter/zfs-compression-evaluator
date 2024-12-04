# zfs-compression-evaluator
## What This program does
The `zfs-compression-evaluator` script evaluates and compares different compression algorithms based on their performance metrics. It uses data from a provided Excel file containing details about various compression algorithms, such as compression ratios, read/write speeds, and IOPS. The program calculates an overall score for each algorithm, considering the weights for various metrics like compression ratio, sequential read/write IOPS, and random read/write IOPS. The results are then displayed and saved to a CSV file, making it easy to identify the best compression algorithms for your use case.

## Requirements
- Python 3.x
- Required Python packages:
    - `pandas`
    - `json`
    - `unittest`
    - `openpyxl`

These can be installed using `pip`:
```bash
pip install pandas openpyxl
```
## Installation

1. Clone the repository or download the script files.

    ```bash
    git clone https://github.com/LilyTheOtter/zfs-compression-evaluator
    ```

2. Install required Python dependencies.

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure that you have the necessary input files:
    - `compression algorithms filtered.xlsx`: The input Excel file containing the compression algorithms data.
    - `weights.json`: The JSON file containing the weights for scoring.

## Usage

1. Ensure that the required files are in place:
    - `compression algorithms filtered.xlsx`: This file should contain the compression algorithms data.
    - `weights.json`: This file contains the weights that will be used to calculate the scores. If you don’t have this file, refer to the example `weights.json` structure provided in the installation section.

2. Modify the `weights.json` file if necessary to reflect your preferred weightings for the compression metrics (such as sequential and random read/write speeds and compression ratios).

3. To run the script and calculate the compression scores, execute the following command:

    ```bash
    python3 compression_comparison.py
    ```

4. The script will process the data and print the top compression algorithms along with their scores.

5. The results will be saved as a CSV file (`compression_algorithms_results.csv`) in the same directory as the script. You can open this CSV file for further analysis or use it for reporting purposes.

## Example

The script will print the top compression algorithms based on their scores. For example:

```text
Top Compression Algorithms:
   Algorithm  Sequential Compression Ratio  Random Compression Ratio     Score
34   zstd-19                          3.66                      1.98  0.921568
33   zstd-18                          3.65                      1.98  0.917809
30   zstd-15                          3.47                      1.98  0.915996
27   zstd-12                          3.43                      1.98  0.915025
22    zstd-7                          3.35                      1.98  0.913821

Results saved to 'compression_algorithms_results.csv'

Running unit tests...

....
----------------------------------------------------------------------
Ran 4 tests in 0.035s

OK
```
The results will be saved in a CSV file named `compression_algorithms_results.csv` in the same directory as the script. You can open this CSV file to view the complete list of compression algorithms, their respective compression ratios, and calculated scores.

The weights file used in the example:
```json
{
	"Sequential Compression Ratio": 0.3,
	"Sequential Write Transfer Speed (MB/s)": 0,
	"Sequential Write IOPS": 0,
	"Sequential Read Transfer Speed (MB/s)": 0,
	"Sequential Read IOPS": 0.1,
	"Sequential Read/Write Transfer Speed (MB/s)": 0,
	"Sequential Read/Write IOPS": 0,
	"Random Compression Ratio": 0.35,
	"Random Write Transfer Speed (MB/s)": 0,
	"Random Write IOPS": 0,
	"Random Read Transfer Speed (MB/s)": 0,
	"Random Read IOPS": 0.25,
	"Random Read/Write Transfer Speed (MB/s)": 0,
	"Random Read/Write IOPS": 0
}
```
