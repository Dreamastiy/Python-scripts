
# coding: utf-8

# In[50]:

get_ipython().magic(u'matplotlib inline')
# ��������� ��� ������ ����
import numpy as np
import pandas as pd
import matplotlib
from pylab import *

from sklearn import ensemble
from sklearn.grid_search import GridSearchCV


# In[51]:

# ��������� ������ 
loc_train = "D:\\Tomato2.csv"
df_train = pd.read_csv(loc_train, error_bad_lines=False, sep = ";", decimal = ',' )
feature_cols = [col for col in df_train.columns if col not in ['Date','Nomalized', 'Year']]


# In[52]:

# ������� ������������� ������� 0,6 �� ��
X_train = df_train[feature_cols].iloc[1:600]
y = df_train['Nomalized'].iloc[1:600]


# In[53]:

# ������� ��� � ����������� �� ���������
clf = ensemble.RandomForestRegressor(n_estimators = 500, n_jobs = -1, oob_score = 1)
clf.fit(X_train, y)


# In[54]:

# ������ ����� �� ����� ���������� � ������� ������������ � ����� �������� �������
model = ensemble.RandomForestRegressor()
n_e = np.array([100, 200, 250]) # ���������� ��������
msl = np.array([1,2,4]) # ����������� ���������� �������� � ��������� ����
mf = np.array([1,2,4,8,16,30])

grid1 = GridSearchCV(estimator=model, param_grid=dict(n_estimators=n_e, min_samples_leaf=msl, max_features = mf))
grid1.fit(X_train, y)


# In[55]:

# ������� ��������� ������ �� ���� �������
X_train = df_train[feature_cols]
y = df_train['Nomalized']

# ������� ������������ ������ ��-��������� � � ������� ������������ ��������
vals_auto = clf.predict(X_train)
vals_grid = grid1.predict(X_train)


# In[56]:


# ������� �������
# ����������� ��������
t = range(1, 953, 1)
plot(t, y)
xlabel('Days from 2013')
ylabel('Season coeff')
title('Seasonality fact')
grid(True)
show()

# ������� ���������� �� ������������ �������� ������ � ����������� �� ���������
plot(t, (y - vals_auto) / y * 100.)
xlabel('Days from 2013')
ylabel('Season deviation, [%]')
title('Random forest auto deviation from fact')
grid(True)
show()

# ������� ���������� �� ������������ �������� ������ � ����������� �� ���������
plot(t, (y - vals_grid) / y * 100.)
xlabel('Days from 2013')
ylabel('Season deviation, [%]')
title('Random forest grid search deviation from fact')
grid(True)
show()


# In[57]:

print grid1.best_score_
print grid1.best_estimator_
print grid1.best_params_