"""
Week 4 Deliverable
-------------------
Reads the 11 data files (output-Set0.txt to output-Set10.txt, ~5M events in total),
selects the molecules of interest based on their ID code, and computes the average
number of each molecule per event, together with the statistical uncertainty.

New this week:
- ALL the files need to be read, not only one 
- The uncertainty is calculated with the sub-sampling method: every file is used
  as one sub-sample, so there are 11 sub-samples
- It checks if there is an asymmetry between the normal molecule (positive ID)
  and its variant (negative ID)
"""

import math #needed for the square roots (uncertainty)

UNPHYSICAL_VALUE = -1  #used when an uncertainty can't be calculated (it can never really be negative)

#the data is split in 10 files: output-Set1.txt until output-Set10.txt
#we do not want to include file 0 in our 
FIRST_FILE = 1 
LAST_FILE = 10 

#Molecule IDs and names
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
    #Same function as in week 3, but now "data" is a list with ONE average per
    #sub-sample (so 11 numbers, one per file) instead of one number per event.
    #The uncertainty is then the spread of the sub-sample averages / sqrt(number of sub-samples)
    n = len(data)
    if n == 0:   #cannot calculate a mean from 0 sub-samples
        return UNPHYSICAL_VALUE, UNPHYSICAL_VALUE
    mean = sum(data) / n
    if n > 1:
        variance = sum((x - mean) ** 2 for x in data) / (n - 1)   #sample variance, divides by (N-1)

        if variance < 0:   #protects the sqrt -- variance can't really be negative, but check anyway
            error = UNPHYSICAL_VALUE
        else:
            error = math.sqrt(variance / n)
    else:
        error = UNPHYSICAL_VALUE   #can't get a real uncertainty from just 1 sub-sample

    return mean, error


def calculate_correlation(data_a, data_b):
    #Correlation coefficient r between two lists (here: the file averages of the
    #normal molecule and of its variant).
    #r close to 1 -> they go up and down together, r close to 0 -> not related
    n = len(data_a)
    if n < 2:   #need at least 2 points to calculate a correlation
        return 0

    mean_a = sum(data_a) / n
    mean_b = sum(data_b) / n

    covariance = 0
    variance_a = 0
    variance_b = 0
    for i in range(n):
        covariance = covariance + (data_a[i] - mean_a) * (data_b[i] - mean_b)
        variance_a = variance_a + (data_a[i] - mean_a) ** 2
        variance_b = variance_b + (data_b[i] - mean_b) ** 2

    if variance_a == 0 or variance_b == 0:   #avoid dividing by 0 (e.g. molecule never appears)
        return 0

    return covariance / math.sqrt(variance_a * variance_b)


#total_counts[molecule_id]   = how many of that molecule in ALL files together
#file_averages[molecule_id]  = list with the average per event in each file (the sub-samples)
total_counts = {}
file_averages = {}
for molecule_id in molecules:
    total_counts[molecule_id] = 0
    file_averages[molecule_id] = []

n_events_total = 0  #number of (non-empty) events in all files together
n_empty = 0         #number of empty events (0 particles) that were skipped

#Loop over the 10 files, one after the other
for set_number in range(FIRST_FILE, LAST_FILE + 1):
    filename = "output-Set" + str(set_number) + ".txt"   #builds the name: output-Set1.txt, output-Set2.txt, ...

    #Protection 1: Checking that the file exists before using it
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("Error: could not find the file", filename)
        exit()

    print("Reading", filename, "...")

    #counts for THIS file only (this file is one sub-sample)
    file_counts = {}
    for molecule_id in molecules:
        file_counts[molecule_id] = 0
    n_events_file = 0
    file_ok = True   #becomes False if something is wrong in the file

    #loop reads the file one event at a time (same as week 3)
    while True:
        header_line = f.readline()
        if header_line == "":   #empty string means, there is nothing else to read
            break

        header = header_line.split()

        #Header only has event number and particle count - double checking
        if len(header) != 2:
            print("Error: malformed header line:", header_line)
            file_ok = False
            break

        try:
            n_particles = int(header[1])
        except ValueError:
            print("Error, count is not an integer", header_line)
            file_ok = False
            break

        #A particle count can't physically be negative
        if n_particles < 0:
            print("Error: negative particle count:", header_line)
            file_ok = False
            break

        #Empty events are skipped, like in week 3
        if n_particles == 0:
            n_empty = n_empty + 1
            continue

        #Reading the particle lines of this event
        for i in range(n_particles):
            line = f.readline()

            #if the file ends in the middle of an event, something is wrong
            if line == "":
                print("Error: file ended in the middle of an event:", header_line)
                file_ok = False
                break

            #Making sure each particle line has 4 components
            columns = line.split()   #splitting components between spaces
            if len(columns) != 4:
                print("Error: malformed particle line:", line)
                continue   #skip this broken line, but keep reading the rest

            try:
                particle_id = int(columns[3])   #convert ID to integer
            except ValueError:
                print("Error: ID is not an integer:", line)
                continue   #again if this fails it will only skip a line instead of breaking

            #counting the molecule if it's one we're tracking
            if particle_id in file_counts:
                file_counts[particle_id] = file_counts[particle_id] + 1

        if not file_ok:   #stop reading this file if there was a problem
            break

        n_events_file = n_events_file + 1   #one more complete event in this file

    f.close()   #closing file

    #If a file had no events it can't be used as a sub-sample
    if n_events_file == 0:
        print("Warning: no events found in", filename)
        continue

    #This file is finished: add its counts to the totals and save its averages
    for molecule_id in molecules:
        total_counts[molecule_id] = total_counts[molecule_id] + file_counts[molecule_id]
        file_averages[molecule_id].append(file_counts[molecule_id] / n_events_file)

    n_events_total = n_events_total + n_events_file

print("\nEvents counted:", n_events_total)
print("Empty events skipped:", n_empty)
print("Number of sub-samples (files):", len(file_averages[211]))

if n_events_total == 0:   #nothing to calculate
    print("No events found.")
    exit()


#QUESTION 1: Average count of each molecule and its uncertainty

#saving the average and uncertainty of every molecule, needed again for question 2
averages = {}
uncertainties = {}

print("\nQUESTION 1: average number of each molecule per event")
print(f"\n{'code':>6} {'name':<26}{'total_count':>12}{'average_per_event':>19}{'uncertainty':>13}")
#the numbers are just regulating the space between the columns so it looks organized

for molecule_id in molecules:
    #the average uses ALL events together: total count / total number of events
    average = total_counts[molecule_id] / n_events_total

    #the uncertainty comes from the spread of the 11 file averages (sub-sampling)
    mean_of_files, error = calculate_average_and_uncertainty(file_averages[molecule_id])

    averages[molecule_id] = average
    uncertainties[molecule_id] = error

    name = molecules[molecule_id]
    error_str = "N/A" if error == UNPHYSICAL_VALUE else f"{error:.6f}"
    #shows "N/A" instead of printing -1, so the table doesn't look like a real uncertainty value
    print(f"{molecule_id:>6} {name:<26}{total_counts[molecule_id]:>12}{average:>19.6f}{error_str:>13}")


#QUESTION 2: Asymmetry between the normal molecule and its variant

#difference   = average(normal) - average(variant)
#uncertainty  = sqrt(err_normal^2 + err_variant^2 - 2*r*err_normal*err_variant)
   #(r is the correlation, because both molecules come from the same events)
#n_sigma      = difference / uncertainty  -> how many sigmas away from 0
#asymmetry %  = difference / (average(normal) + average(variant)) * 100
#significant if n_sigma is bigger than 3

print("\nQUESTION 2: asymmetry between normal and variant molecule")
print(f"\n{'code':>6} {'name':<18}{'difference':>11}{'uncertainty':>13}{'r':>8}{'n_sigma':>9}{'asym_%':>9}{'asym_unc_%':>12}{'significant':>13}")

for molecule_id in molecules:
    if molecule_id < 0:   #only start from the normal molecules, the variant is -molecule_id
        continue

    variant_id = -molecule_id

    #If there were no assymetry the difference would be 0 
    difference = averages[molecule_id] - averages[variant_id]

    error_normal = uncertainties[molecule_id]
    error_variant = uncertainties[variant_id]

    #if one of the uncertainties could not be calculated, the rest can't either
    if error_normal == UNPHYSICAL_VALUE or error_variant == UNPHYSICAL_VALUE:
        print(f"{molecule_id:>6} {molecules[molecule_id]:<18}  N/A")
        continue

    #r = 1 means they always fluctuate together and 0 that they are unrelated 
    r = calculate_correlation(file_averages[molecule_id], file_averages[variant_id])

#KEY LINE - uncertainty of the difference: the -2*r part removes the fluctuations that
    #both molecules share, so the uncertainty becomes smaller when r is close to 1
    variance_difference = error_normal ** 2 + error_variant ** 2 - 2 * r * error_normal * error_variant
    if variance_difference <= 0:   #protects the sqrt and the division below
        print(f"{molecule_id:>6} {molecules[molecule_id]:<18}  uncertainty could not be calculated")
        continue
    difference_error = math.sqrt(variance_difference)

    #measures how big the differnece is compared to the uncretainty
    n_sigma = difference / difference_error

    total = averages[molecule_id] + averages[variant_id]
    if total == 0:   #avoid dividing by 0
        print(f"{molecule_id:>6} {molecules[molecule_id]:<18}  molecule never found")
        continue
    asym_percent = difference / total * 100
    asym_error_percent = difference_error / total * 100

    #True or False
    significant = abs(n_sigma) > 3   
    
    #printing all these numbers in one row of the table 
    print(f"{molecule_id:>6} {molecules[molecule_id]:<18}{difference:>11.4f}{difference_error:>13.4f}{r:>8.3f}{n_sigma:>9.2f}{asym_percent:>9.3f}{asym_error_percent:>12.3f}{str(significant):>13}")