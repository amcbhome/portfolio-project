# Prescriptive Analytics Engine: Network Logistics Optimization (ACCA SBL Case Study)

## 📌 Business Case Overview
This repository contains an optimization engine that transitions a 3x3 logistics network problem from static spreadsheet environments into a scalable data application. 

Based on the ACCA Strategic Business Leader (SBL) framework for minimizing corporate transportation overhead, this application uses Python's `PuLP` library to run a transportation algorithm. It calculates the most efficient distribution routes from three inventory depots to three regional retail hubs.

## 📊 Business Intelligence Comparison
| Metric Layer | Excel Solver Baseline | Prescriptive Python Engine |
| :--- | :--- | :--- |
| **Total Logistics Cost** | £812,500 | £812,500.00 |
| **Calculation Engine** | Local Simplex LP Add-in | Scalable `PuLP` Linear Solver |
| **Data Ingestion** | Static Grid Cells | Multi-variable Streamlit Inputs |
| **Operational Slack** | Explicit Worksheet Formulas | Dynamic Software-Layer Metrics |

## 💡 Strategic Insights & Slack Management
* **Store Demand Saturation:** Store 1 and Store 3 run at absolute capacity limits, meaning their constraint boundaries are binding. Store 2 shows an operational slack of 150 unallocated delivery spaces.
* **Supply Constraints:** All three supply depots show zero inventory slack, meaning every available unit is fully utilized across the network. This highlights that total product supply, rather than store capacity, is the primary constraint limiting further distribution volume.
