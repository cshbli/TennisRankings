import csv

# Read the txt file and convert to CSV
input_file = 'WTA_Top_200_Rankings.txt'
output_file = 'WTA_Top_200_Rankings.csv'

# Open output CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header
    writer.writerow(['Rank', 'Player'])
    
    # Read and process each line from txt file
    with open(input_file, 'r', encoding='utf-8') as txtfile:
        for line in txtfile:
            # Split by tab
            parts = line.strip().split('\t')
            
            if len(parts) >= 2:
                rank = parts[0]
                player_name = parts[1]
                
                # Write to CSV
                writer.writerow([rank, player_name])

print(f"✓ Converted {input_file} to {output_file}")
print(f"  Format: Rank, Player")
