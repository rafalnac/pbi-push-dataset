# Power BI Push Dataset

The project goal is to design cost effective real-time streaming solution in Power BI.

It has been inspired based on the solution provided by [SQLBI](https://youtu.be/vpD_PKtcTj8?si=8h-j4Rd9BlG9Q-x6)

The main focus of the project and its first phase is to develop a solution from the backend side, which has not been covered extensively in the mentioned solution.

### Architecture of the solution and how the application works:

1. Send data to Azure Event Hub.
2. Reveive data from Azure Event Hub.
3. Capture events and store them in blob container on ADL Gen2.
4. Create Power BI Push Dataset in Power BI Service.
5. Send events to Power BI Push Dataset
