import csv
import pandas as pd


# file path for canard cmd and encoder data
file_path = "postflight/canard_cmd_and_encoder_data/canard-commands-and-encoder.txt"



def output_xlsx():     
    # parse by message type
    proc_cmd = {"time": [], "data": []} # proc board cmd
    mcb_encoder = {"time": [], "data": []} # mcb encoder
    state_est_cmd = {"time": [], "data": []} # proc board state est cmd 

    # parse data line by line with text strips to separate columns
    with open(file_path, "r") as file:
        all_lines = file.readlines()
        
        flight_time = 0.0 # launch time in sec 
        prev_time = 0.0 # previous timestamp in sec


        for each_ln in all_lines:
            ln = each_ln.split() # removes the newline character

            # change timestamp to match flight time before parsing
            
            raw_time = float(ln[7]) 
            if raw_time > prev_time:
                flight_time = flight_time + (raw_time - prev_time)
                prev_time = raw_time
            else:
                prev_time = raw_time
                flight_time = flight_time + (65535 - prev_time) + raw_time # account for rollover
               

    
    
            if ln[2] == "ACTUATOR_ANALOG_CMD": # proc board cmd
                proc_cmd["time"].append(flight_time)
                proc_cmd["data"].append(float(ln[11]))
                # proc_cmds.append("time": flight_time, "data": ln[8])

            elif ln[2] == "SENSOR_ANALOG": # mcb encoder
                mcb_encoder["time"].append(flight_time)
                mcb_encoder["data"].append(float(ln[11]))
                # mcb_encoder.append("time": flight_time, "data": ln[11])

            
            elif ln[2] == "STATE_EST_DATA": # proc board state est cmd
                state_est_cmd["time"].append(flight_time)
                state_est_cmd["data"].append(float(ln[11]))
                # state_est_cmd.append("time": flight_time, "data": ln[11])

        # write each list into different sheets of the same csv file
        output_file_path = "postflight/canard_cmd_and_encoder_data/xlsx_output/canard_cmd_and_encoder_data.xlsx"

        with pd.ExcelWriter(output_file_path) as writer:
            # writer = csv.writer(output_file)
            
            # write proc board cmds
            df = pd.DataFrame(proc_cmd)
            df.to_excel(writer, sheet_name='proc_cmd', index=False)

            # write mcb encoder
            df = pd.DataFrame(mcb_encoder)
            df.to_excel(writer, sheet_name='mcb_encoder', index=False)

            # write state est cmd
            df = pd.DataFrame(state_est_cmd)
            df.to_excel(writer, sheet_name='state_est_cmd', index=False)
    
def output_csv():

    proc_cmds = []
    mcb_encoder = []
    state_est_cmd = []

    # parse data line by line with text strips to separate columns
    with open(file_path, "r") as file:
        all_lines = file.readlines()
        
        flight_time = 0.0 # launch time in sec 
        prev_time = 0.0 # previous timestamp in sec


        for each_ln in all_lines:
            ln = each_ln.split() # removes the newline character

            # change timestamp to match flight time before parsing
            
            raw_time = float(ln[7]) 
            if raw_time > prev_time:
                flight_time = flight_time + (raw_time - prev_time)
                prev_time = raw_time
            else:
                prev_time = raw_time
                flight_time = flight_time + (65535 - prev_time) + raw_time # account for rollover
                

    

            if ln[2] == "ACTUATOR_ANALOG_CMD": # proc board cmd
                    
                proc_cmds.append([flight_time, ln[11]])

            elif ln[2] == "SENSOR_ANALOG": # mcb encoder
                
                mcb_encoder.append([flight_time, ln[11]])

            
            elif ln[2] == "STATE_EST_DATA": # proc board state est cmd
                
                state_est_cmd.append([flight_time, ln[11]])

            

        # output to csv file
        output_file_path_csv = "postflight/canard_cmd_and_encoder_data/csv_output/proc_cmd.csv"
        with open(output_file_path_csv, mode = "w", newline = "") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["time", "data"])
            writer.writerows(proc_cmds)
            

        output_file_path_csv = "postflight/canard_cmd_and_encoder_data/csv_output/mcb_encoder.csv"
        with open(output_file_path_csv, mode = "w", newline = "") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["time", "data"])
            writer.writerows(mcb_encoder)
            
        
        output_file_path_csv = "postflight/canard_cmd_and_encoder_data/csv_output/state_est_cmd.csv"
        with open(output_file_path_csv, mode = "w", newline = "") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["time", "data"])
            writer.writerows(state_est_cmd)


if __name__ == "__main__":
    output_xlsx()
    output_csv()
        
    

        
        
        
        
        
        



