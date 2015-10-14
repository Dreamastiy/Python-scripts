import cv2
import numpy as np
import pandas as pd
from scipy import ndimage
import matplotlib.pyplot as plt
import matplotlib
import math as m
from skimage import morphology
import cv2
import csv

#gps_data = np.genfromtxt(, delimiter=';')
gps_data = pd.read_csv(filepath_or_buffer = 'C:\\Users\Dmi\\Desktop\\MatLab\\Python scripts\\Tracking\\Dasha_1.csv', sep = ';', decimal = ',')
#help(genfromtxt)
#print gps_data.iloc[:,1]
def get_Dims(df):
    """get min, max and dims of tracks"""
    lon_min = min(df.iloc[:,0])
    lon_max = max(df.iloc[:,0])
    lat_min = min(df.iloc[:,1])
    lat_max = max(df.iloc[:,1])
    lon_dim = lon_max - lon_min
    lat_dim = lat_max - lat_min
    return lon_dim , lat_dim, lon_min, lon_max, lat_min, lat_max
    
#temp = get_Dims(gps_data)
#print gps_data.iloc[:,1]

def get_Matrix(df, res):
    """generating matrix of data"""
    temp = get_Dims(df)
    lon_q = temp[0]    
    lat_q = temp[1]
    lon_min = temp[2]
    lat_min = temp[4]
    lon = df.iloc[:, 0]
    lat = df.iloc[:, 1]
    a = np.zeros(shape=(int(lon_q * 10 ** res), int(lat_q * 10 ** res)))    
    l = len(df.iloc[:,1])
    #print (0,l-1)
    #print lon_q, lat_q
    for x in range(0, l - 1):
        #print x
        xx = int((lon[x] - lon_min) * 10 ** res) - 1
        yy = int((lat[x] - lat_min) * 10 ** res) - 1
        #print xx, yy
        a[xx, yy] = 1.0
        
    return a


tt = get_Matrix(gps_data, 5)  
plt.imshow(tt, aspect = 1)
plt.show()

fig, ax = plt.subplots(figsize=(10, 200))
blurred_track = tt
#blurred_track = ndimage.gaussian_filter(tt, sigma=5)
ax.imshow(blurred_track)# , aspect = 0.1)
#ax.show()
#print temp
#blurred_track[blurred_track < 0.01] = 0
#blurred_track[blurred_track > 0] = 1 
#plt.imshow(blurred_track, aspect = 0.1)
median_track = blurred_track
#median_track = ndimage.median_filter(blurred_track, size = 5)
plt.imshow(median_track, aspect = 1)

im = np.array(median_track * 255, dtype = np.uint8)
#threshed = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)
#im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im = cv2.threshold(im, 0, 255, cv2.THRESH_OTSU)[1]
im = morphology.skeletonize(im > 0) * 1.0
print im
print type(im).__name__



resized_image = cv2.resize(im, (200, 1500)) 
cv2.imshow("Final", resized_image)

def restore_Matrix(df_or, df_f ,res):
    temp = get_Dims(df_or)
    lon_q = temp[0]    
    lat_q = temp[1]
    lon_min = temp[2]
    lat_min = temp[4]
    lon = df_or.iloc[:, 0]
    lat = df_or.iloc[:, 1]
    l = []
    for (x,y), value in np.ndenumerate(df_f):
        if im[x, y] == 1:
            #print x, y
            l.append([lon_min + float(x) / 10 ** res, lat_min + float(y) / 10 ** res])
    return l
    
results = restore_Matrix(gps_data, im, 5)
print results

with open("C:\\Users\Dmi\\Desktop\\MatLab\\Python scripts\\Tracking\\result.csv", "wb") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerows([['Longitude', 'Latitude']])
    writer.writerows(results)


