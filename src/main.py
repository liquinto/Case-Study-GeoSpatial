from BaseModel import BaseModel
from cleaner import DataCleaner

def main():
    cleaner = DataCleaner()
    basemodel = BaseModel()

    discharge_ommen = cleaner.rws_discharge_cleaner("../data/discharge/Ommen.csv")
    X = discharge_ommen.loc[:, discharge_ommen.columns != 'ALFANUMERIEKEWAARDE']
    y = discharge_ommen['ALFANUMERIEKEWAARDE']
    basemodel.fit(X = None, y = y)
    predictions = basemodel.predict(X = X)
    print(predictions)


if __name__ == "__main__":
    main()


