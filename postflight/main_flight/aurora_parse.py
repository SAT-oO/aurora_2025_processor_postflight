
import pandas as pd


# file path for canard cmd and encoder data
file_path = "postflight/main_flight/aurora-flight-phase-parsley.txt"
   
# parse by message type
state_est = {"time": [], "state_id": [], "data": []} # state est data
mcb_encoder = {"time": [], "data": []} # mcb encoder
proc_cmd = {"time": [], "data": []} # proc board state est cmd 

# timestamp processing
proc_flight_time = 0.0
proc_prev_time = 0.0
mcb_flight_time = 0.0
mcb_prev_time = 0.0

proc_cycle = 0
mcb_cycle = 0

def corr_time(raw_time, board = ""):
    if board == "proc":
        global proc_flight_time
        global proc_prev_time

        global proc_cycle 

        if raw_time < proc_prev_time:
            proc_cycle = proc_cycle + 1
            
        
        proc_flight_time = raw_time + (proc_cycle * 65535)
        proc_prev_time = raw_time

        return proc_flight_time
    
    elif board == "mcb":
        global mcb_flight_time
        global mcb_prev_time

        global mcb_cycle 

        if raw_time < mcb_prev_time:
            mcb_cycle = mcb_cycle + 1
            
        
        mcb_flight_time = raw_time + (mcb_cycle * 65535)
        mcb_prev_time = raw_time

        return mcb_flight_time
    else:
        return raw_time
        

    

# parse data line by line with text strips to separate columns
with open(file_path, "r") as file:
    all_lines = file.readlines()
    

    for each_ln in all_lines:
        ln = each_ln.split() # removes the newline character

        # change timestamp to match flight time before parsing
        if len(ln) <= 7 or ln[6] != "time:":
            continue
        raw_time = float(ln[7]) * 1000.0 # convert to ms
        
        # print(each_ln)


        if ln[2] == "ACTUATOR_ANALOG_CMD": # proc board cmd
            flight_time = corr_time(raw_time, "proc")

            proc_cmd["time"].append(flight_time)
            proc_cmd["data"].append(float(ln[11]))
            # proc_cmds.append("time": flight_time, "data": ln[8])

        elif ln[9] == "SENSOR_CANARD_ENCODER_1": # mcb encoder
            flight_time = corr_time(raw_time, "mcb")

            mcb_encoder["time"].append(flight_time)
            mcb_encoder["data"].append(float(ln[11]))
            # mcb_encoder.append("time": flight_time, "data": ln[11])

        
        elif ln[2] == "STATE_EST_DATA": # state est data
            # update timestamp
            flight_time = corr_time(raw_time, "proc")

            state_est["time"].append(flight_time)
            state_est["state_id"].append(ln[9])
            state_est["data"].append(float(ln[11]))
            # state_est_cmd.append("time": flight_time, "data": ln[11])

    # convert lists to dataframes
        

    # write each list into different sheets of the same csv file
    output_file_path = "postflight/main_flight/aurora_flight_data.xlsx"

    with pd.ExcelWriter(output_file_path) as writer:
        # writer = csv.writer(output_file)
        
        # write proc board cmds
        df = pd.DataFrame(proc_cmd)
        df.columns = ["time_ms", "data"]
        df.to_excel(writer, sheet_name='proc_cmd', index=False)

        # write mcb encoder
        df = pd.DataFrame(mcb_encoder)
        df.columns = ["time_ms", "data"]
        df.to_excel(writer, sheet_name='mcb_encoder', index=False)

        # write state est cmd
        df = pd.DataFrame(state_est)
        df.columns = ["time_ms", "state_id", "data"]
        df.to_excel(writer, sheet_name='state_est_data', index=False)