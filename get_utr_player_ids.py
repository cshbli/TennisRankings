import pandas as pd
import requests
import time
from datetime import datetime

# Headers (no cookie required)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.utrsports.net/'
}

# API Endpoint
SEARCH_API = "https://api.utrsports.net/v2/search"

def search_utr_player_id(player_name):
    """
    Search for a player and get their UTR ID
    """
    try:
        params = {
            'schoolClubSearch': 'false',
            'query': player_name,
            'top': 1,
            'skip': 0
        }
        
        response = requests.get(
            SEARCH_API,
            params=params,
            headers=HEADERS,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for results in the correct structure (players.hits)
            if 'players' in data and 'hits' in data['players'] and len(data['players']['hits']) > 0:
                player = data['players']['hits'][0]
                source = player.get('source', {})
                
                return {
                    'utr_id': source.get('id') or player.get('id'),
                    'utr_name': source.get('displayName'),
                    'utr_rating': source.get('singlesUtr')
                }
        
        return None
        
    except Exception as e:
        print(f"  Error: {e}")
        return None

def test_single_player():
    """
    Test the API with a single player (Carlos Alcaraz)
    """
    test_player = "Carlos Alcaraz"
    
    print(f"Testing API with: {test_player}")
    print("="*60)
    
    player_data = search_utr_player_id(test_player)
    
    if player_data and player_data.get('utr_id'):
        print("✓ SUCCESS! API is working")
        print(f"Player: {player_data.get('utr_name', '')}")
        print(f"UTR ID: {player_data.get('utr_id')}")
        print(f"UTR Rating: {player_data.get('utr_rating', 'N/A')}")
        print("="*60)
        return True
    else:
        print("✗ FAILED! Unable to fetch data")
        print("="*60)
        print("\nPossible issues:")
        print("1. API may require authentication")
        print("2. Network connection issue")
        print("3. API endpoint may have changed")
        return False

def get_utr_ids_for_atp_players():
    """
    Read ATP rankings and fetch UTR player IDs for all players
    """
    print("Loading ATP Top 200 Rankings...")
    
    # Read ATP rankings
    df = pd.read_csv('ATP_Top_200_Rankings.csv')
    
    print(f"Found {len(df)} ATP players")
    print("\nFetching UTR Player IDs...\n")
    
    results = []
    
    for idx, row in df.iterrows():
        rank = row['Rank']
        player_name = row['Player']
        
        print(f"[{idx+1}/{len(df)}] {player_name} (ATP #{rank})...", end=' ')
        
        # Search for player
        player_data = search_utr_player_id(player_name)
        
        if player_data and player_data.get('utr_id'):
            utr_id = player_data.get('utr_id')
            utr_name = player_data.get('utr_name', '')
            utr_rating = player_data.get('utr_rating', 'N/A')
            
            print(f"✓ ID: {utr_id}, UTR: {utr_rating}")
            
            results.append({
                'ATP_Rank': rank,
                'Player_Name': player_name,
                'UTR_ID': utr_id,
                'UTR_Name': utr_name,
                'UTR_Rating': utr_rating
            })
        else:
            print("✗ Not found")
            results.append({
                'ATP_Rank': rank,
                'Player_Name': player_name,
                'UTR_ID': None,
                'UTR_Name': '',
                'UTR_Rating': 'N/A'
            })
        
        # Delay to avoid rate limiting
        time.sleep(0.5)
    
    # Create DataFrame
    result_df = pd.DataFrame(results)
    
    # Save to CSV
    current_date = datetime.now().strftime('%Y-%m-%d')
    output_file = f'ATP_Players_UTR_IDs_{current_date}.csv'
    result_df.to_csv(output_file, index=False)
    
    print(f"\n{'='*60}")
    print(f"✓ SUCCESS: '{output_file}' has been created.")
    print(f"{'='*60}")
    
    # Statistics
    found_count = len(result_df[result_df['UTR_ID'].notna()])
    print(f"\nUTR IDs found: {found_count}/{len(df)} players ({found_count*100//len(df)}%)")
    
    return result_df

if __name__ == "__main__":
    print("="*60)
    print("ATP Players - UTR ID Fetcher")
    print("="*60 + "\n")
    
    # Test with single player first
    print("Step 1: Testing API with Carlos Alcaraz...\n")
    if not test_single_player():
        print("\n⚠️  API test failed. Please check configuration.")
        exit(1)
    
    # Ask user to continue
    print("\nAPI test successful!")
    response = input("\nContinue to fetch all 200 players? (y/n): ")
    
    if response.lower() != 'y':
        print("Cancelled by user.")
        exit(0)
    
    print("\n" + "="*60)
    print("Step 2: Fetching all ATP Top 200 players...")
    print("="*60 + "\n")
    
    results = get_utr_ids_for_atp_players()
    
    print("\n--- Sample: Top 20 Players ---")
    print(results.head(20).to_string(index=False))
