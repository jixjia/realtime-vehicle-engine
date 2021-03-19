# Realtime Vehicle Engine Anomaly Detection

### About
This repository contains entire source code for biulding a real-time predictive solution demo on Alibaba Cloud International/

There is a video tutorial recorded in Japanese showing you how to build the solution end-to-end. 
The tutorial is made for the Alibaba Cloud Apasara Conference Big Data Hands-On session

### Business Scenario
Using a simulated sensor data we pretend there is a vehicle running 24/7 on street.
We will process the engine telemetry streams and send it off to an engine anomaly detection model for diagnosis. 
Results are then displayed on a live dashboard to inform end users about heathiness of our mock vehicle. Everything end-to-end in real-time

![img](https://jixjia-oss-singapore.oss-ap-southeast-1.aliyuncs.com/github/vehicle-anomaly-detection/Record_2021_03_19_15_45_20_419.gif)

### Architecture
The entire solution is built on Alibaba Cloud International site. 
This repository includes all source code necessary for building every components outlined in the architecture diagram.
![img](https://jixjia-oss-singapore.oss-ap-southeast-1.aliyuncs.com/github/vehicle-anomaly-detection/architecture_animated.gif)

### Visualizations
The live dashboard receives an update from the Hybrid Serving Analytical Processing system every 5 seconds and shows the latest status of our vehicle to end user
![img](https://jixjia-oss-singapore.oss-ap-southeast-1.aliyuncs.com/github/vehicle-anomaly-detection/demo_DataV_optimized.gif)
