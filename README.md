# PRA2003 - Simulating molecular emissions in a combustion reaction

## Silvia Jimeno Ferrer - I6377278

## Scenario
This is a chemistry-themed exercise simulating molecular emissions in a combustion reaction. Each file represents a single simulation of molecular species produced during combustion at high temperatures.

## Input Structure
Each file contains around 500k events, therefore this code analyses 5 million simulated combustion events in total for 6 molecular species, each one as a normal molecule and its variant. 

Each input file follows this format:
**Header line** (first line of each event) it contains:
  - **Event ID**: the ID of the experiment or simulation run
  - **Number of molecules tracked**: the total number of molecules observed in this run

**Data lines** (there is one per molecule, following the header):
- **3D momentum components**: `px`, `py`, `pz` (in units of 10⁻²³ kg·m/s)
- **Molecule/Isotope ID**: an integer ID identifying the molecule or isotope

---
**Goal: Answer the following questions**
1. What are the average counts of each molecular species and their statistical uncertainties?
2. Is there any asymmetry between the normal and the variant molecule?
3. Is there any asymmetry as a function of their momentum?

---

## Installation and usage

Needs Python 3 (tested with Python 3 on macOS). The week 3 and week 4 scripts only use `math`, which already comes with Python. The final script (question 3) also needs `numpy` and `matplotlib`:

```bash
python3 -m pip install numpy matplotlib
```

To run:

1. Download the data files (`output-Set1.txt` ... `output-Set10.txt`, about 5 million events in total) and put them in the same folder as the scripts. The data files are not included in this repository because they are too large for GitHub. (`output-Set0.txt` is not needed: it only contains one event and is not used in the analysis.)
2. Open that folder in VS Code, or open a terminal in that folder (the data files must be in the folder you run the script from).
3. Depending on what you want to run:
   - Only one dataset, week 3 version: `python3 "week 3 deliverable.py"` will ask you to type a filename, for example `output-Set1.txt` (type only one file name).
   - ALL 10 datasets combined, week 4: `python3 "week 4 deliverable.py"` runs automatically, no input needed. It prints in tables the results for questions 1 and 2.
   - Asymmetry as a function of momentum, final version: `python3 "final code practical.py"` runs automatically and saves the figures.

## Files

| File | Description |
|---|---|
| `week 2.py` | Week 2 exercise: first steps reading the data file. |
| `week 3 deliverable.py` | Reads one data file (the user types the file name) and calculates the average count of each molecule per event and its statistical uncertainty. |
| `week 4 deliverable.py` | Runs all 10 datasets combined. Calculates the average count of each molecule per event with the uncertainty from the sub-sampling method (each file is one sub-sample), and checks the asymmetry between each normal molecule and its variant. **Answers questions 1 and 2.** |
| `final code practical.py` | Calculates the asymmetry as a function of momentum and saves the figure. **Answers question 3.** |
| `All IDs - asymmetry as a function of momentum.jpeg` | Figure with the asymmetry as a function of momentum, one panel per pair. |
| `All IDS - mometum distribution.jpeg`, `All IDs momentum distribution - no file 10.png` | Figures with the momentum spectrum (dN/dP) of the normal and the variant molecule, with and without the file that differs. |
| `README.md` | This file. |

## The molecules

Each molecule has an ID number. A **positive** ID is the normal molecule and the **negative** ID is its variant.

| ID | Normal molecule | ID | Variant |
|---:|---|---:|---|
| 211 | Carbon monoxide | -211 | Carbon-13 monoxide |
| 321 | Nitric oxide | -321 | Ionised NO |
| 2212 | Water | -2212 | Heavy water (D2O) |
| 3122 | Methane (CH4) | -3122 | Methyl ion (CH3-) |
| 3312 | Ethylene (C2H4) | -3312 | Ionised ethylene (C2H3-) |
| 3334 | Ozone (O3) | -3334 | Superoxide anion (O2-) |

## How the code works

All scripts follow the same steps:

1. **Read the files.** The program opens the files one by one. If a file is missing, it prints an error and stops.
2. **Read the events.** For every event it reads the header line to know how many molecule lines follow, and then reads those lines.
3. **Check for mistakes in the data.** Broken molecule lines are skipped, and a broken header stops the reading of that file.
4. **Skip empty events.** Events with 0 molecules are skipped and not counted as events.
5. **Sub-samples.** Every file is one sub-sample (10 in total). Everything is calculated in each file separately, and the spread between the 10 files is used for the statistical uncertainty.

---

## Question 1: Average counts and uncertainties

**File:** `week 4 deliverable.py` (the week 3 script gives the same calculation for one file).

**Method:** The program counts how many times each molecule appears in every file and divides by the number of events in that file. This gives 10 averages for each molecule. The final average is the total count divided by the total number of events. The uncertainty comes from the spread of the 10 file averages (sub-sampling method): the standard deviation of the 10 values divided by √10, which is the precision of the average.

**Example (carbon monoxide):** 92,126,688 molecules were found in about 4.62 million events, so the average is about 19.95 molecules per event.

### Results

| ID | Molecule | Total count | Average per event | Uncertainty |
|---:|---|---:|---:|---:|
| 211 | Carbon monoxide | 92126688 | 19.949508 | 0.032746 |
| -211 | Carbon-13 monoxide | 91977542 | 19.917211 | 0.031873 |
| 321 | Nitric oxide | 11587227 | 2.509148 | 0.004774 |
| -321 | Ionised NO | 11560946 | 2.503457 | 0.005504 |
| 2212 | Water | 5578693 | 1.208034 | 0.001896 |
| -2212 | Heavy water (D2O) | 5468447 | 1.184161 | 0.002412 |
| 3122 | Methane (CH4) | 1277330 | 0.276599 | 0.001074 |
| -3122 | Methyl ion (CH3-) | 1254690 | 0.271696 | 0.000985 |
| 3312 | Ethylene (C2H4) | 182139 | 0.039441 | 0.000284 |
| -3312 | Ionised ethylene (C2H3-) | 180104 | 0.039000 | 0.000402 |
| 3334 | Ozone (O3) | 5482 | 0.001187 | 0.000042 |
| -3334 | Superoxide anion (O2-) | 5318 | 0.001152 | 0.000051 |

This table shows how carbon monoxide is the most common molecule, with about 20 per event. Whereas, ozone and superoxide are the rarest, with only about 1 in every 1000 events.

---

## Question 2: Asymmetry between the normal and the variant molecule

**File:** `week 4 deliverable.py`

**Method:** The normal molecule is compared with its variant (for example carbon monoxide with carbon-13 monoxide) by taking the difference between their averages. If there is no asymmetry, the difference should be close to 0. The normal molecule and its variant come from the same events, so they go up and down together from file to file. The program measures this with the correlation r between their 10 file averages (r = 1 means they always change together), and uses it to get the uncertainty of the difference. Then it counts how many uncertainties ("sigmas") the difference is away from 0. **An asymmetry is called significant if it is more than 3 sigma.** To compare molecules with very different amounts, the difference is also given as a percentage of the total (normal + variant).

### Results

| Normal / Variant | Difference | Uncertainty | r | n_sigma | Asymmetry (%) | Significant? |
|---|---:|---:|---:|---:|---:|:---:|
| Carbon monoxide / Carbon-13 monoxide | 0.0323 | 0.005 | 0.991 | 7.15 | 0.081 ± 0.011 | Yes |
| Nitric oxide / Ionised NO | 0.0057 | 0.003 | 0.804 | 1.73 | 0.114 ± 0.066 | No |
| Water / Heavy water | 0.0239 | 0.002 | 0.414 | 10.06 | 0.998 ± 0.100 | Yes |
| Methane / Methyl ion | 0.0049 | 0.001 | 0.843 | 8.41 | 0.894 ± 0.106 | Yes |
| Ethylene / Ionised ethylene | 0.0004 | 0.000 | 0.019 | 0.90 | 0.562 ± 0.624 | No |
| Ozone / Superoxide anion | 0.0000 | 0.000 | -0.090 | 0.51 | 1.496 ± 2.930 | No |

### Conclusion

In all pairs the normal molecule is a bit more common than its variant. For **water** (10.1 sigma), **methane** (8.4 sigma) and **carbon monoxide** (7.2 sigma) the difference is bigger than 3 sigma, so there is a significant asymmetry. For **nitric oxide**, **ethylene** and **ozone** the difference is smaller than 2 sigma, so it could just be a random fluctuation and we **can't** say there is an asymmetry.

---

## Question 3: Asymmetry as a function of momentum

**File:** `final code practical.py`, which saves the figures.

**Method:** The momentum of every molecule is calculated from `px`, `py` and `pz`, and the molecules are split into bins of momentum: 0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 6, 8 and everything above 8 (units 10⁻²³ kg·m/s). In each bin, the asymmetry between the normal and the variant molecule (their difference divided by their sum) is calculated separately in each of the 10 files. The point in the plot is the average of the 10 files, and the error bar is the statistical uncertainty of each bin, taken as the standard deviation of the 10 files. I used the standard deviation here, and not the error on the mean (about 3 times smaller), because it shows how much the asymmetry changes between files, which is the more careful choice when deciding whether a bin is really different from zero.

### Results

![Asymmetry vs momentum](All%20IDs%20-%20asymmetry%20as%20a%20function%20of%20momentum.jpeg)

Each panel is one pair. The blue points are the asymmetry in each bin (vertical bar = statistical uncertainty, horizontal bar = bin width). The orange band is the overall asymmetry with its uncertainty, the dashed line is A = 0, and the green line is a straight-line fit through the points from 0 to 8.

The slope of the fit tells if the asymmetry changes with momentum. In every pair it is consistent with 0 (less than 1.5 sigma):

| Pair | Slope of the fit (per 10⁻²³ kg·m/s) | Sigma from 0 |
|---|---:|---:|
| Carbon monoxide / Carbon-13 monoxide | +0.0002 ± 0.0002 | 1.3 |
| Nitric oxide / Ionised NO | +0.0004 ± 0.0004 | 0.9 |
| Water / Heavy water | +0.0004 ± 0.0009 | 0.5 |
| Methane / Methyl ion | +0.0004 ± 0.0012 | 0.3 |
| Ethylene / Ionised ethylene | +0.0005 ± 0.0030 | 0.1 |
| Ozone / Superoxide anion | -0.0062 ± 0.0172 | 0.4 |

**What I see:** For carbon monoxide, water and methane the points stay slightly above 0 in almost every bin and follow the orange band (the overall asymmetry), so the asymmetry is the same at low and high momentum. For nitric oxide, ethylene and ozone the points scatter around 0 within their large error bars. The error bars get bigger at high momentum and for the rare molecules because there are fewer molecules in those bins.

### Momentum spectrum (dN/dP)

**What I did:** To check whether the normal and the variant molecule move in the same way, I also plotted how many molecules there are per event for each unit of momentum (dN/dP), for both molecules of every pair (blue = normal, red = variant, log scale). The open last bin (P > 8) is not shown.

![Momentum spectrum](All%20IDS%20-%20mometum%20distribution.jpeg)

**What was observed**
- In every pair the blue and red points lie on top of each other, so the normal and the variant molecule have the same momentum spectrum within the uncertainties. This agrees with the asymmetry not depending on momentum.
- Most molecules have a low momentum. The spectrum goes up to a maximum at about P = 0.5 to 2 and then falls towards higher momentum.
- In every pair, the points between P = 2.5 and 4 have bigger error bars than their neighbours. Since the error bar is the spread between the 10 files, this means that the files do not agree with each other in this range.

### Why are the error bars big between P = 2.5 and 4?

I looked at this together with my group. We compared the number of molecules per event in each momentum bin, file by file. When we were doing this, we noticed Files 1 to 9 were very similar to each other, but **file 10 was very different**. Example for methane / methyl ion (molecules per event in each bin):

| P bin | 0–0.5 | 0.5–1 | 1–1.5 | 1.5–2 | 2–2.5 | 2.5–3 | 3–4 | 4–6 | 6–8 | > 8 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| File 1 | 0.0158 | 0.0522 | 0.0539 | 0.0474 | 0.0393 | 0.0323 | 0.0506 | 0.0682 | 0.0446 | 0.1473 | 0.552 |
| File 10 | 0.0004 | 0.0067 | 0.0219 | 0.043 | 0.0671 | 0.0909 | 0.21 | 0.1075 | 0.0018 | 0.0005 | 0.550 |

- The total number of molecules per event in file 10 is the same as in the other files (0.550 against 0.552).
- But the molecules in file 10 have higher momentum: there are fewer molecules at low momentum and more around P = 2.5 to 4.
- We notice this was different but we do not know the reason for it.

Without file 10, the error bars of the spectrum are much smaller:

![Momentum spectrum without file 10](All%20IDs%20momentum%20distribution%20-%20no%20file%2010.png)

**Decision:** We kept all 10 files in the final analysis. File 10 has the same number of molecules per event as the others, so it is fine for the average counts and the overall asymmetry. It only makes the error bars of the momentum plots larger, and this is a limitation of the analysis.

---

**Conclusion:** The asymmetry exists for water, methane and carbon monoxide, but it is a small constant effect that does not change with momentum. For nitric oxide, ethylene and ozone we cannot say that there is an asymmetry.

## Limitations

- Pairs with very few molecules (ozone / superoxide) have large uncertainties.
- A momentum bin is left off the plot if it has no error bar (fewer than 2 sub-samples with molecules in it).
- File 10 has a different momentum distribution than the other nine files, for an unknown reason. It makes the error bars of the momentum plots bigger.
- A slope consistent with zero does not prove that the asymmetry is independent of momentum (it could go up and then down). That is why the points in each bin are also compared with the overall asymmetry.
