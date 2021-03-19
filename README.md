# Realtime Vehicle Engine Anomaly Detection

&copy; 2021 Originally created by Jixin Jia for demo purpose

### About
This repository contains entire source code for biulding a real-time predictive solution demo on Alibaba Cloud International.

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

![img](https://jixjia-oss-singapore.oss-ap-southeast-1.aliyuncs.com/github/vehicle-anomaly-detection/architecture.png)

### Function Compute
A serverless platform for generating realistic sensor telemetries and send them in streams to our message hub backed by Kafka.

![img](https://jixjia-oss-singapore.oss-ap-southeast-1.aliyuncs.com/github/vehicle-anomaly-detection/demo_function_compute.gif)

### MQ for Kafka
A servie for running Kafka topics. We use it as message broker to let subscribers consume the telemtries with ease.

![img](https://jixjia-oss-singapore.oss-ap-southeast-1.aliyuncs.com/github/vehicle-anomaly-detection/demo_Kafka_on_MQ.gif)

### Realtime Compute (Flink)
Famous streaming processing technology backed by Alibaba Cloud, providing a robust and easy way for processing, transforming our incoming streaming data. We also use it to call the anomaly detection model for predictive diagnosis

![img](https://jixjia-oss-singapore.oss-ap-southeast-1.aliyuncs.com/github/vehicle-anomaly-detection/demo_realtime_processing_flink.gif)

### Machine Learning Platform for AI 
Alibaba Cloud's proprietary no-code/low-code service for fast prototyping an ML solution, and turn them into a REST API with single click.

![img](https://jixjia-oss-singapore.oss-ap-southeast-1.aliyuncs.com/github/vehicle-anomaly-detection/demo_anomaly_detection_modelling.gif)

### Visualizations
The live dashboard receives an update from the Hybrid Serving Analytical Processing system every 5 seconds and shows the latest status of our vehicle to end user

![img](https://jixjia-oss-singapore.oss-ap-southeast-1.aliyuncs.com/github/vehicle-anomaly-detection/demo_DataV_optimized.gif)
