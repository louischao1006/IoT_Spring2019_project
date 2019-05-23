[1] Data.csv: 
   The dataset gathered in this project which contains CO2 concentration, network delay, time, three sound amplitudes, temperature data and the occupancy of Mudd 1214.
[2] finalgather.py:
   The loop lasting python program, which is ran on the intel Edison. It get the sample value from sensors, and import into DynamoDB.
[3] finalml.ipynb:
    The data processing file, including part of paraphrase, normalization and visualization. The prediction model in built, and accuracy and F1 score are calculated here.
[4] realtime.py:
    The loop lasting python program, which only renew the dynamodb, to make it only contain the latest features.
[5] server.py:
    The interface setting program including interface layout and making prediction.
[6] serverfunction.py:
    The library-like, provides function for server.py
