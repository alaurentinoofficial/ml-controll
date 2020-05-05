import os
import joblib

from model.mlctrl import get_model_uri

model = joblib.load(get_model_uri("production-model"))

def predict(x):
    return model.predict(x)


if __name__ == "__main__":
    print(predict([ [32.0, 23.0] ]))