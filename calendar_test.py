import pandas as pd
import numpy as np
pollutant = [1,2,3,34,56,23,34,23,12,12,1,3,7,45,34,94,24,3,2,4,7,5,43,23,9,10,84,64,54,35,48,10,23,12,1,2]
pollutant_name = 'pm10.ML'

limit = {
                'pm25.ML': 35,
                'pm10.ML': 35,
                'pm1.ML': 35,
                'correctedNO': 45,
                'co.ML': 9000,
                'no2.ML': 1000,
                'o3,ML': 1000
            }

# stringa = "hathoseareinteresting"
# print(stringa[2:-2])

smooth = 24
conv = [1/smooth] * smooth
offload = smooth // 2
variable = list(pollutant)
conv_list=np.convolve(conv,variable)
conv_results = []
for item in conv_list:
    conv_results.append(1) if item >= limit[pollutant_name] else conv_results.append(0)

conv_results = conv_results[offload-1:-offload]
new_list = [conv_results[i:i + 24] for i in range(0, len(conv_results), 24)]
final_results = []
for list in new_list:
    final_results.append(1) if 1 in list else final_results.append(0)

print(conv_results)
print(final_results)
# print(len(pollutant))

