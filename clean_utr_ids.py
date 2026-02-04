import pandas as pd

# Read the CSV file
df = pd.read_csv('ATP_Players_UTR_IDs_2026-02-04.csv')

# Convert UTR_ID to integer (removes .0) and handle NaN values
df['UTR_ID'] = df['UTR_ID'].apply(lambda x: int(x) if pd.notna(x) else '')

# Remove UTR_Name column
# df = df.drop(columns=['UTR_Name'])

# Save back to CSV with specific formatting to avoid .0
df.to_csv('ATP_Players_UTR_IDs_2026-02-04.csv', index=False)

print("✓ File updated successfully!")
print(f"  - Removed '.0' from UTR_ID column")
print(f"  - Removed UTR_Name column")
print(f"\nUpdated columns: {list(df.columns)}")
print(f"\nSample (first 5 rows):")
print(df.head().to_string(index=False))
