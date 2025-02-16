# Redundancy Detection Script

This Python script identifies and groups potentially redundant datasets from a metadata CSV file. By comparing key attributes such as indicator name, geographic coverage, time range, units, and source, the script computes a redundancy score for each pair of datasets. Datasets scoring above a defined threshold are flagged as redundant, and clusters of similar datasets are then formed to help you decide which version to keep.

---

## Features

- **Indicator Similarity:** Uses fuzzy text matching to compare dataset titles/indicators.
- **Geographic Overlap:** Checks if datasets cover the same regions.
- **Time Range Overlap:** Computes the normalized overlap between dataset time spans.
- **Units & Source Matching:** Ensures consistency in measurement units and data sources.
- **Redundancy Scoring:** Combines these factors with configurable weights.
- **Clustering:** Groups similar datasets into clusters for easy review.

---

## Requirements

- Python 3.6 or higher
- [pandas](https://pandas.pydata.org/)
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)
- [python-Levenshtein](https://pypi.org/project/python-Levenshtein/)
- [networkx](https://networkx.org/)

Install the required packages using pip:

```bash
pip install pandas fuzzywuzzy python-Levenshtein networkx
```

---

## Input File

The script expects a CSV file (e.g., `hp_dataset_metadata.csv`) containing metadata for each dataset with at least the following columns:

- `id`: Unique identifier for each dataset.
- `indicator`: Dataset title or indicator name.
- `source`: The data provider or origin.
- `geographic_coverage`: Description of the geographic scope (e.g., "Global", "Country-specific").
- `time_start`: Start year of the dataset.
- `time_end`: End year of the dataset.
- `units`: Measurement units (e.g., "years", "scale 0-1").

---

## Usage

1. Place your CSV file (e.g., `hp_dataset_metadata.csv`) in the same directory as the script.
2. Run the script using Python:

   ```bash
   python redundancy_detection.py
   ```

3. The script will:
   - Compute a redundancy score for every pair of datasets.
   - Flag dataset pairs with a score above the set threshold (default is 0.8).
   - Build a graph and output clusters of redundant datasets.

The output will list redundant dataset pairs along with their scores and print clusters of datasets that are considered redundant.

---

## Script Overview

- **Helper Functions:**
  - `compute_time_overlap(start1, end1, start2, end2)`: Calculates normalized overlap between two time ranges.
  - `compare_datasets(row1, row2, weights)`: Computes a weighted redundancy score by comparing:
    - **Indicator Similarity:** Fuzzy matching of the `indicator` field.
    - **Geographic Overlap:** Direct comparison of `geographic_coverage`.
    - **Time Range Overlap:** Normalized overlap between `time_start` and `time_end`.
    - **Units & Source:** Checks for exact matches.

- **Redundancy Scoring:**
  - Weights for each attribute are configurable (default weights provided).
  - A threshold (default 0.8) is applied to flag redundant dataset pairs.

- **Clustering:**
  - Uses NetworkX to build a graph where nodes represent datasets.
  - Edges connect datasets that exceed the redundancy threshold.
  - Connected components (clusters) of the graph are output as groups of redundant datasets.

---

## Customization

- **Weights:** Adjust the weights in the `weights` dictionary to change the importance of each attribute.
- **Threshold:** Change the `threshold` variable to control sensitivity.
- **Input File:** Modify the file name in the script if your CSV file is named differently.

---

## License

This script is provided "as is" without warranty of any kind. Feel free to modify and use it as needed.

---

## Contact

For any questions or improvements, please contact Alan Ye/ zy221@georgetown.edu.

Happy coding!
