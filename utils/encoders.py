from sklearn.preprocessing import LabelEncoder

class EncoderManager:
    def __init__(self):
        self.encoders = {}

    def fit_transform(self, df, columns):
        for col in columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.encoders[col] = le
        return df

    def transform(self, col, value):
        return self.encoders[col].transform([value])[0]
