import json
import joblib
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import SGDClassifier
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score


def save_metrics(metrics, output_name):
    with open(output_name, 'w') as file:
        file.write( json.dumps(metrics) )


def save_image(figure, output_name):
    figure.savefig(output_name)


if __name__ == "__main__":
    #########################
    X, y = make_moons(n_samples=100, noise=0.13)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
    #########################


    #########################
    model = SGDClassifier(alpha=0.001, max_iter=100)
    model.fit(X, y)
    #########################


    #########################
    train_output = model.predict(X_train)
    test_output = model.predict(X_test)
    #########################


    #########################
    metrics = {}

    metrics["train_f1"] = f1_score( y_train, train_output )
    metrics["train_recall"] = recall_score( y_train, train_output )
    metrics["train_accuracy"] = accuracy_score( y_train, train_output )

    metrics["test_f1"] = f1_score( y_test, test_output )
    metrics["test_recall"] = recall_score( y_test, test_output )
    metrics["test_accuracy"] = accuracy_score( y_test, test_output )

    save_metrics(metrics, "./output/metrics.json")
    #########################


    #########################
    joblib.dump(model, './output/model.pkl')
    #########################