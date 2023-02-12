import os
import pandas 
import cv2
import numpy as np
BASE_PATH = '/mnt/HDD/archive'

csv = pandas.read_csv(f'{BASE_PATH}/rtsd-frames/full-gt.csv')
print(csv['sign_class'].unique())

class_mean_length = 100
df2 = csv[(csv['sign_class'] == '1_17') & (csv['width'] >= 10) & (csv['height'] >= 10)][50:150] 
df1 = csv[(csv['sign_class'] == '1_23') & (csv['width'] >= 10) & (csv['height'] >= 10)][50:150]
df4 = csv[(csv['sign_class'] =='1_20_3') & (csv['width'] >= 10) & (csv['height'] >= 10)][0:100] 
df3 = csv[(csv['sign_class'] =='1_2') & (csv['width'] >= 10) & (csv['height'] >= 10)][0:100] 
df5 = csv[(csv['sign_class'] =='1_20_2') & (csv['width'] >= 10) & (csv['height'] >= 10)][0:100] 

df6 = csv[(csv['sign_class'] == '5_19_1') & (csv['width'] >= 10) & (csv['height'] >= 10)][50:150] 
df7 = csv[(csv['sign_class'] == '5_15_3') & (csv['width'] >= 10) & (csv['height'] >= 10)][0:100] 
df8 = csv[(csv['sign_class'] == '5_7_2') & (csv['width'] >= 10) & (csv['height'] >= 10)][0:100] 
df9 = csv[(csv['sign_class'] == '5_15_2') & (csv['width'] >= 10) & (csv['height'] >= 10)][0:100]
df10 = csv[(csv['sign_class'] == '5_15_7') & (csv['width'] >= 10) & (csv['height'] >= 10)][0:100]



csv = pandas.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10])

i = int(class_mean_length*0.7)
print(' HERE ',df1[i:-1]['sign_class'].value_counts())

train = pandas.concat([df1[0:i], df2[0:i], df3[0:i], df4[0:i], df5[0:i], df6[0:i], df7[0:i], df8[0:i], df9[0:i], df10[0:i]])
valid = pandas.concat([df1[i:-1], df2[i:-1], df3[i:-1], df4[i:-1], df5[i:-1], df6[i:-1], df7[i:-1], df8[i:-1], df9[i:-1], df10[i:-1]])

print(len(train), len(valid)) 
print(train['sign_class'].value_counts(), valid['sign_class'].value_counts())
with open(f'{BASE_PATH}/rtsd-frames/obj.names', 'w') as f:
    for sign_id in csv['sign_class'].unique():
        f.write(f'{sign_id}\n')

classes = np.loadtxt(f'{BASE_PATH}/rtsd-frames/obj.names', dtype='str')

def create_dataset(csv, ds_type):
    os.system(f"rm {BASE_PATH}/rtsd-frames/{ds_type}/*")
    with open(f"{BASE_PATH}/rtsd-frames/{ds_type}/{ds_type}.txt", 'w') as train_file:
        for row in csv.iterrows():
            img = cv2.imread(f"{BASE_PATH}/rtsd-frames/rtsd-frames/{row[1]['filename']}")


            #print(row[1]['filename'], img[row[1]['x_from'], row[1]['y_from']])
            #img[int(y_center):int(y_center)+1000, int(x_center)] = (255, 255 ,255)
            #img[row[1]['y_from'], int(x_center)] = (255, 255 ,255)
            #img[row[1]['y_from']:(row[1]['y_from']+ width), row[1]['x_from']] = (255, 255 ,255)
            #img[row[1]['y_from'], row[1]['x_from']:(row[1]['x_from']+ height)] = (255, 255 ,255)
            #img = cv2.resize(img, (608, 608))

                #print(f"{row[1]['filename']} {class_id} {x_center} {y_center} {width} {height}")
            #print(f"{row[1]['filename']} {class_id} {x_center} {y_center} {width} {height}")
            class_id = np.nonzero(classes == row[1]['sign_class'])[0][0]
            x_center = (row[1]['x_from'] + row[1]['width']/2)/img.shape[1]
            y_center = (row[1]['y_from'] + row[1]['height']/2)/img.shape[0]
            width = row[1]['width']/img.shape[1]
            height = row[1]['height']/img.shape[0]
            with open(f"{BASE_PATH}/rtsd-frames/{ds_type}/{row[1]['filename'].split('.')[0]}.txt", 'w') as f:
                f.write(f"{class_id} {x_center} {y_center} {width} {height}")
            cv2.imwrite(f"{BASE_PATH}/rtsd-frames/{ds_type}/{row[1]['filename']}", img)
            train_file.write(f"{BASE_PATH}/rtsd-frames/{ds_type}/{row[1]['filename']}\n")

create_dataset(train, 'train')
create_dataset(valid, 'valid')

 