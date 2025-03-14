def calculate_arrivals_departures(df):
    """
    Computes vessel arrivals and departures for each port using vectorized operations.
    Returns:
    --------
    Three DataFrames:
    - port_result_df (All vessel types)
    - car_df (Only Cargo vessels)
    - pas_df (Only Passenger vessels)
    """
    # only calculate once and store result
    global port_result_df, car_df, pas_df
    if port_result_df is not None and car_df is not None and pas_df is not None:
        return port_result_df, car_df, pas_df
    
    cargo_df = df[df["Vessel Type Name"] == "Cargo"]
    passenger_df = df[df["Vessel Type Name"] == "Passenger"]
    
    def compute_port_stats(filtered_df):
        # national flag
        port_flags = {
            "Port of Tacoma": "\U0001F1FA\U0001F1F8", #US
            "Port of Vancouver": "\U0001F1E8\U0001F1E6", #CA
            "Port of Long Beach": "\U0001F1FA\U0001F1F8",
            "Port of Los Angeles": "\U0001F1FA\U0001F1F8",
            "Port of San Francisco": "\U0001F1FA\U0001F1F8",
            "Port of Oakland": "\U0001F1FA\U0001F1F8",
            "Port of Seattle": "\U0001F1FA\U0001F1F8",
            "Port of Ensenada": "\U0001F1F2\U0001F1FD", #MX
            "Port of San Diego": "\U0001F1FA\U0001F1F8",
        }
        
        if filtered_df.empty:
            return pd.DataFrame(columns=["FLAG", "PORT NAME", "ARRIVALS", "DEPARTURES"])
        
        # Vectorized approach to detect arrivals and departures
        # Sort by MMSI and BaseDateTime
        sorted_df = filtered_df.sort_values(by=["MMSI", "BaseDateTime"]).reset_index(drop=True)
        
        # Get the previous port for each row
        sorted_df['prev_port'] = sorted_df['Nearest Port'].shift(1)
        sorted_df['prev_mmsi'] = sorted_df['MMSI'].shift(1)
        
        # A port departure happens when a vessel's previous port is different than current port
        # but the MMSI is the same (same vessel moved to a different port)
        departures = sorted_df[(sorted_df['prev_port'] != sorted_df['Nearest Port']) & 
                              (sorted_df['prev_mmsi'] == sorted_df['MMSI'])]
        
        # Count departures per port
        if not departures.empty:
            departure_counts = departures['prev_port'].value_counts().reset_index()
            departure_counts.columns = ['PORT NAME', 'DEPARTURES']
        else:
            departure_counts = pd.DataFrame(columns=['PORT NAME', 'DEPARTURES'])
        
        # Count arrivals per port
        if not departures.empty:
            arrival_counts = departures['Nearest Port'].value_counts().reset_index()
            arrival_counts.columns = ['PORT NAME', 'ARRIVALS']
        else:
            arrival_counts = pd.DataFrame(columns=['PORT NAME', 'ARRIVALS'])
            
        # Merge arrival and departure counts
        result = pd.merge(arrival_counts, departure_counts, on='PORT NAME', how='outer').fillna(0)
        
        # Add flags
        result['FLAG'] = result['PORT NAME'].map(lambda x: port_flags.get(x, "\U0001F3F3"))
        
        # Ensure integers for counts
        result['ARRIVALS'] = result['ARRIVALS'].astype(int)
        result['DEPARTURES'] = result['DEPARTURES'].astype(int)
        
        # Reorder columns and sort
        result = result[['FLAG', 'PORT NAME', 'ARRIVALS', 'DEPARTURES']]
        return result.sort_values(by="ARRIVALS", ascending=False)
    
    port_result_df = compute_port_stats(df)
    car_df = compute_port_stats(cargo_df)
    pas_df = compute_port_stats(passenger_df)
    
    return port_result_df, car_df, pas_df