import numpy as np
import math
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from scipy.stats import boxcox
from scipy.stats import shapiro 
from scipy.stats import lognorm
from scipy.stats import kstest,norm
from scipy.stats import lognorm
from pmdarima import auto_arima
import warnings

path = Path.cwd().parent.parent
filePath = str(path) + "/data_cleanup/second_dataset/train_data_price_corrected.parquet"
df = pd.read_parquet(filePath)

df['date_from'] = df['date_from'] + pd.DateOffset(years=2)
df['date_to'] = df['date_to'] + pd.DateOffset(years=2)
df = df[df['date_from'] > '2010-1-2']
df = df[df['date_to'] < '2011-4-25']
df = df[df['date_to'] > '2010-1-2']
print(df.info())
df.to_parquet("test.parquet")
