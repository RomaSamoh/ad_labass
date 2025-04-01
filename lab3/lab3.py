from spyre import server
import pandas as pd
import matplotlib.pyplot as plt

class DataAnalysisApp(server.App):
    title = "NOAA data vizualization"

    inputs = [
        {
            "type": "dropdown",
            "label": "NOAA data dropdown",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}],
            "key": "ticker",
            "action_id": "update_data"},
        
        {
            "type": "dropdown",
            "label": "Region dropdown",
            "options": [
                {"label": "Вінницька", "value": "1"},
                {"label": "Волинська", "value": "2"},
                {"label": "Дніпропетровська", "value": "3"},
                {"label": "Донецька", "value": "4"},
                {"label": "Житомирська", "value": "5"},
                {"label": "Закарпатська", "value": "6"},
                {"label": "Запорізька", "value": "7"},
                {"label": "Івано-Франківська", "value": "8"},
                {"label": "Київська", "value": "9"},
                {"label": "Кіровоградська", "value": "10"},
                {"label": "Луганська", "value": "11"},
                {"label": "Львівська", "value": "12"},
                {"label": "Миколаївська", "value": "13"},
                {"label": "Одеська", "value": "14"},
                {"label": "Полтавська", "value": "15"},
                {"label": "Рівенська", "value": "16"},
                {"label": "Сумська", "value": "17"},
                {"label": "Тернопільська", "value": "18"},
                {"label": "Харківська", "value": "19"},
                {"label": "Херсонська", "value": "20"},
                {"label": "Хмельницька", "value": "21"},
                {"label": "Черкаська", "value": "22"},
                {"label": "Чернівецька", "value": "23"},
                {"label": "Чернігівська", "value": "24"},
                {"label": "Крим", "value": "25"},
                {"label": "Київ", "value": "26"},
                {"label": "Севастополь", "value": "27"}],
            "key": "region",
            "action_id": "update_data"},
        
        {
            "type": "text",
            "label": "Select range",
            "key": "range",
            "value": "1-12",
            "action_id": "update_data"},
        
        {
            "type":'slider',
            "label": 'Select year',
            "min" : 1981,
            "max" : 2023,
            "key": 'year',
            "action_id" : "update_data"}]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Update"}]
    
    tabs = ["Plot", "Table"]

    outputs = [ { "type": "plot",
                    "id": "plot",
                    "control_id": "update_data",
                    "tab": "Plot"},
               
                { "type": "table",
                    "id": "table_id",
                    "control_id": "update_data",
                    "tab": "Table",
                    "on_page_load": True}]

    def getData(self, params):
        df = pd.read_csv('combined_data.csv')
        region = params['region']
        range = params['range']
        year = params['year']
        week_n, week_m = map(int, range.split('-'))
        
        df = df[df['area'] == int(region)]
        df = df[(df['Week'].between(week_n, week_m)) & (df['Year'] == int(year))]
        
        return df[['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']]

    def getRegionList(self, region):
        region_list = {
            "1": "Вінничини",
            "2": "Волині",
            "3": "Дніпропетровщини",
            "4": "Донеччини",
            "5": "Житомирщини",
            "6": "Закарпаття",
            "7": "Запоріжжя",
            "8": "Івано-Франківщини",
            "9": "Київщини",
            "10": "Кіровоградщини",
            "11": "Луганщини",
            "12": "Львівщини",
            "13": "Миколаївщини",
            "14": "Одещини",
            "15": "Полтавщини",
            "16": "Рівенщини",
            "17": "Сумщини",
            "18": "Тернопільщини",
            "19": "Харківщини",
            "20": "Херсонщини",
            "21": "Хмельницька",
            "22": "Черкащини",
            "23": "Чернівецька",
            "24": "Чернігівщини",
            "25": "Криму",
            "26": "Києва",
            "27": "Севастополя"
        }
        return region_list.get(region, "")


    def getPlot(self, params):
        df = self.getData(params)
        ticker = params['ticker']
        year = params['year']
        range = params['range']
        data_region = params['region']
        region= self.getRegionList(data_region)
        
        week_n, week_m = map(int, range.split('-'))

        pllt, ax = plt.subplots()
        df.plot(x='Week', y=ticker, legend=True, ax=ax, color='red')
        ax.set_ylabel(ticker)
        ax.set_xlabel("Тижні")
        ax.set_title(f"Графік для {region} за {year} рік протягом {week_n}-{week_m} тижнів")
        return pllt

    def getHTML(self, params):
        df = self.getData(params)
        return df.to_html()
    
if __name__ == '__main__':
    app = DataAnalysisApp()
    app.launch(port=7070)