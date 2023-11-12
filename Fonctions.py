import pandas as pd
import numpy as np
import os 

os.system("cls")
def Safety_car(df):
    """Extracts intervals from a DataFrame and adds +1 to the second couple if the two elements are equal.

    Args:
        df: A DataFrame containing the data to extract intervals from.

    Returns:
        A list of intervals, where each interval is a tuple of (start, end).
    """

    # Initialize the list of intervals
    intervals = []

    # Iterate over the rows in the DataFrame
    for i in range(len(df)):

        # Check if the current row is the start of a new interval
        if i == 0 or df.iloc[i, 0] != df.iloc[i - 1, 0] + 1:

            # Add the new interval to the list
            intervals.append([df.iloc[i, 0],df.iloc[i, 0]])

        # Update the end of the current interval
        intervals[-1] = (intervals[-1][0], df.iloc[i, 0])

    # Loop over the intervals and check if the couples of intervals need +1 for the second couple
    for i in range(len(intervals)):
        if intervals[i][0] == intervals[i][1]:
            # Convert the interval tuple to a list
            interval_list = list(intervals[i])

            # Update the value of the second element in the list
            interval_list[1] = interval_list[1] + 1

            # Convert the list back to a tuple
            intervals[i] = tuple(interval_list)

    return intervals

def CalculateDeltaTime(Telemetry, Telemetry_ref):

    """
    Calculates the delta times for a given lap, relative to a reference lap.

    Args:
    Telemetry: Telemetry data for the lap to calculate the delta times for.
    Telemetry_ref: Telemetry data for the reference lap.

    Returns:
    Delta_time: array of delta time.
    Distance: array of distance.
    
    """
    # # Add attribute TimeS to the dataframe
    Telemetry["TimeS"] = Telemetry["Time"].dt.total_seconds()
    Telemetry_ref["TimeS"] = Telemetry_ref["Time"].dt.total_seconds()

    # # Stretch or contract the distances across all the data objects so that the total
    # # distance of the lap matches the fastest (reference) lap in the selection.
    Telemetry["Distance"] = Telemetry["Distance"] * (Telemetry_ref.iloc[-1]["Distance"] / Telemetry.iloc[-1]["Distance"])
    # Use linear interpolation to align each data object with the data objects in
    # the fastest lap.

    interp_lap_data = np.interp(Telemetry["Distance"], Telemetry_ref["Distance"],Telemetry_ref["TimeS"])
    # Return the difference in time at each instance.
    Delta_time =  interp_lap_data.tolist() - Telemetry["TimeS"]
    Distance = Telemetry["Distance"]

    return Delta_time, Distance

def SectorDistance(laps):
    
    """
    This function calculates the distance of each sector
    
    args:
        laps (fastf1.core.Laps): laps of the driver

    returns:
        sector_distance (list): list of the distance of each sector
    """
    sector_time = []
    sector_distance = []
    lap = laps.pick_fastest()
    for i in range(3):
        sector_time.append(lap["Sector"+str(i+1)+"Time"])
    for i in range(2):
        sector_time[i+1] = sector_time[i] + sector_time[i+1]
    lap_telemetry = lap.get_telemetry()
    sector_distance.append(lap_telemetry.loc[lap_telemetry["Time"] <= sector_time[0],"Distance"].max())
    sector_distance.append(lap_telemetry.loc[lap_telemetry["Time"] <= sector_time[1],"Distance"].max())
    sector_distance.append(lap_telemetry["Distance"].max())
    return sector_distance
    
def SectorLocation(laps):
    """
    This function calculates the location of each sector

    args:
        laps (fastf1.core.Laps): laps of the driver

    returns:
        sector_location (list): list of the location of each sector
    """
    sector_location = [[],[]]
    sector_distance = SectorDistance(laps)
    comp = laps.pick_fastest().get_telemetry()
    comp = comp [["X","Y","Distance"]]
    for i in sector_distance:
        Sec = comp
        Sec["MinDis"] = (Sec["Distance"] - i).abs()
        sec_loc = Sec.loc[Sec["MinDis"]==Sec["MinDis"].min(),["X","Y"]].values[0]
        sector_location[0].append(sec_loc[0]) # Append X
        sector_location[1].append(sec_loc[1]) # Append Y
    return sector_location

def GapSector(laps_driver1, laps_driver2, lap = None):
    
    """
    This function calculates the gap between two drivers in each sector

    args:
        laps_driver1 (fastf1.core.Laps): laps of the first driver
        laps_driver2 (fastf1.core.Laps): laps of the second driver
        lap (int): lap number, if not specified the fastest lap will be used
    """

    if lap == None:
        laps_driver1 = laps_driver1.pick_fastest()
        laps_driver2 = laps_driver2.pick_fastest()
        laps_driver1["S1"] = laps_driver1["Sector1Time"].total_seconds()
        laps_driver1["S2"] = laps_driver1["Sector2Time"].total_seconds()
        laps_driver1["S3"] = laps_driver1["Sector3Time"].total_seconds()
        laps_driver2["S1"] = laps_driver2["Sector1Time"].total_seconds()
        laps_driver2["S2"] = laps_driver2["Sector2Time"].total_seconds()
        laps_driver2["S3"] = laps_driver2["Sector3Time"].total_seconds()
        comparaison = laps_driver2[["S1","S2","S3"]].reset_index(drop=True) - laps_driver1[["S1","S2","S3"]].reset_index(drop=True)
        comparaison = comparaison.values
    else:
        laps_driver1 = laps_driver1.pick_lap(lap)
        laps_driver2 = laps_driver2.pick_lap(lap)
        laps_driver1["S1"] = laps_driver1["Sector1Time"].dt.total_seconds()
        laps_driver1["S2"] = laps_driver1["Sector2Time"].dt.total_seconds()
        laps_driver1["S3"] = laps_driver1["Sector3Time"].dt.total_seconds()
        laps_driver2["S1"] = laps_driver2["Sector1Time"].dt.total_seconds()
        laps_driver2["S2"] = laps_driver2["Sector2Time"].dt.total_seconds()
        laps_driver2["S3"] = laps_driver2["Sector3Time"].dt.total_seconds()
        comparaison = laps_driver2[["S1","S2","S3"]].reset_index(drop=True) - laps_driver1[["S1","S2","S3"]].reset_index(drop=True)
        comparaison = comparaison.values[0]
       
    return comparaison

def CompoundColorDf():
    return pd.DataFrame.from_dict(
        {
            1: ['HARD','#F0F0EC'], 
            2:['INTERMEDIATE', '#43B02A'], 
            3:['MEDIUM','#FFD12E'], 
            4:['SOFT', '#DA291C'], 
            5:['TEST_UNKNOWN', '#434649'], 
            6:['UNKNOWN','#00FFFF'], 
            7:['WET', '#0067AD']
        },
        orient='index',
        columns=['Compound', 'CompoundColor']
    )

print('Done')