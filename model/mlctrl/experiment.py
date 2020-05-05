import os
import re
import uuid
import json
import time
from contextlib import contextmanager

from matplotlib.pyplot import Figure

class Experiment():
    __is_running : bool

    name : str
    experiment_id : str
    out_dir : str

    model_filename : str
    metrics : dict

    def __init__(self, name:str):
        self.name = name
        self.__is_running = False
        
        self.metrics = dict()

        self.experiment_id = str(uuid.uuid4())
        self.out_dir = f"./output/{self.name}/{self.experiment_id}"
    
    @contextmanager
    def run(self):
        self.__is_running = True

        try:
            os.makedirs(self.out_dir)
        except:
            pass

        start = time.time()
        yield  self
        elepsed = time.time() - start

        with open( os.path.join(self.out_dir, "config.json"), 'w' ) as file:
            file.write(
                json.dumps({
                    "name": self.name,
                    "experiment_id": self.experiment_id,
                    "model_filename": self.model_filename,
                    "duration": elepsed,
                    "metrics": self.metrics,
                })
            )

        self.__is_running = False

    def log_metric(self, name : str, value : float):
        if not self.__is_running:
            raise ValueError("""
            It's necessary start the experiment using with statement

            Example:

            experiment = Experiment( ... )
            with experiment.run():
                experiment.log_metric( ... )  
            """)

        if not ( isinstance(value, float) or isinstance(value, list) ):
            raise ValueError("The metric value needs to be a float or a list of it")


        if isinstance(value, list):
            value = map(lambda x: float(x), value)

        if  not name in self.metrics:
            self.metrics[name] = value
        
        else:
            if not isinstance(self.metrics[name], list):
                self.metrics[name] = [ self.metrics[name] ]
            
            if isinstance(value, float):
                self.metrics[name].append(value)
            else:
                self.metrics[name] = self.metrics[name] + value
    
    def log_image(self, name : str, figure : Figure):
        if not self.__is_running:
            raise ValueError("""
            It's necessary start the experiment using with statement

            Example:

            experiment = Experiment( ... )
            with experiment.run():
                experiment.log_image( ... )  
            """)

        figure.savefig(os.path.join( self.out_dir, f"{name}.jpg" ))

    def log_model(self, model_path : str):
        if not self.__is_running:
            raise ValueError("""
            It's necessary start the experiment using with statement

            Example:

            experiment = Experiment( ... )
            with experiment.run():
                experiment.log_model( ... )  
            """)

        filename = re.search("[a-zA-Z0-9-_]*\\.[a-zA-Z]*$", model_path)

        if filename == None:
            raise ValueError("Invalid file name or extention")

        self.model_filename = filename[0]

        os.rename(model_path, os.path.join( self.out_dir, filename[0] ) )