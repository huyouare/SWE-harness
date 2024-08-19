import pandas as pd

# Load the datasets
file1_path = "data/ensembled_annotations_public.csv"
file2_path = "data/swe-bench-verified.csv"

# Read the CSV files
df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

# Display the first few rows and columns of each dataset to understand their structure
df1_head = df1.head()
df2_head = df2.head()
df1_info = df1.info()
df2_info = df2.info()

# Columns to ignore during merge
ignore_columns = [
    "underspecified_decided_by",
    "false_negative_decided_by",
    "other_major_issues_decided_by",
    "difficulty_decided_by",
    "difficulty_ensemble_decision_procedure",
]

# Perform the join operation on the common key 'instance_id', excluding specified columns
merged_df = pd.merge(
    df1.drop(columns=ignore_columns, errors="ignore"),
    df2,
    on="instance_id",
    how="inner",
)

# Display the first few rows of the merged dataset
print("\nMerged Dataset Head:")
print(merged_df.head())

# Save the merged dataset to a new CSV file
merged_file_path = "data/swe-bench-verified_merged.csv"
merged_df.to_csv(merged_file_path, index=False)
print(f"\nMerged dataset saved to {merged_file_path}")
