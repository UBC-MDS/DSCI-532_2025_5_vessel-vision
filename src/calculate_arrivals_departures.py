import pandas as pd

# calculate departures and arrivals
def calculate_arrivals_departures(df):
     
    """
    Computes the number of vessel arrivals and departures for each port.
    Based on MMSI and BaseDateTime, identifies when a vessel's nearest port change within its all records,
    which means it moves from one port to another, and counts the number of arrivals and departures for each port. 
    Also assigns the corresponding national flag emoji to each port.

    Parameters:
    -----------
    df : pd.DataFrame
        A DataFrame contains following columns:
        - "MMSI": Unique vessel identifier.
        - "BaseDateTime": Timestamp of the vessel's recorded position.
        - "Nearest Port": The port nearest to the vessel at the recorded timestamp.

    Returns:
    --------
    pd.DataFrame
        A DataFrame contains following columns:
        - "FLAG": Emoji of the port's country.
        - "PORT NAME": Name of the port.
        - "ARRIVALS": Number of vessels that arrived at the port.
        - "DEPARTURES": Number of vessels that departed from the port.
    """
    
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

    # sort by MMSI and BaseDateTime
    df = df.sort_values(by=["MMSI", "BaseDateTime"])

    port_stats = {}

    # calculate arrival & departure
    prev_port = None
    prev_mmsi = None

    for index, row in df.iterrows():
        current_port = row["Nearest Port"]
        mmsi = row["MMSI"]

        if mmsi != prev_mmsi:
            prev_mmsi = mmsi
            prev_port = current_port
            continue

        if current_port != prev_port:
            # departure from old port +1
            if prev_port in port_stats:
                port_stats[prev_port]["departures"] += 1
            else:
                port_stats[prev_port] = {"arrivals": 0, "departures": 1}

            # arrival in new port +1
            if current_port in port_stats:
                port_stats[current_port]["arrivals"] += 1
            else:
                port_stats[current_port] = {"arrivals": 1, "departures": 0}

        prev_port = current_port

    # For filtered data, if no arrivals or departures, return blank table
    if not port_stats:
        return pd.DataFrame(columns=["FLAG", "PORT NAME", "ARRIVALS", "DEPARTURES"])

    result_df = pd.DataFrame([
        {
            "FLAG": port_flags.get(port, "\U0001F3F3"), 
            "PORT NAME": port,
            "ARRIVALS": stats["arrivals"],
            "DEPARTURES": stats["departures"],
        }
        for port, stats in port_stats.items()
    ])


    result_df = result_df.sort_values(by="ARRIVALS", ascending=False)

    return result_df
