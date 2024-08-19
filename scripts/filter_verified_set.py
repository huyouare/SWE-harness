import pandas as pd

# Load the merged dataset
df = pd.read_csv("data/swe-bench-verified_merged.csv")

# Filter the dataset
filtered_df = df[
    (df["underspecified"] == 0)
    & (df["false_negative"] == 0)
    & (df["other_major_issues"] == 0)
    & (df["difficulty"] == "<15 min fix")
]

# Remove columns with notes
columns_to_remove = ["underspecified_notes", "false_negative_notes", "other_notes"]
filtered_df = filtered_df.drop(columns=columns_to_remove, errors="ignore")

# Write the filtered dataset to a new CSV file
filtered_df.to_csv("data/swe-bench-verified_filtered.csv", index=False)

print(f"Filtered dataset saved to data/swe-bench-verified_filtered.csv")
print(f"Number of rows in filtered dataset: {len(filtered_df)}")

# Calculate and display the distribution across repos
repo_distribution = filtered_df["repo"].value_counts()
print("\nDistribution across repos:")
print(repo_distribution)
