# Analysis for Accurate Estimation of GPS Signal Delays

This repository contains the data processing pipelines, signal analysis scripts, and experimental notebooks developed as part of my **Final Year Project at Nanyang Technological University (NTU)**, conducted in collaboration with **A*STAR’s National Metrology Centre**.

The project focuses on analysing GNSS receiver clock bias and GPS signal delays using CGGTTS data, investigating how environmental factors, satellite geometry, and surrounding infrastructure influence timing accuracy — with the long-term goal of improving low-cost GNSS receiver performance.

---

## 🎯 Project Objectives

- Analyse GPS receiver clock system offsets (REFSYS) from CGGTTS files  
- Study signal stability across different days, months, and locations  

### Investigate effects of:

- Satellite elevation & azimuth angles  
- Environmental conditions (temperature, pressure, rainfall, wind)  
- Urban obstructions & multipath risk  

- Quantify signal volatility and long-term timing drift  
- Build foundations for future ML-based clock bias correction models  

---

## 📂 Repository Structure
Analysis-for-Accurate-Estimation-of-GPS-Signal-Delays/
│
├── data/ # Raw CGGTTS files and weather datasets
├── notebooks/ # Jupyter notebooks for analysis & visualisation
├── results/ # Generated plots and processed outputs
├── src/ # Core data loading and preprocessing utilities
├── README.md
├── LICENSE
└── .gitignore

---

## 📊 Key Analyses Performed

### ⏱ Time Transfer & Clock Stability

- Average REFSYS vs time (daily & monthly)  
- Long-term drift trends  
- Monthly stability boxplots  

### 🛰 Satellite Geometry Effects

- Elevation angle vs REFSYS (multipath sensitivity)  
- Azimuth angle vs volatility (urban reflection zones)  

### 🌦 Environmental Impact

- REFSYS vs temperature, pressure, rainfall, wind speed  
- Weather-driven volatility comparisons  

### 🏙 Urban Obstruction Risk

- Building reflection risk proxy analysis  
- Signal instability by direction & elevation  

### ⏰ Temporal Behaviour

- Day vs night volatility comparison  
- Hourly resampled stability metrics  

---

## 📁 Results

The `results/` folder contains:

- Monthly REFSYS trend plots  
- Stability boxplots  
- Elevation & azimuth impact visualisations  
- Weather correlation graphs  
- Volatility comparison charts  

These outputs provide quantitative insights into GPS timing degradation under real-world conditions.

---

## 🛠 Tools & Technologies

- Python (Pandas, NumPy, Matplotlib)  
- CGGTTS time transfer format  
- RTKLib & RINEX preprocessing  
- Jupyter Notebooks  
- Statistical volatility & trend analysis  

---

## 📌 Key Findings

- Low-cost GNSS receivers exhibit large clock system offsets (REFSYS)  

### Signal stability varies with:

- Satellite geometry  
- Environmental conditions  
- Urban reflection effects  

- Weather and obstruction effects measurably increase volatility  
- Timing drift trends remain consistent across months but differ by environment  

---

## 🚀 Future Work

- Machine learning models for clock bias correction  
- Real-time GNSS error mitigation frameworks  
- Broader environmental datasets  
