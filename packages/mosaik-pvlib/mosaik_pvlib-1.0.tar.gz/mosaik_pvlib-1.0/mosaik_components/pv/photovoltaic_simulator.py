"""
@author: Fernando Penaherrera

Adapter for the MOSAIK-API for connection of the PVSystem class 
for simulation of a photovoltaic system.

TODO: Implement Raise value errors

"""

import itertools
import mosaik_api_v3
from mosaik_components.pv.configurations import generate_configurations
from mosaik_components.pv import photovoltaic

meta = {
    "type": "time-based",
    "models": {
        "PVSim": {
            "public": True,
            # each of the parameters can be manually configured as well
            "params": list(generate_configurations().keys()),
            "attrs": [
                "P[MW]",  # output active power [MW]
                "Q[MVar]",  # output reactive power [MVar]
                "GHI[W/m2]",  # input direct normal irradiation [W/m2]
                "Wind[m/s]",  # input Wind Speed [m/s]
                "Air[C]",  # input Air Temperature Speed [C]
                "Air[Pa]",  # input Air Pressure [Pa]. Can be None
            ],
        },
    },
    "extra_methods": [
        "get_entities",  # Provides a list with the generated entities
    ],
}
DATE_FORMAT = "YYYY-MM-DD HH:mm:ss"


# ------------INPUT-SIGNALS--------------------
# GHI           input direct normal irradiation [W/m2]
# windSpeed     input Wind Speed [m/s]
# airTemp       input Air Temperature Speed [C]
# pressure      input Air Pressure [Pa]. Can be None

# ------------OUTPUT-SIGNALS--------------------
# P             output active power [MW]
# Q             output reactive power [MVar]


class PVSimulator(mosaik_api_v3.Simulator):
    """
    Simulator to be coupled in the co-simulation framework.
    """

    def __init__(self):
        """Class constructor"""
        # all methods in the inheritance chain are called.
        super(PVSimulator, self).__init__(meta)

        self.gen_neg = False  # true if generation is negative for coupling with PandaPower

        self.sid = None
        self.cache = None

        # Dictionaries for handling data
        self.entities = {}
        self.eid_counters = {}

        self.simulator = photovoltaic.Simulator()

    def init(
        self,
        sid,
        time_resolution=60,
        start_date=None,
        step_size=60,
        gen_neg=True,
        calc_mode="detailed",
        pv_data=None,
    ):
        """Initialization of the instances. Uses arguments to construct the PV Systems

        Args:
            sid (str): String ID. Provided by the MOSAIK API
            time_resolution (int, optional): Time resolution for the simulation . Defaults to 60.
            start_date (str, optional): Start date in format in format "YYYY-MM-DD hh:mm:ss". Defaults to None.
            step_size (int, optional):  Simulation step size. Defaults to 60.
            gen_neg (bool, optional): True if Generation output is with negative symbol. Defaults to True.
            calc_mode (str, optional): Calculation mode: "simple" or "detailed". Defaults to "detailed".
            pv_data (dict, optional): Dictionary with the PV configuration data. Defaults to None.

        Returns:
            _type_:
        """
        self.sid = sid
        self.gen_neg = gen_neg
        self.time_resolution = time_resolution
        self.start_date = start_date
        self.step_size = step_size
        self.calc_mode = calc_mode

        self.pv_data = pv_data

        return self.meta

    def create(self, num, model_type):
        """Create a number of instances of the PV model

        Args:
            num (int): Number of instances to be created
            model_type (PVSystem): Class of the model

        Returns:
            list: List with the created entities each as a dictionary
        """

        entities = []

        # creation of the entities:
        for i in range(num):
            pv_model_params = self.pv_data[str(i)]
            eid = "{}_{}".format(model_type, i)  # Entities IDs
            model = self.simulator.add_model(
                start_date=self.start_date, calc_mode=self.calc_mode, **pv_model_params
            )
            # create full id
            full_id = self.sid + "." + eid

            self.entities[eid] = {
                "ename": eid,
                "etype": model_type,
                "model": model,
                "full_id": full_id,
            }

            entities.append({"eid": eid, "type": model_type, "rel": []})

        return entities

    def step(self, time, inputs, max_advance=3600):
        """Advance model time

        Args:
            time (int): Time step size in seconds.
            inputs (dict): Input data for modelling.
            max_advance (int, optional): Maximum advance in seconds. Defaults to 3600.
        """
        self.cache = {}
        for eid, attrs in inputs.items():

            for attr, vals in attrs.items():
                pressure = None
                dni = None
                dhi = None
                windSpeed = None
                airTemp = None
                if attr == "GHI[W/m2]":
                    ghi = list(vals.values())[0]

                if attr == "Wind[m/s]":
                    windSpeed = list(vals.values())[0]

                if attr == "Air[C]":
                    airTemp = list(vals.values())[0]

                if attr == "Air[Pa]":
                    pressure = list(vals.values())[0]

            dict_input = {
                "ghi": ghi,
                "dni": None,
                "dhi": None,
                "temp_air": airTemp,
                "wind_speed": windSpeed,
                "pressure": pressure,
            }

        self.simulator.step(self.step_size, dict_input)

        return time + self.step_size

    def get_data(self, outputs):
        """Fetches the simulation results as data for the next simulator

        Args:
            outputs (dict): Dictionary with output results

        Raises:
            ValueError: Unknown output attribute

        Returns:
            dict: Dictionary with the output data
        """
        data = {}
        for eid, attrs in outputs.items():

            data[eid] = {}
            for attr in attrs:
                if attr not in ["P[MW]", "Q[MVar]"]:
                    raise ValueError('Unknown output attribute "{}"'.format(attr))
                if attr == "P[MW]":
                    data[eid][attr] = getattr(self.entities[eid]["model"], 'P') / 10**6 # W -> MW
                elif attr == "Q[MVar]":
                    data[eid][attr] = getattr(self.entities[eid]["model"], 'Q') / 10**6 # W -> MW

        return data

    def get_entities(self):
        """Provides a list with the entities as dict

        Returns:
            list: List of entities as dict
        """
        # return entities of API
        return self.entities


if __name__ == "__main__":
    pass
