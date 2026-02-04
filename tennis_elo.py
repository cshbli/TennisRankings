import pandas as pd
from datetime import datetime, timedelta

def get_top_100_elo():
    # K-Factor and Baseline
    BASE_K_FACTOR = 32
    START_YEAR = 2017
    CURRENT_YEAR = 2026
    
    # Tournament weighting multipliers
    TOURNAMENT_WEIGHTS = {
        'G': 2.0,    # Grand Slams
        'F': 1.75,   # Tour Finals
        'M': 1.5,    # Masters 1000
        'A': 1.25,   # ATP 500
        'D': 1.0,    # ATP 250
    }
    
    # Define Data Sources (Local CSV files)
    sources = {y: f"{y}.csv" for y in range(START_YEAR, CURRENT_YEAR)}

    print("Step 1: Loading Match History (2017-2026)...")
    all_matches = []
    for year, filename in sources.items():
        try:
            df = pd.read_csv(filename)
            all_matches.append(df)
            print(f"  Loaded {year} data.")
        except: print(f"  Warning: Skipping {year} (file not found).")

    # Combine and Sort
    df_all = pd.concat(all_matches, ignore_index=True)
    df_all['tourney_date'] = pd.to_datetime(df_all['tourney_date'], format='%Y%m%d', errors='coerce')
    df_all = df_all.sort_values('tourney_date')

    # Generate all Mondays from 1/1/2021 to today
    start_date = pd.Timestamp('2021-01-01')
    end_date = pd.Timestamp.now()
    
    # Find first Monday on or after start_date
    current = start_date
    while current.dayofweek != 0:  # 0 = Monday
        current += timedelta(days=1)
    
    mondays = []
    while current <= end_date:
        mondays.append(current)
        current += timedelta(days=7)
    
    print(f"Step 2: Calculating Weekly Ratings for {len(mondays)} Mondays...")
    
    # Elo Engine with weekly snapshots
    elo_ratings = {}   # {player_id: rating}
    player_names = {}  # {player_id: name}
    player_last_match = {}  # {player_id: last_match_date}
    weekly_ratings = []  # List of {date, player_id, rating}
    
    monday_idx = 0
    next_monday = mondays[0] if mondays else None
    
    for _, match in df_all.iterrows():
        match_date = match['tourney_date']
        
        # Capture ratings for all passed Mondays
        while next_monday and match_date >= next_monday:
            # Record current ratings for this Monday
            for p_id, rating in elo_ratings.items():
                weekly_ratings.append({
                    'Date': next_monday,
                    'Player_ID': p_id,
                    'Player': player_names[p_id],
                    'Elo_Rating': int(round(rating))
                })
            
            monday_idx += 1
            next_monday = mondays[monday_idx] if monday_idx < len(mondays) else None
        
        # Process match
        w_id, l_id = match['winner_id'], match['loser_id']
        w_name, l_name = match['winner_name'], match['loser_name']
        tourney_level = match.get('tourney_level', 'D')  # Default to ATP 250 if missing
        
        # Store names for mapping later
        player_names[w_id] = w_name
        player_names[l_id] = l_name
        
        # Track last match date
        player_last_match[w_id] = match_date
        player_last_match[l_id] = match_date
        
        # Get Current Ratings or Default
        r_w = elo_ratings.get(w_id, 1500)
        r_l = elo_ratings.get(l_id, 1500)
        
        # Apply tournament weighting to K-factor
        weight = TOURNAMENT_WEIGHTS.get(tourney_level, 1.0)
        K_FACTOR = BASE_K_FACTOR * weight
        
        # Elo Formula
        exp_w = 1 / (1 + 10 ** ((r_l - r_w) / 400))
        shift = K_FACTOR * (1 - exp_w)
        
        elo_ratings[w_id] = r_w + shift
        elo_ratings[l_id] = r_l - shift
    
    # Capture final Monday if needed
    while next_monday and next_monday <= end_date:
        for p_id, rating in elo_ratings.items():
            weekly_ratings.append({
                'Date': next_monday,
                'Player_ID': p_id,
                'Player': player_names[p_id],
                'Elo_Rating': int(round(rating))
            })
        monday_idx += 1
        next_monday = mondays[monday_idx] if monday_idx < len(mondays) else None

    # Convert to DataFrame
    weekly_df = pd.DataFrame(weekly_ratings)
    
    # Filter players who have played since 1/1/2025
    cutoff_date = pd.Timestamp('2025-01-01')
    active_players = {p_id for p_id, last_date in player_last_match.items() if last_date >= cutoff_date}
    
    # Identify top 100 active players based on final ratings
    final_ratings = {p_id: rating for p_id, rating in elo_ratings.items() if p_id in active_players}
    top_100_ids = sorted(final_ratings.keys(), key=lambda x: final_ratings[x], reverse=True)[:100]
    
    # Filter weekly ratings to only top 100 players
    top_100_weekly = weekly_df[weekly_df['Player_ID'].isin(top_100_ids)].copy()
    
    # Pivot: One row per player, one column per date
    pivot_df = top_100_weekly.pivot(index=['Player_ID', 'Player'], columns='Date', values='Elo_Rating')
    
    # Convert all rating columns to nullable integers (keep NaN for weeks before player started)
    for col in pivot_df.columns:
        pivot_df[col] = pivot_df[col].astype('Int64')  # Use Int64 to support NaN
    
    # Reset index to make Player_ID and Player regular columns
    pivot_df = pivot_df.reset_index()
    
    # Add final rating column (rounded to integer)
    pivot_df['Final_Rating'] = pivot_df['Player_ID'].map(final_ratings).round().astype(int)
    
    # Sort by final rating (descending)
    pivot_df = pivot_df.sort_values('Final_Rating', ascending=False)
    
    # Reorder columns: Player info, Final_Rating, then all date columns
    date_columns = [col for col in pivot_df.columns if isinstance(col, pd.Timestamp)]
    date_columns.sort()  # Ensure chronological order
    column_order = ['Player_ID', 'Player', 'Final_Rating'] + date_columns
    pivot_df = pivot_df[column_order]
    
    # Format date columns as strings for better CSV readability
    pivot_df.columns = ['Player_ID', 'Player', 'Final_Rating'] + [col.strftime('%Y-%m-%d') for col in date_columns]
    
    # Step 3: Save to CSV
    pivot_df.to_csv("Top_100_Tennis_Elo_Weekly_2021_2026.csv", index=False)
    print(f"\nSUCCESS: 'Top_100_Tennis_Elo_Weekly_2021_2026.csv' has been created.")
    print(f"Total: {len(pivot_df)} active players (played since 1/1/2025) with {len(date_columns)} weekly ratings each")
    print(f"Sorted by current Elo rating (high to low), one row per player with all weekly history.")
    return pivot_df

if __name__ == "__main__":
    results = get_top_100_elo()
    print("\n--- Sample: First 20 Records ---")
    print(results.head(20))