# PRA2003 - Simulating molecular emissions in a combustion reaction

## Silvia Jimeno Ferrer - I6377278 

## Scenario
This is a chemistry-themed exercise simulating molecular emissions in a combustion reaction. Each file represents a single simulation of molecular species produced during combustion at high temperatures.

## Input Structure
Each input file follows this format:
**Header line** (First line of the file) it contains: 
  - **Event ID**: the ID of the experiment or simulation run
  - **Number of molecules tracked**: the total number of molecules observed in this run

**Data lines** (There is one per molecule, following the header):
- **3D momentum components** — `px`, `py`, `pz` (in units of 10⁻²³ kg·m/s)
- **Molecule/Isotope ID** — an integer ID identifying the molecule or isotope

---
**Goal: Answer the following questions**
1. What are the average counts of each molecular species and their statistical uncertainties?
2. Is there any asymmetry between the normal and the variant molecule?
3. Is there any asymmetry as a function of their momentum?

---

## Installation and usage

Needs Python 3 (tested with Python 3 on macOS). No additional packages are required: the only module used is `math`, which already comes with Python.

To run:

1. Download the data files (`output-Set0.txt`, `output-Set1.txt` ... `output-Set10.txt`, about 5 million events in total) and put them in the same folder as the scripts. The data files are not included in this repository because they are too large for GitHub.
2. Open that folder in VS Code, or open a terminal in that folder (the data files must be in the folder you run the script from).
3. Depending on what you want to run:
   - Only one dataset, week 3 version: `python3 "week 3 deliverable.py"` will ask you to type a filename, for example `output-Set1.txt` (type only one file name).
   - ALL 11 datasets combined, week 4: `python3 "week 4 deliverable.py"` runs automatically, no input needed, just needs the 11 data files in the same folder. It prints in tables the results for questions 1 and 2.

## Files

| File | Description |
|---|---|
| `code week 2` | Week 2 exercise: first steps reading the data file. |
| `week 3 deliverable.py` | Reads one data file (the user types the file name) and calculates the average count of each molecule per event and its statistical uncertainty |
| `week 4 deliverable.py` | Runs all 11 datasets (`output-Set0.txt` to `output-Set10.txt`) combined. Calculates the average count of each molecule per event with the uncertainty from the sub-sampling method (each file is one sub-sample), and checks the asymmetry between each normal molecule and its variant. **This is the version for the week 4 deliverable.** |
| `README.md` | This file. |

## The molecules

Each molecule has an ID number. A **positive** ID is the normal molecule and the **negative** ID which is its variant.

| ID | Normal molecule | ID | Variant |
|---:|---|---:|---|
| 211 | Carbon monoxide | -211 | Carbon-13 monoxide |
| 321 | Nitric oxide | -321 | Ionised NO |
| 2212 | Water | -2212 | Heavy water (D2O) |
| 3122 | Methane (CH4) | -3122 | Methyl ion (CH3-) |
| 3312 | Ethylene (C2H4) | -3312 | Ionised ethylene (C2H3-) |
| 3334 | Ozone (O3) | -3334 | Superoxide anion (O2-) |

## How the code works (step by step)

1. **Open the files one by one.** A `for` loop goes over the numbers 0 to 10 and builds the file names (`output-Set0.txt`, `output-Set1.txt`, ...). If a file is missing, the program prints an error and stops.
2. **Read the events.** For every event the program reads the header line to know how many molecule lines follow, and then reads those lines.
3. **Count the molecules.** For every molecule line it takes the ID (the 4th column). If the ID is one of the 12 molecules in the table above, the count for that molecule goes up by 1.
4. **Check for mistakes in the data.** The program checks that:
   - If the header line has 2 values
   - If the number of molecules is a whole number and not negative
   - If every molecule line has 4 values and the ID is a whole number
   - If the file does not end in the middle of an event

   If a molecule line is broken it is skipped. If a header line is broken, the program stops reading that file.
5. **Skip empty events.** Events with 0 molecules are skipped and counted separately, like in week 3.
6. **Save the results of each file.** When a file is finished, the program saves the average of each molecule in that file (this is used for the sub-sampling) and adds the counts to the total.
7. **Calculate and print the answers** to questions 1 and 2 (explained below).

---

## Question 1: average counts and uncertainties

### Average per event

The average of a molecule is the total number of that molecule found in all files, divided by the total number of events:

```
average = total count of the molecule / total number of events
```

As a math formula, with $n_i$ the number of that molecule in event $i$ and $N$ the total number of events:

$$
\bar{n} = \frac{1}{N}\sum_{i=1}^{N} n_i
$$

**Example (carbon monoxide):** 92,126,688 molecules were found in about 4.62 million events, so the average is 92,126,688 / 4,618,000 ≈ **19.95** molecules per event.

### Uncertainty (sub-sampling method)

For the uncertainty the data is split into smaller groups, called sub-samples. In this code **every file is one sub-sample**, so there are **K = 11** sub-samples.

1. The average of the molecule is calculated in each file separately, giving 11 averages: a1, a2, ..., a11.
2. The spread of these 11 averages is calculated (the sample variance, dividing by K - 1):

```
mean of the averages = (a1 + a2 + ... + a11) / K

variance = sum of (ai - mean of the averages)^2 / (K - 1)
```

3. The uncertainty on the average is:

```
uncertainty = sqrt(variance / K)
```

As math formulas, with $a_k$ the average in file $k$:

$$
\bar{a} = \frac{1}{K}\sum_{k=1}^{K} a_k
\qquad
s^2 = \frac{1}{K-1}\sum_{k=1}^{K}\left(a_k - \bar{a}\right)^2
\qquad
\sigma = \sqrt{\frac{s^2}{K}} = \frac{s}{\sqrt{K}}
$$

**Example (carbon monoxide):** the 11 file averages of carbon monoxide have a spread (standard deviation) of about s = 0.109. The uncertainty is then 0.109 / √11 = 0.109 / 3.32 ≈ **0.033**.

The idea is simple: if the 11 files give very similar averages, the result is precise and the uncertainty is small. If they are very different, the uncertainty is bigger.

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

**What this means:** carbon monoxide is the most common molecule, with about 20 per event. Ozone and superoxide are the rarest, with only about 1 in every 1000 events.

---

## Question 2: asymmetry between the normal and the variant molecule

To see if there is an asymmetry, the normal molecule is compared with its variant (for example carbon monoxide with carbon-13 monoxide).

### Difference

```
difference = average(normal) - average(variant)
```

$$
\Delta = \bar{n}_{normal} - \bar{n}_{variant}
$$

**Example (carbon monoxide):** 19.949508 − 19.917211 = **0.0323**

If there is no asymmetry, the difference should be close to 0.

### Uncertainty of the difference

The normal molecule and its variant come from the same events, so when one goes up in a file, the other usually goes up too. This is measured with the **correlation coefficient r** between their 11 file averages (r = 1 means they always go up and down together, r = 0 means they are not related). The uncertainty of the difference takes this into account:

```
uncertainty of difference = sqrt(unc_normal^2 + unc_variant^2 - 2 * r * unc_normal * unc_variant)
```

The correlation r is calculated from the 11 file averages of the normal molecule ($a_k$) and of the variant ($b_k$):

$$
r = \frac{\sum_{k}(a_k - \bar{a})(b_k - \bar{b})}{\sqrt{\sum_{k}(a_k - \bar{a})^2 \, \sum_{k}(b_k - \bar{b})^2}}
$$

and the uncertainty of the difference is:

$$
\sigma_\Delta = \sqrt{\sigma_{normal}^2 + \sigma_{variant}^2 - 2\,r\,\sigma_{normal}\,\sigma_{variant}}
$$

**Example (carbon monoxide):** with σ_normal = 0.0327, σ_variant = 0.0319 and r = 0.991:

```
sqrt(0.0327^2 + 0.0319^2 - 2 * 0.991 * 0.0327 * 0.0319) ≈ 0.0045
```

Without the correlation (r = 0) it would be sqrt(0.0327² + 0.0319²) ≈ 0.046, so taking r into account makes the uncertainty about 10 times smaller. (The exact result depends on all the decimals of r, which is why the code uses the unrounded values.)

When r is close to 1, the uncertainty of the difference becomes much smaller, because the shared ups and downs cancel out when subtracting.

### Is it significant?

The number of sigmas tells how far the difference is from 0, compared to its uncertainty:

```
n_sigma = difference / uncertainty of difference
```

$$
n_\sigma = \frac{\Delta}{\sigma_\Delta}
$$

**Example (carbon monoxide):** 0.0323 / 0.0045 ≈ **7.15**, which is bigger than 3, so it is significant.

In this analysis, **an asymmetry is called significant if n_sigma is bigger than 3**.

### Asymmetry in %

To compare molecules with very different amounts, the asymmetry is also given as a percentage:

```
asymmetry (%) = difference / (average(normal) + average(variant)) * 100

uncertainty of asymmetry (%) = uncertainty of difference / (average(normal) + average(variant)) * 100
```

$$
A = \frac{\bar{n}_{normal} - \bar{n}_{variant}}{\bar{n}_{normal} + \bar{n}_{variant}} \times 100\%
\qquad
\sigma_A = \frac{\sigma_\Delta}{\bar{n}_{normal} + \bar{n}_{variant}} \times 100\%
$$

**Example (carbon monoxide):** 0.0323 / (19.9495 + 19.9172) × 100 = 0.0323 / 39.87 × 100 ≈ **0.081%**, with uncertainty 0.0045 / 39.87 × 100 ≈ **0.011%**.

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

In all pairs the normal molecule is a bit more common than its variant. For **water** (10.1 sigma),**methane** (8.4 sigma), **carbon monoxide** (7.2 sigma), and  this difference is bigger than 3 sigma, so there is a significant asymmetry. For **nitric oxide**, **ethylene** and **ozone** the difference is smaller than 2 sigma, so it could just be a random fluctuation and we **can't** say there is an asymmetry.

---

## Question 3: asymmetry as a function of momentum

This question will be answered next week. The current code only uses the molecule ID (4th column) and does not use the momentum values (`px`, `py`, `pz`). 
