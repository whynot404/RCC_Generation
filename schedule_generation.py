#!/usr/bin/env python3

import time
import calendar
import pandas as pd
import re
from pathlib import Path
from math import ceil



MAX_EXPORT_LIMIT =  99_998 #99_998  # Maximum number of rows recommended for export
SCHEDULE_FILE_NAME = "sample_sched.xlsx"  # Default schedule file name
BASE_PATH = Path(__file__).parent  # Base path of the current script
OUTPUT_FOLDER = BASE_PATH / 'Output'
OUTPUT_FOLDER.mkdir(exist_ok=True)


# Export data
def export_data(df: pd.DataFrame, file_name: str) -> list[Path]:
    
    len_df = len(df)
    start = time.perf_counter()
    output_files =[]
   
    if not file_name.lower().endswith(".csv"):
        file_name += ".csv"

    if len_df > MAX_EXPORT_LIMIT:
    
        #export_files = (len_df // MAX_EXPORT_LIMIT) + 1 
        export_files = ceil(len_df / MAX_EXPORT_LIMIT)
        stem = Path(file_name).stem

        for i in range(export_files):
            start_index = i * MAX_EXPORT_LIMIT
            end_index = min((i + 1) * MAX_EXPORT_LIMIT, len_df)
            output_path = OUTPUT_FOLDER / f"{stem}_part_{i+1}.csv"
            
            df.iloc[start_index:end_index].to_csv(output_path, index=False)
            output_files.append(output_path)

    else:
        # if number of rows is less than the maximum export limit
        output_path = OUTPUT_FOLDER / file_name
        df.to_csv(output_path, index=False)
        output_files.append(output_path)
     
    end = time.perf_counter() 
    print(f"Total Time : {end - start:.4f} seconds")
    return output_files

# Load data from consolidated RSR
def new_load_data(file_location)->pd.DataFrame:
   return pd.read_excel(file_location)
   
def new_generate_schedule(tempfile:str,month:int, year:int,start_day:int,output_file:str)->list[Path]:
    
    SCHEDULE_MAIN_LIST_SET = set()
    df = new_load_data(tempfile)
    unique_count =  df.iloc[:, 0].nunique()
    STORE_LIST = df.values.tolist()

    last_day = calendar.monthrange(year, month)[1]

    if start_day < 1 or start_day > last_day:
        raise ValueError(
            f"Invalid start day. Please enter a value between 1 and {last_day}."
        )
    for s_name in STORE_LIST:

            # Service Days (e.g. Mon/Wed/Fri)
            if pd.isna(s_name[2]):
                continue
        
            service_days = re.sub(r"[-,]","/", str(s_name[2)).split("/") # correction if there's incorrect slices
        
            for week in calendar.monthcalendar(year, month):
                for day in week:

                    if day == 0:
                        continue

                    # Skip dates before the selected start day
                    if day < start_day:
                        continue

                    day_name = calendar.day_abbr[
                        calendar.weekday(year, month, day)
                    ]

                    if day_name in service_days:

                        schedule = (
                            s_name[0],
                            s_name[1],
                            f"{year:04d}{month:02d}{day:02d}"
                        )
                    
                        SCHEDULE_MAIN_LIST_SET.add(schedule)

    dfload = pd.DataFrame(list(SCHEDULE_MAIN_LIST_SET),
                      columns=[
                          "STORE_ID",
                          "STORE_NAME",
                          "SERVICE_DAY"
                      ]
                      ).sort_values(by=["STORE_ID,SERVICE_DAY"], ascending=[True,True])

    output_files_stats =  export_data(dfload,output_file)

    return {"output_files": output_files_stats,
    "unique_store_count": unique_count,
    "total_schedule_rows": len(dfload)
    }
        

