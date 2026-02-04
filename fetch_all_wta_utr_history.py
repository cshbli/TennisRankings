import pandas as pd
import requests
import time
from datetime import datetime

# ===== CONFIGURATION =====
# Cookie from browser (provided by user)
COOKIE_STRING = "_gcl_aw=GCL.1770162282.CjwKCAiA1obMBhAbEiwAsUBbIvsSuOIF_mnWmtZVfw3xzvPPCsJ5YYOX_UJs3xEetnUrHYG60Nb-gBoCpMIQAvD_BwE; _gcl_dc=GCL.1770162282.CjwKCAiA1obMBhAbEiwAsUBbIvsSuOIF_mnWmtZVfw3xzvPPCsJ5YYOX_UJs3xEetnUrHYG60Nb-gBoCpMIQAvD_BwE; _gcl_gs=2.1.k1$i1770162281$u255840972; _gcl_au=1.1.937439040.1770162282; cebs=1; _ga=GA1.1.1711657992.1770162282; _ce.clock_data=0%2C73.194.7.128%2C1%2C684fac3d8e595845640e507a9122bd55%2CChrome%2CUS; cebsp_=1; _fbp=fb.1.1770162282358.828206736591854654; sharedid=8704e877-8f8f-4fb4-a5f6-195f0a5bc32f; sharedid_cst=zix7LPQsHA%3D%3D; _au_1d=AU1D-0100-001770162283-TL083BFT-0LMF; _cc_id=b523c349ca311ae897577886ec69d47f; panoramaId=eda3ea64504b6e2bee7d0decd85e16d53938c0d7d409637d55e9f96a630c1e58; panoramaId_expiry=1770767083154; panoramaIdType=panoIndiv; connectId={\"ttl\":86400000,\"lastUsed\":1770162283635,\"lastSynced\":1770162283635}; _ce.s=v~cda4e0a5794a2b8a3ee1d25b171164f559ee1c5b~lcw~1770162295987~vir~new~lva~1770162282027~vpv~0~v11.cs~468890~v11.s~4fd612b0-015a-11f1-945d-6503c230f5df~v11.vs~cda4e0a5794a2b8a3ee1d25b171164f559ee1c5b~v11.fsvd~eyJ1cmwiOiJ1dHJzcG9ydHMubmV0L3BhZ2VzL3Rlbm5pcy1uZWFyLW1lIiwicmVmIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJ1dG0iOlsiYWR3b3JkcyIsInBwYyIsIiIsIiIsIlRlbm5pcy1CcmFuZC1QTWF4Il19~v11.sla~1770162282332~v11.ws~1~v11.wr~22~v11.ss~1770162282334~v11ls~4fd612b0-015a-11f1-945d-6503c230f5df~vdva~1770163199999~gtrk.la~ml78xd4j~v11e~1~v11nv~0~lcw~1770162296136; _ga_VV8MC4HMJ0=GS2.1.s1770162282$o1$g1$t1770162296$j46$l0$h0; _ga_FVWZ0RM4DH=GS2.1.s1770162296$o1$g0$t1770162296$j60$l0$h0; _ga_0B4P6MG9VT=GS2.1.s1770162282$o1$g1$t1770162297$j45$l0$h0; ajs_anonymous_id=499ea746-c5b4-4478-a32f-4edf51692d77; _ga_6CHSZXCWB1=GS2.1.s1770162288$o1$g1$t1770162299$j49$l0$h0; OptanonAlertBoxClosed=2026-02-03T23:44:59.636Z; cto_bundle=JIHPVF9PUHZZdHJ6JTJCaHp0a2xVbXJpdVd6Wmt6Tmt0bFhranFqc3BxSlIwS21mdyUyRlI0dWtsYyUyRld4Ulp2aiUyQm1IWDkxUTB4M0ZkMnNmWHFSRDU0dVlZSnZEY1RLaU1Obm5YMXFZNWdGWEw5djRUJTJCdjRIUnptV3dMbDRyT2JnTkFIdTZYejloVGN1cHZkNzQ1VEprZVlRa0N2Wjg4SkZpV0tqamVFMFBlNzFGeHR4bm45anVzY3ZXcFZsTXAzWmE1Q3VHRTlH; jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNZW1iZXJJZCI6IjE3ODM4IiwiZW1haWwiOiJjc2hibGlAaG90bWFpbC5jb20iLCJWZXJzaW9uIjoiMSIsIkRldmljZUxvZ2luSWQiOiIyNzU2MzI2MyIsImFtciI6WyJwd2QiXSwibmJmIjoxNzcwMTYyNTM2LCJleHAiOjE3NzI3NTQ1MzYsImlhdCI6MTc3MDE2MjUzNn0.GzvzzjW-azYKb5KZir3RFSbWg6rkGzuzT4qN43sRw48; ut_user_info=SubscriptionType%3DFree%26MemberId%3D17838%26Email%3Dcshbli%40hotmail.com; ajs_user_id=17838; ab.storage.sessionId.39f28a45-a4c7-4fec-a1de-56fa1fed9ba6=g%3Ae8b7cdc8-a792-5df1-28a9-bccc4a103d89%7Ce%3A1770164336647%7Cc%3A1770162536647%7Cl%3A1770162536647; ab.storage.userId.39f28a45-a4c7-4fec-a1de-56fa1fed9ba6=g%3A17838%7Ce%3Aundefined%7Cc%3A1770162536646%7Cl%3A1770162536648; ab.storage.deviceId.39f28a45-a4c7-4fec-a1de-56fa1fed9ba6=g%3A63ff3c83-7c47-fccb-d88d-aa8092dafd55%7Ce%3Aundefined%7Cc%3A1770162536649%7Cl%3A1770162536649; _clck=1jjqzr9%5E2%5Eg3a%5E0%5E2225; _clsk=c1do5h%5E1770169566059%5E1%5E1%5Ei.clarity.ms%2Fcollect; __gads=ID=16d52b567a4e5395:T=1770162299:RT=1770169569:S=ALNI_MbeAv0SN0tZmu5KIUTy4CfbW7yC8w; __gpi=UID=00001342cbf9eb63:T=1770162299:RT=1770169569:S=ALNI_MZobSgtJj6h-nZorIXw1NOBE6RFwA; __eoi=ID=1b39b07ba121ebf7:T=1770162299:RT=1770169569:S=AA-AfjbqAKmseU8xXXdeZvYSwUh3; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Feb+03+2026+20%3A46%3A14+GMT-0500+(Eastern+Standard+Time)&version=202406.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=54b67c67-7c44-45da-b01e-3709ba4d988d&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0002%3A0%2CC0001%3A1%2CC0004%3A0%2CC0003%3A0&AwaitingReconsent=false&intType=3&geolocation=US%3BNY"

# Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.utrsports.net/',
    'Cookie': COOKIE_STRING
}

# API Endpoints
PLAYER_STATS_API = "https://api.utrsports.net/v4/player/{player_id}/all-stats"

# Input and output files
INPUT_CSV = "WTA_Players_UTR_IDs_2026-02-04.csv"
OUTPUT_CSV = "WTA_Top_200_UTR_History_2021_2026.csv"

def get_player_stats(player_id):
    """
    Fetch player stats including UTR rating history
    """
    try:
        url = PLAYER_STATS_API.format(player_id=player_id)
        
        params = {
            'type': 'singles',
            'resultType': 'verified',
            'months': 12,
            'fetchAllResults': False
        }
        
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ✗ Stats Status: {response.status_code}")
        
        return None
        
    except Exception as e:
        print(f"  ✗ Stats Error: {e}")
        return None

def parse_rating_history(stats_data, player_id, player_name, wta_rank):
    """
    Extract and format rating history from stats response
    Returns a dict with player info and all ratings
    """
    # Extract history from nested structure
    history = stats_data.get('extendedRatingProfile', {}).get('history', [])
    
    if not history:
        print(f"    No history data found")
        return None
    
    # Filter for dates from 1/1/2021 onwards
    cutoff_date = datetime(2021, 1, 1)
    
    filtered_history = []
    for record in history:
        date_str = record.get('date', '')
        try:
            record_date = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
            
            if record_date >= cutoff_date:
                filtered_history.append({
                    'Date': record_date.strftime('%Y-%m-%d'),
                    'Rating': record.get('rating')
                })
        except:
            continue
    
    if not filtered_history:
        print(f"    No history records from 1/1/2021 onwards")
        return None
    
    # Sort by date (oldest to newest for consistent ordering)
    filtered_history.sort(key=lambda x: x['Date'])
    
    # Create single row format: player info + dates as columns
    row_data = {
        'WTA_Rank': wta_rank,
        'Player_Name': player_name,
        'UTR_ID': player_id
    }
    
    for item in filtered_history:
        row_data[item['Date']] = item['Rating']
    
    return row_data

def fetch_all_utr_histories():
    """
    Main function to fetch UTR history for all WTA Top 200 players
    """
    print("="*80)
    print("Fetching UTR History for WTA Top 200 Players")
    print("="*80 + "\n")
    
    # Read the input CSV with UTR IDs
    print(f"Reading player list from: {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV)
    print(f"✓ Loaded {len(df)} players\n")
    
    # Store all player histories
    all_histories = []
    success_count = 0
    fail_count = 0
    
    # Process each player
    for idx, row in df.iterrows():
        wta_rank = row['WTA_Rank']
        player_name = row['Player_Name']
        utr_id = row['UTR_ID']
        
        # Handle UTR_ID as either int or float
        try:
            utr_id = int(float(utr_id))
        except:
            print(f"[{idx+1}/200] Rank {wta_rank}: {player_name} - Invalid UTR ID")
            fail_count += 1
            continue
        
        print(f"[{idx+1}/200] Rank {wta_rank}: {player_name} (UTR ID: {utr_id})")
        
        # Fetch player stats
        stats = get_player_stats(utr_id)
        
        if stats:
            # Parse rating history
            history_data = parse_rating_history(stats, utr_id, player_name, wta_rank)
            
            if history_data:
                all_histories.append(history_data)
                print(f"  ✓ Success - {len([k for k in history_data.keys() if k not in ['WTA_Rank', 'Player_Name', 'UTR_ID']])} rating records")
                success_count += 1
            else:
                print(f"  ✗ No history data")
                fail_count += 1
        else:
            print(f"  ✗ Failed to fetch stats")
            fail_count += 1
        
        # Rate limiting - wait 0.5 seconds between requests
        time.sleep(0.5)
    
    print("\n" + "="*80)
    print(f"Completed: {success_count} successful, {fail_count} failed")
    print("="*80 + "\n")
    
    if all_histories:
        # Convert to DataFrame
        # Use pd.DataFrame.from_dict to handle varying columns
        result_df = pd.DataFrame(all_histories)
        
        # Sort columns: WTA_Rank, Player_Name, UTR_ID, then dates in chronological order
        fixed_cols = ['WTA_Rank', 'Player_Name', 'UTR_ID']
        date_cols = sorted([col for col in result_df.columns if col not in fixed_cols])
        result_df = result_df[fixed_cols + date_cols]
        
        # Save to CSV
        result_df.to_csv(OUTPUT_CSV, index=False)
        
        print(f"✓ Saved combined history to: {OUTPUT_CSV}")
        print(f"  Total players: {len(result_df)}")
        print(f"  Total columns: {len(result_df.columns)}")
        print(f"  Date range: {date_cols[0]} to {date_cols[-1]}")
        print(f"  Total date columns: {len(date_cols)}")
        
        # Show sample
        print("\n--- Sample: First 5 Players, First 8 Columns ---")
        print(result_df.iloc[:5, :min(8, len(result_df.columns))].to_string(index=False))
        
        return result_df
    else:
        print("✗ No data retrieved")
        return None

if __name__ == "__main__":
    results = fetch_all_utr_histories()
