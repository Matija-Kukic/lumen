from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.responses import HTMLResponse  
from pathlib import Path
from pmdarima import auto_arima
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import base64
import io
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

app = FastAPI(debug=True)

# Load data
path = Path.cwd().parent.parent
filePath = str(path) + "/data_cleanup/train_data_price_corrected.parquet"
df = pd.read_parquet(filePath)


predictions = [66.1204873036973, 42.13618580295928, 47.306399700706, 12.462631925635533, 9.509987176765158, 
                  5.441063672357098, 8.319151240012145, 15.159606735197471, 24.157299521262797, 18.965896548509573, 
                  18.59458989001553, 22.05220463766649, 29.04581722432586, 24.8047543308673, 29.270103766325846, 
                  36.87794920250883, 34.273266483900926, 12.33392250156801, 25.054159429334472, 35.12921735629977, 
                  44.56500895579472, 43.73261874290899, 34.563936122701755, 26.307446229495902, 51.14578924762675, 
                  26.99050997755871, 42.078269722668885, 34.53287242878045, 31.513849925616604, 33.90730938034177, 
                  25.007058545931148, 23.420477289750533, 13.423834442337412, 35.44631623627591, 42.008118642432315, 
                  30.36235545305116, 35.78921716312473, 19.42040210563665, 23.319877292239664, 6.164526955438479, 
                  25.662064511633332, 34.28931424819955, 72.90566612358184, 65.93943816474874, 65.33419660545106, 
                  29.28357596571557, 27.608390736785, 41.586858555161015, 44.76111304819093, 48.077741304007965, 
                  27.532412851259412, 27.655027672854725, 82.48211104956542, 16.28672580969254, 24.05328660993959, 
                  25.228014155022283, 43.072005379356625, 30.247960575314078, 19.020403627834117, 11.024165728250406, 
                  18.24420050485943, 38.777319175541464, 43.84255692802889, 42.68583110308, 41.65839582274808, 
                  26.25318628487887, 27.964110056725037, 28.264782171289752, 32.28353257146265, 32.57007126156294, 
                  47.05314724571588, 49.667708897733725, 43.845668369171854, 24.88578760441046, 22.122657448148523, 
                  23.298696777621746, 27.72662372014449, 45.841442143253786, 38.48571705951574, 24.914796008595726, 
                  18.854186570932004, 17.032464506993197, 34.50713372471217, 36.390560462340765, 38.91184846500109, 
                  32.47959672653111, 27.8807798095569, 15.830241493850748, 14.976703194785715, 18.997331809709106, 
                  54.42463247363732, 75.96282217055587, 74.87013949483861, 23.631095073881117, 25.651994467384863, 
                  34.83112902922836, 47.91247032574989, 44.92683808379086, 55.94151487050854, 51.25326734005896, 
                  41.924539513724525, 42.31164160546607, 41.6674987124511, 17.714855092068227, 28.1633985095224, 
                  38.9286047570989, 70.91113396966755, 42.75331933480994, 27.48230684895878, 33.63147601074491, 
                  57.62392746911971, 59.22768839055242, 65.85528588145375, 59.56085911177386, 48.65191777518083, 
                  49.93741315297452, 51.29272977173942, 72.77560786724992, 60.554435687091306, 56.19345992369025, 
                  32.98253288795082, 34.32200035129036, 33.216166756695884, 36.400116832193056, 58.47046162886355, 
                  67.49621491748556, 72.54696404883784, 84.9062861970828, 68.38002800739949, 43.86812261461475, 
                  60.84167656455472, 64.66881593834366, 53.45904525553783, 72.9455183084331, 48.382134165365, 
                  97.186458034413, 24.321537838556623, 41.11723848885303, 92.61760332043566, 32.646276763939184, 
                  59.68344810510122, 96.99160899616994, 109.83046315728951, 103.89515941486175, 16.605139215808503, 
                  47.84886968558862, 34.52614012308241, 71.1168348060083, 54.90430766335749, 43.78819883977027, 
                  44.58343370162709, 89.67086696808444, 91.18225928961816, 37.245507510959, 47.34611294532052, 
                  49.60840141594, 67.46238577737043, 41.6034789388383, 70.03486885803437, 99.3191088267273, 
                  67.47689043882532, 26.804349792543466, 48.80391408682439, 99.90627949315297, 95.62712814066779, 
                  15.533378177656218, 79.35377264119312, 51.12844144431103, 46.88774984771892, 51.61298391994268, 
                  67.07575262316739, 54.97214419606679, 16.47412701783908, 48.87433478176512, 34.565342082303914, 
                  42.71585052922139, 27.21358750999753, 86.57403940971741, 78.9657602335013, 84.16305371834093, 
                  95.61809704769605, 70.36038015385819, 42.877220532758564, 30.894653411505207, 66.73015697298466, 
                  39.4275131217131, 48.29031372283318, 64.02586024145808, 33.234059450024304, 44.78712391534726, 
                  38.2256706213615, 69.50828170147076, 52.82025013097535, 46.286683884808774, 72.98111225219093, 
                  44.53207302102608, 49.34495860141095, 37.37271386135787, 41.02477997896817, 37.40715131332022, 
                  36.58965615964452, 73.26963394330595, 36.99789536366994, 42.431781622172, 60.2483433040729, 
                  37.03823929899158, 26.824324543287748, 48.07706055479245, 52.53158052323224, 62.226314272789104, 
                  47.88136666146715, 76.78530070011341, 31.126825492980903, 23.92315728406181, 43.212075626531785, 
                  61.50455852233428, 39.055899373067156, 24.899166360097563, 43.93459305540115, 79.6090895782446, 
                  75.51598436537626, 74.80692937850807, 96.97548358611891, 32.241345195562936, 32.992659119055844, 
                  49.48758381583499, 105.6288883442524, 94.5375966420182, 87.17090946693142, 89.32535717173614, 
                  89.21925737376934, 92.08308298674744, 102.7613298323432, 77.39177370473509, 62.96422471800556, 
                  89.9431038932577, 54.112226171640664, 43.89245126310615, 40.32957013528519, 78.07524495000206, 
                  39.59828035448934, 29.54704005984206, 44.92345856236778, 94.30080685364481, 64.30177119610512, 
                  43.118658013464774, 30.34352391033398, 78.1091962595989, 37.139831073621295, 64.92974552952214, 
                  77.60829043513202, 98.97406464997702, 92.73026380632773, 108.60953210868396, 72.2167923132827, 
                  55.18816241584117, 38.157256230395014, 87.64617444945694, 58.50293967138113, 72.17463879246806, 
                  78.30981008266289, 50.96192883024828, 28.52334092597232, 31.451050289256038, 62.75738576530727, 
                  41.78234733043017, 56.950589843318475, 43.33961354552322, 69.13963565563677, 53.20420676569391, 
                  59.03880353849685, 70.99025249099401, 37.4403532834846, 38.94433750302294, 51.68266122708594, 
                  95.9067335000707, 91.14328557756907, 68.50503756851218, 59.43854421809455, 48.263402126842394, 
                  45.36506432009927, 96.05956850601517, 98.66637801649178, 72.10715612043357, 43.73312320498069, 
                  49.6352261643507, 47.4869910063732, 49.986135554056645, 62.85624617890681, 45.928571570358514, 
                  80.59535876478715, 41.80088935993572, 41.59501602195721, 40.41383385155719, 45.51494306919887, 
                  37.926114608601516, 20.072257399927025, 16.109445225736163, 22.784572967066573, 48.92027321794189, 
                  36.90346963772828, 45.58425871146979, 51.837150561855424, 40.10380611828456, 15.153246448355437, 
                  12.333478151186494, 39.0241123696433, 38.78532243517666, 52.04107878138791, 62.05988608564185, 
                  39.111316854730724, 44.48876873411016, 17.066412012542802, 32.72627302603678, 51.515963207369026, 
                  65.82606724654488, 38.00041964155515, 20.967432532576588, 21.76002091965901, 42.640658439347575, 
                  66.46736536303528, 78.77875691621996, 76.8967179769842, 77.90013997420462, 21.901556668674708, 
                  20.803891825459246, 18.94071976965702, 40.12304573155287, 48.98507330647508, 51.3275320324944, 
                  40.827503163848974, 29.495307538493975, 31.191565453346453, 17.984066823385543, 31.961768146505637, 
                  34.529730028988446, 38.54053484167823, 37.13545868352166, 28.521678206186778, 19.840571549309335, 
                  22.705205631864146, 30.176295488061548, 33.67537601666603, 44.09501259369252, 28.79434918908756, 
                  18.05042970935868, 10.388408304803049, 14.183936824326478, 26.55269381310987, 42.842350380616885,
                  60.694175862972145, 36.242294526771005, 22.784627616018494, 19.8246871524296, 11.341981963172213, 
                  17.417818571197046, 15.518670249180266, 6.443655770319741, 0.9297065748094415, 3.794924983254702, 
                  4.7184197464357815, 2.8342713058541142, 14.68460237552463, 26.509466148006105, 56.20473738384552, 
                  53.945918714204005, 34.132897603796984]

# Generate list of dates from January 2009 to January 2010
date_range = [datetime(2009, 1, 1) + timedelta(days=i) for i in range(len(predictions))]

# Define endpoint for predictions
@app.get("/room-occupancy/plot", response_class=HTMLResponse)
async def room_occupancy_plot():
   try:
      '''
      room_occupancy = df[(df["cancel_date"].isna())]
      dates = []
      for index, row in room_occupancy.iterrows():
         delta = (row["date_to"] - row["date_from"]).days
         for i in range(delta):
            dates.append((row["date_from"] + pd.Timedelta(days=i), row["room_cnt"]))

      # Convert to DataFrame
      room_dates_df = pd.DataFrame(dates, columns=["date", "room_cnt"])

      # Group by date and sum room count
      room_occupancy = room_dates_df.groupby("date")["room_cnt"].sum().reset_index()

      # Apply logarithm function to guest_count data
      room_occupancy["room_count_log"] = np.log(room_occupancy["room_cnt"])

      # Seasonal differencing
      seasonal_difference = room_occupancy['room_count_log'].diff(periods=365)

      # Remove NaN values resulted from differencing
      seasonal_difference = seasonal_difference.dropna()

      seasonal_difference_df = seasonal_difference.to_frame(name='room_cnt').reset_index()
      seasonal_difference_df.columns = ['date', 'room_cnt']  
      seasonal_difference_df = seasonal_difference_df[seasonal_difference_df["date"] > "2009-01-01"]

      test = room_occupancy.iloc[1:368]
      train = room_occupancy.iloc[368:]

      # Best prediction
      mod = ARIMA(seasonal_difference_df["room_cnt"], order=(0, 0, 2), seasonal_order=(1, 0, 1, 7))
      mod = mod.fit()

      start = len(seasonal_difference_df)
      end = len(test) + len(seasonal_difference_df) - 1

      pred = mod.predict(start=start, end=end)

      original_train = room_occupancy.iloc[369:]
      prediction_list = list()
      for i, data in enumerate(train["room_count_log"]):
         prediction_list.append(data)
      for i, prediction in enumerate(pred):
         prediction_list[i] += prediction
      for i in range(len(prediction_list)):
         prediction_list[i] = math.exp(prediction_list[i])

      date_list = test.index.tolist()
   
      # Plot
      plt.figure(figsize=(50, 10))
      plt.plot(date_list, prediction_list, color="red", label="Predicted")
      plt.plot(test.index, test["room_cnt"], color="blue", label="Actual")
      plt.title("Ukupan broj zauzetih soba")
      plt.xlabel("Datum")
      plt.ylabel("Ukupan broj gostiju")
      plt.xticks(rotation=45)
      plt.legend()
      '''
      plt.figure(figsize=(10, 6))
      plt.plot(date_range, predictions, label='Predictions', color='blue')
      plt.title('Predictions Plot')
      plt.xlabel('Date')
      plt.ylabel('Predicted Value')
      plt.legend()
        
      # Convert plot to HTML
      img_bytes = io.BytesIO()
      plt.savefig(img_bytes, format='png')
      img_bytes.seek(0)
      img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
      plt.close()

      html_content = f"<img src='data:image/png;base64,{img_base64}' />"
      return html_content

   except Exception as e:
      return {"error": str(e)}

if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="127.0.0.1", port=8000)