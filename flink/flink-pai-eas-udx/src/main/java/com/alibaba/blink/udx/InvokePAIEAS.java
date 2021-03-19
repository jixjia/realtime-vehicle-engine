package com.alibaba.blink.udx;

import org.apache.flink.table.functions.FunctionContext;
import org.apache.flink.table.functions.ScalarFunction;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class InvokePAIEAS extends ScalarFunction {

    @Override
    public void open(FunctionContext context) {}

    private static final String POST_URL = "http://1208604289338550.vpc.cn-hangzhou.pai-eas.aliyuncs.com/api/predict/merck_anomaly_pai";
    private static final String AUTH_TOKEN = "ZjM5NjAxZDg5NTMwYzY5NDg3NTEyZTE4N2QyNWQzZWNjOTlhY2ZjNw==";

    // Main evaluator
    public String eval(Double rpm,
                       Double coolant_temp,
                       Double vapor_pressure,
                       Double cm_voltage,
                       Double torque_percent,
                       Double oxygen_rate) throws IOException {

        // JSON String need to be constructed for the specific resource
        String PAYLOAD = "[{\"rpm\":"+rpm+",\"coolant_temp\":"+coolant_temp+",\"vapor_pressure\":"+vapor_pressure+",\"cm_voltage\":"+cm_voltage+",\"torque_percent\":"+torque_percent+",\"oxygen_rate\":"+oxygen_rate+"}]";
        String jsonInputString = PAYLOAD;

        // Construct HTTP request conn
        URL obj = new URL(POST_URL);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Content-Type", "application/json; utf-8");
        con.setRequestProperty("Accept", "application/json");
        con.setRequestProperty ("Authorization", AUTH_TOKEN);
        con.setDoOutput(true);
        con.setConnectTimeout(5000);

        // Call endpoint
        try(OutputStream os = con.getOutputStream()) {
            byte[] input = jsonInputString.getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        // Response status code
        int responseCode = con.getResponseCode();

        // Get output streamer
        if (responseCode == HttpURLConnection.HTTP_OK) { //success
            try(BufferedReader br = new BufferedReader(
                    new InputStreamReader(con.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine = null;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }

                // Check binary classification probabilities
                Double p_0 = Double.parseDouble(response.substring(response.indexOf("p_0") + 5, response.indexOf(",")));
                Double p_1 = Double.parseDouble(response.substring(response.indexOf("p_1") + 5, response.indexOf("}")));

                if (p_0 >= p_1) {
                    System.out.println("Prediction result: Normal");
                    return "Normal";
                } else {
                    System.out.println("Prediction result: Abnormal");
                    return "Abnormal";
                }
            }
        } else {
            return "PAI-EAS Unavailable";
        }
    }

    @Override
    public void close() {}
}