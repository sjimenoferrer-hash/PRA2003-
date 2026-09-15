# PRA2003 - Simulating molecular emissions in a combustion reaction

## Silvia Jimeno Ferrer - I6377278 

## Context
This is a chemistry-themed exercise simulating molecular emissions in a combustion reaction. Each file represents a single simulation of molecular species produced during combustion at high temperatures.

## Input Structure
Each input file follows this format:
**Header line** (first line of the file):
- **Event ID**: the ID of the experiment or simulation run
- **Number of molecules tracked**: the total number of molecules observed in this run

**Data lines** (one per molecule, following the header):
- **3D momentum components** — `px`, `py`, `pz` (in units of 10⁻²³ kg·m/s)
- **Molecule/isotope ID** — an integer code identifying which molecule or isotope this row represents

---
**Answer the following questions**
1. What are the average counts of each molecular species and their statistical uncertainties?
2. Is there any asymmetry between the normal and the variant molecule?
3. Is there any asymmetry as a function of their momentum?
