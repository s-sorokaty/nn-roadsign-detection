import pandas 
import numpy as np

csv = pandas.read_csv('/mnt/HDD/archive/rtsd-frames/full-gt.csv')
classes = csv['sign_class'].unique()

for row in csv.iterrows():
    class_id = np.nonzero(classes == row[1]['sign_class'])[0][0]
    x_center = (row[1]['x_from']+row[1]['width']/2)/1000
    y_center = (row[1]['y_from']+row[1]['height']/2)/1000
    width = row[1]['width']/1000
    height = row[1]['height']/1000
    print(class_id, x_center, y_center, width, height)
