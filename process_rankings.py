import pandas as pd
import re

def process_rankings_txt():
    """
    Process rankings.txt file and extract rank and player name
    """
    print("Processing rankings.txt file...")
    
    with open('rankings.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    rankings = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Check if line is a rank number (pure digits, possibly with tab)
        if re.match(r'^\d+\t*$', line):
            current_rank = line.replace('\t', '').strip()
            i += 1
            
            # Check if next line is rank change (could be number, +number, -number)
            if i < len(lines):
                next_line = lines[i].strip()
                # If next line is a single number or +/-number, it's rank change - skip it
                if re.match(r'^[+\-]?\d+\t*$', next_line):
                    i += 1
            
            # Now get the player name (should be the next line with letters)
            if i < len(lines):
                player_line = lines[i].strip()
                # Check if this is a player name (has letters, not just numbers/symbols)
                if player_line and re.search(r'[A-Za-z]', player_line) and not re.match(r'^[\d\s\t,+\-]+$', player_line):
                    rankings.append({
                        'Rank': current_rank,
                        'Player': player_line
                    })
        
        i += 1
    
    # Create DataFrame
    df = pd.DataFrame(rankings)
    
    # Remove duplicates and keep top 200
    df = df.drop_duplicates(subset=['Player']).head(200)
    
    # Save to CSV
    output_file = 'ATP_Top_200_Rankings.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\nSUCCESS: '{output_file}' has been created.")
    print(f"Total players: {len(df)}")
    
    return df

if __name__ == "__main__":
    rankings = process_rankings_txt()
    print("\n--- Top 20 ATP Players ---")
    print(rankings.head(20).to_string(index=False))
