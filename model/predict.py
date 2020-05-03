import os
import joblib

model = joblib.load("./output/model.pkl")

def predict(x):
    return model.predict(x)


if __name__ == "__main__":
    print(predict([ [32.0, 23.0] ]))