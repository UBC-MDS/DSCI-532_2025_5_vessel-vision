# **Milestone 1 - Dashboard Proposal**

## **1. Motivation and Purpose**
### **Project Background**
We are a team of data science students at UBC, working on an interactive dashboard as part of our DSCI 532 course. Our goal is to build a **Vancouver AIS Vessel Tracking Dashboard** to enable real-time and historical analysis of ship movements in and around Vancouver. 

### **Target Audience**
Our dashboard is designed for:
- **Port of Vancouver Authorities**: To monitor vessel congestion, optimize port operations, and track vessel movement.
- **Shipping and Logistics Companies**: To track cargo ship arrivals/departures for supply chain efficiency.
- **Marine Researchers and Environmental Analysts**: To study shipping patterns and assess their environmental impact.
- **Coast Guard and Security Agencies**: To enhance maritime security and respond to potential threats.

### **Problem Statement**
The maritime industry in Vancouver requires real-time access to vessel movement data for decision-making. Traditional tools lack **interactive visualizations** and **custom filtering**, making it difficult to analyze trends efficiently. Our dashboard will address this gap by providing an intuitive and interactive platform to explore AIS (Automatic Identification System) data.

---

## **2. Description of the Data**
The dataset used in this project comes from the **NOAA AIS Data Archive**, specifically from [this source](https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2023/AIS_2023_12_31.zip). This dataset provides **USA national AIS data**, including vessel movements in and around Vancouver, Canada. It contains attributes such as:
- **MMSI (Maritime Mobile Service Identity)** – Unique vessel identifier
- **BaseDateTime** – Timestamp of the data entry
- **LAT, LON** – Latitude and Longitude (vessel position)
- **SOG (Speed Over Ground)** – Speed in knots
- **COG (Course Over Ground)** – Direction of vessel movement
- **Heading** – Vessel’s actual heading
- **VesselName** – Name of the ship
- **IMO, CallSign** – Additional ship identifiers
- **VesselType** – Cargo, Passenger, Tanker, etc.
- **Length, Width, Draft** – Vessel dimensions
- **Cargo Type** – Type of cargo being transported

### **Planned Data Processing and Feature Engineering**
- **Geographic Filtering**: Select only vessels **within the Vancouver region** (LAT ~49, LON ~-123).
- **Time-Based Trends**: Analyze vessel movement patterns over different time periods.
- **Vessel Traffic Density**: Visualize congested areas in the port.
- **Derived Variables**: Compute daily vessel counts, speed distributions, and time spent in certain zones.

---

## **3. Research Questions and Usage Scenarios**
### **Research Questions**
- How many vessels are active in Vancouver at different times of the day/week/month?
- What are the most common vessel types navigating Vancouver waters?
- How does vessel speed and movement pattern vary across different zones?
- Can we detect congested areas or bottlenecks in vessel traffic?

### **User Story: Port Operations Manager**
> John is a port operations manager responsible for overseeing vessel traffic at the **Port of Vancouver**. He logs into the dashboard to analyze vessel congestion in different port zones. Using the interactive filters, he selects the **current date** and views a **heatmap of vessel density**. He notices high congestion near **Burrard Inlet**, prompting him to **schedule additional tugboats** to assist incoming cargo ships. Additionally, he downloads a **weekly report** summarizing vessel arrivals and departures, which helps him optimize berthing schedules.

### **User Story: Marine Researcher**
> Lisa is an environmental researcher studying the **impact of vessel traffic on marine life**. She accesses the dashboard to explore **historical ship movement patterns**. By filtering the data for specific vessel types (tankers, cargo ships), she identifies areas with **high shipping frequency** near protected marine zones. This insight helps her advocate for new **conservation policies** and designated no-go zones to protect marine biodiversity.

---

## **4. App Sketch & Brief Description**



---


This proposal outlines our vision for the  AIS Vessel Tracking Dashboard. We aim to create a user-friendly tool for port authorities, researchers, and security agencies to **analyze vessel movement data** efficiently. 🚢📊

