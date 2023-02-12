import os
import pandas 
import cv2
import numpy as np
BASE_PATH = '/mnt/HDD/archive'

csv = pandas.read_csv(f'{BASE_PATH}/rtsd-frames/full-gt.csv')
df1 = csv[csv['sign_class'] == '1_23'][50:100]
print(df1)
df2 = csv[csv['sign_class'] == '1_17'][50:100] 
df3 = csv[csv['sign_class'] =='1_12_2'][0:50] 
df4 = csv[csv['sign_class'] =='1_20'][0:50] 
df5 = csv[csv['sign_class'] == '5_19_1'][50:100] 
df6 = csv[csv['sign_class'] == '5_15_3'][0:50] 
df7 = csv[csv['sign_class'] == '5_21'][0:50] 
df8 = csv[csv['sign_class'] == '5_15_2'][0:50]
csv = pandas.concat([df1, df2, df3, df4, df5, df6, df7, df8])
print(csv['sign_class'].value_counts())
i = int(len(csv)*0.7)
train= csv[0:i]
valid = csv[i:-1] 
print(len(train), len(valid))

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
            if row[1]['width']/img.shape[1]>=0.035 and row[1]['height']/img.shape[0]>=0.035:
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

 