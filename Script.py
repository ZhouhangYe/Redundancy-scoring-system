import pandas as pd
from fuzzywuzzy import fuzz
import networkx as nx

# Load the dataset metadata from CSV
df = pd.read_csv("hp_dataset_metadata.csv")

# --- Helper Functions ---

def compute_time_overlap(start1, end1, start2, end2):
    """
    Compute normalized overlap between two time ranges.
    Returns a ratio between 0 and 1.
    """
    overlap = max(0, min(end1, end2) - max(start1, start2))
    avg_duration = ((end1 - start1) + (end2 - start2)) / 2.0
    return overlap / avg_duration if avg_duration > 0 else 0

def compare_datasets(row1, row2, weights):
    """
    Calculate a redundancy score for two datasets by comparing key attributes.
    
    - Indicator Similarity: Fuzzy text matching on the 'indicator' field.
    - Geographic Overlap: 1 if geographic coverage is identical; else 0.
    - Time Range Overlap: Normalized overlap of the time ranges.
    - Units: 1 if units match exactly; else 0.
    - Source: 1 if sources are identical; else 0.
    
    The overall score is a weighted sum of these comparisons.
    """
    # Indicator similarity using fuzzy matching (0 to 1 scale)
    indicator_similarity = fuzz.token_set_ratio(row1["indicator"], row2["indicator"]) / 100.0
    
    # Geographic overlap: 1 if exactly the same, else 0.
    geo_similarity = 1.0 if row1["geographic_coverage"] == row2["geographic_coverage"] else 0.0
    
    # Time range overlap (normalized)
    time_overlap = compute_time_overlap(row1["time_start"], row1["time_end"],
                                        row2["time_start"], row2["time_end"])
    
    # Units similarity: 1 if units match exactly, else 0.
    unit_similarity = 1.0 if row1["units"] == row2["units"] else 0.0
    
    # Source similarity: 1 if the same source, else 0.
    source_similarity = 1.0 if row1["source"] == row2["source"] else 0.0
    
    # Weighted score calculation (weights sum to 1.0)
    score = (indicator_similarity * weights["indicator"] +
             geo_similarity * weights["geo"] +
             time_overlap * weights["time"] +
             unit_similarity * weights["unit"] +
             source_similarity * weights["source"])
    
    return score

# --- Parameters and Weights ---

# Weights for each attribute (sum should equal 1.0)
weights = {
    "indicator": 0.35,   # Emphasize indicator/title similarity
    "geo": 0.2,          # Geographic coverage
    "time": 0.25,        # Time range overlap
    "unit": 0.1,         # Units consistency
    "source": 0.1        # Source similarity
}

# Similarity threshold above which datasets are flagged as redundant.
threshold = 0.8

# --- Identify Redundant Pairs ---

redundant_pairs = []
n = len(df)

for i in range(n):
    for j in range(i + 1, n):
        score = compare_datasets(df.iloc[i], df.iloc[j], weights)
        if score >= threshold:
            redundant_pairs.append((df.iloc[i]["id"], df.iloc[j]["id"], score))

print("Redundant dataset pairs (score >= {:.1f}):".format(threshold))
for pair in redundant_pairs:
    print("Dataset {} and Dataset {} with score: {:.2f}".format(pair[0], pair[1], pair[2]))

# --- Group Redundant Datasets into Clusters ---

# Build a graph where nodes are dataset IDs and an edge indicates redundancy.
G = nx.Graph()
G.add_nodes_from(df["id"].tolist())
for d1, d2, score in redundant_pairs:
    G.add_edge(d1, d2)

# Extract connected components as clusters.
clusters = list(nx.connected_components(G))

print("\nRedundant dataset clusters:")
for cluster in clusters:
    if len(cluster) > 1:
        print("Cluster:", cluster)
