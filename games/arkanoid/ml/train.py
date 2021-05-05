#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pickle
import numpy as np
import os
from sklearn.neighbors import KNeighborsClassifier


# beta 8.0.1
X_all = np.array([[0, 0, 0, 0 ,0 ,0]])
y_all = np.array([])



dir_path = '../log/'

all_file_list = os.listdir(dir_path)

for file in all_file_list:
    file_path = dir_path + file
    with open(file_path, 'rb') as f:
        data = pickle.load(f)

    print(data.keys())
    # In[2]:
    data['ml'].keys()
    # In[3]:
    data['ml']['scene_info']
    # In[4]:
    data['ml']['command']
    # In[13]:
    data['ml']['scene_info'][0], data['ml']['command'][-0]
    # In[19]:
    # 提取特徵
    scene_info = data['ml']['scene_info']
    command = data['ml']['command']

    # 提取特徵
    

    scene_info = data['ml']['scene_info']
    command = data['ml']['command']

    k = range(1, len(scene_info)-1)

    ball_x = np.array([scene_info[i]['ball'][0] for i in k])
    ball_y = np.array([scene_info[i]['ball'][1] for i in k])
    ball_speed_x = np.array([scene_info[i+1]['ball'][0] - scene_info[i]['ball'][0] for i in k])
    ball_speed_y = np.array([scene_info[i+1]['ball'][1] - scene_info[i]['ball'][1] for i in k])
    direction = np.where(np.vstack((ball_speed_x, ball_speed_y)) > 0, [[1],[0]], [[2],[3]]).sum(axis=0)  # x y: ++1, +-4, -+2, --3
    platform = np.array([scene_info[i]['platform'][0] for i in k])
    target = np.where(np.array(command) == 'NONE', 0,
                    np.where(np.array(command) == 'MOVE_LEFT', -1, 1))[1:-1]  # [0] SERVE_TO_RIGHT, [1897] None


    # In[27]:


    # 也可以使用 pandas
    X = np.hstack((ball_x.reshape(-1, 1),
                ball_y.reshape(-1, 1),
                ball_speed_x.reshape(-1, 1),
                ball_speed_y.reshape(-1, 1),
                direction.reshape(-1, 1),
                platform.reshape(-1, 1)))
    y = target


    X_all = np.concatenate((X_all, X))
    y_all = np.append(y_all, y)

X_all = np.delete(X_all, 0, axis=0)

# In[29]:


# train data

model = KNeighborsClassifier(n_neighbors=3)
print(model.fit(X_all, y_all))
print(model.score(X_all, y_all))


# In[30]:


with open('my_model.pickle', 'wb') as f:
    pickle.dump(model, f)


# In[ ]:




