import pickle
import pandas as pd
data = pd.read_csv('D:\Downloads\T1.csv')
pickle.dump(data, open('data.pkl', 'wb'))
data = pickle.load(open('data.pkl', 'rb'))
