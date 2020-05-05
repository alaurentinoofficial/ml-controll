import os
import json

registred_models = {}

def get_model_uri(model_name : str):
    load_registred_models()

    if not model_name in registred_models:
        raise ValueError("Model was not registred")

    return registred_models[model_name]

def load_registred_models():
    global registred_models

    with open("./model/mlctrl/config.json", 'r') as file:
        registred_models = json.loads("".join(file.readlines()))
    
def save_registred_models():
    global registred_models

    try:
        with open("./model/mlctrl/config.json", 'w') as file:
            file.write(json.dumps(registred_models))
    except:
        registred_models = {}

def registry_model_to_production(model_name : str, experiment_name : str, experiment_id : str):
    global registred_models

    if registred_models == {}:
        load_registred_models()

    path = f"./output/{experiment_name}/{experiment_id}"
    config_path = os.path.join(path, "config.json")

    with open(config_path, 'r') as file:
        result = json.loads("".join(file.readlines()))

        if not "model_filename" in result:
            raise ValueError("Experiment don't logged a model!")

        registred_models[model_name] = os.path.join( path, result["model_filename"] )
        save_registred_models()