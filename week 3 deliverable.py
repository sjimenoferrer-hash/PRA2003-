"""
Week 3 Deliverable
-------------------
Reads a file containing ~500K events, selects the molecules of interest
based on their ID code, and computes the average number of that molecule 
per event, together with the statistical uncertainty.
"""

import math # needed for the uncertainty

UNPHYSICAL_VALUE = -1  # used when an uncertainty can't be calculated (it can never really be negative)

# Molecule IDs and names
molecules = {
    211: "Carbon monoxide",
    -211: "Carbon-13 monoxide",
    321: "Nitric oxide",
    -321: "Ionised NO",
    2212: "Water",
    -2212: "Heavy water (D2O)",
    3122: "Methane (CH4)",
    -3122: "Methyl ion (CH3-)",
    3312: "Ethylene (C2H4)",
    -3312: "Ionised ethylene (C2H3-)",
    3334: "Ozone (O3)",
    -3334: "Superoxide anion (O2-)"
}

def calculate_average_and_uncertainty(data):
    n = len(data)
    if n == 0:   # cannot calculate a mean from 0 events
        return UNPHYSICAL_VALUE, UNPHYSICAL_VALUE
    mean = sum(data) / n
    if n > 1:
        variance = sum((x - mean) ** 2 for x in data) / (n - 1)   # sample variance, divides by (N-1)

        if variance < 0:   # protects the sqrt -- variance can't really be negative, but check anyway
            error = UNPHYSICAL_VALUE
        else:
            error = math.sqrt(variance / n)
    else:
        error = UNPHYSICAL_VALUE   # can't get a real uncertainty from just 1 event

    return mean, error

# Ask the user for the input file to avoid wording errors
filename = input("Enter the data file name: ") 

#Protection 1: Checking that the file exists before using it
try:
    f = open(filename, "r")
except FileNotFoundError:
    print("Error: could not find the file", filename)
    exit()

# counts[molecule_id] = one number per event (the full history)
# current[molecule_id] = running tally for whichever event is being read right now
counts = {}
current = {}
for molecule_id in molecules:
    counts[molecule_id] = []
    current[molecule_id] = 0

#loop reads the file one event at a time
while True:
    header_line = f.readline()
    if header_line == "":   #empty string means, there is nothing else to read
        break

    header = header_line.split()

    #Header only has event number and particle count - double checking 
    if len(header) != 2: 
        print("Error: malformed header line:", header_line)
        break

    try:
        n_particles = int(header[1]) 
    except ValueError:
        print("Error, count is not an integer", header_line)
        break
    
    #A particle count can't physically be negative
    if n_particles < 0:   
        print("Error: negative particle count:", header_line)
        break
    
    # Resetting to 0, without this lefover from previous event would carry 
    for molecule_id in molecules:
        current[molecule_id] = 0

    for i in range(n_particles): 
        line = f.readline()  

        # Making sure each particle line has 4 components
        columns = line.split() # splitting components between spaces
      
        if len(columns) != 4:
            print("Error: malformed header line:", header_line)
            continue   # skip this broken event, but keep reading the rest of the file

        try:
            particle_id = int(columns[3]) # convert ID to integer
        except ValueError:
            print("Error: ID is not an integer:", line)
            continue # again if this fails it will only skip a line instead of breaking

        # counting the molecule if it's one we're tracking
        if particle_id in current:
            current[particle_id] = current[particle_id] + 1

    # Loop is finished for one event. add this event's counts to the lists
    for molecule_id in molecules:
        counts[molecule_id].append(current[molecule_id])

f.close()   # closing file

# Printing results as a table 
print(f"\n{'ID':>6}  {'Molecule':<26}{'Average':>10}{'Uncertainty':>14}")
 #the numbers in red are just regulating the space between the columns so it looks organize


for molecule_id in molecules:
    mean, error = calculate_average_and_uncertainty(counts[molecule_id])

    if mean == UNPHYSICAL_VALUE:
        print(molecule_id, "| No events found")
        continue
    
    name = molecules[molecule_id]
    error_str = "N/A" if error == UNPHYSICAL_VALUE else f"{round(error, 4)}"
    # shows "N/A" instead of printing -1, so the table doesn't look like a real uncertainty value
    print(f"{molecule_id:>6}  {name:<26}{round(mean, 4):>10}{error_str:>14}")
    #the numbers in red are just regulating the space between the columns so it looks organize