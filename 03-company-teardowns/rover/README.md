Data fetch and visualization code behind the Rover Group marketplace analytics teardown published on Medium.

What This Is
This repo contains the Python script used to fetch, clean, and visualize Rover Group's public SEC 8-K filing data for a company teardown. Three charts are produced:
•	Chart 1: New vs Repeat Bookings and Repeat Share -- Q4 2021 to Q3 2023
•	Chart 2: Acquisition Timeline post-Blackstone -- Oct 2024 to Jan 2026
•	Chart 3: YoY Growth Rate Divergence -- GBV vs New vs Repeat Bookings

Data Sources
•	Rover SEC 8-K Q4 2022: sec.gov/Archives/edgar/data/1826018/000182601823000008/
•	Rover SEC 8-K Q2 2023: sec.gov/Archives/edgar/data/0001826018/000182601823000044/
•	Rover SEC 8-K Q3 2023: sec.gov/Archives/edgar/data/0001826018/000182601823000053/
•	Acquisition history: GlobeNewswire press releases + Wikipedia + Tracxn

Usage
pip install matplotlib pandas numpy
python rover_analytics.py

Outputs three dark-themed PNG files at 180 DPI, ready to embed in a Medium post.

Read the Full Teardown
Medium post: medium.com/@895akshita/b90acd9d9f39
LinkedIn:    linkedin.com/in/akshita-bhalla

CHART ASSET GUIDE

rover_chart1_bookings_breakdown.png  -- Medium Section 2 (What the Data Shows) + attach to LinkedIn standalone post as the image
rover_chart2_acquisition_timeline.png  -- Medium Section 3 (Why the Gap Exists) only
rover_chart3_growth_gap.png  -- Medium Section 2, second visual after the first chart

