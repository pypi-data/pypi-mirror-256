"""
@author: Fernando Penaherrera @UOL/OFFIS

Module for the adaptation of the PVLib library as a MOSAIK class.

This class creates a PV System (based on the PVLib library classes) with physical and geographical properties
Calculation of power output are done via meteorological data input and with the timestamp for solar geometry calculations.

The class includes the step() method to advance the simulation accordingly.
"""


import arrow
import pvlib
import pandas as pd
import datetime
from mosaik_components.pv.common import normalize_product_names
from mosaik_components.pv.configurations import Scenarios, generate_configurations
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.pvsystem import PVSystem as PVLibSystem
import numpy as np
import warnings
from pvlib._deprecation import pvlibDeprecationWarning

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=pvlibDeprecationWarning)

DATE_FORMAT = "YYYY-MM-DD HH:mm:ss"


class PVSystem(object):
    """Generates a class PVSystem with the methods for calculating
    the PV power given the weather values at a certain time

    "simple" and a "detailed" calculation modes are considered

    Args:
        object (Class): Generic class inheritance

    Raises:
        ValueError: "Calculation mode needs to be 'simple' or 'detailed'"
    """

    P = 0
    Q = 0
    results = ["P", "Q"]

    def __init__(self, start_date="2020-06-12 12:00:00", calc_mode="detailed", **kwargs):
        """Creates the system and passes the configuration arguments.

        Args:
            start_date (str, optional): String with date in the format "YYYY-MM-DD HH:MM:SS". Defaults to "2020-06-12 12:00:00".
            calc_mode (str, optional): Calculation. Defaults to "detailed".

        Raises:
            ValueError: "Calculation mode needs to be 'simple' or 'detailed'"
        """

        if calc_mode not in ["simple", "detailed"]:
            raise ValueError("Calculation mode needs to be 'simple' or 'detailed'")

        self.calc_mode = calc_mode

        # Timestamps: Converts the string of time into a readable datetime
        # format.

        # This is used by the PVLib calculator
        self.datetime = pd.date_range(start_date, periods=1, freq="H")

        # This one is used by the step function in MOSAIK
        self.date = arrow.get(start_date, DATE_FORMAT)

        # Build the PV System with the given configuration
        self.set_configuration(**kwargs)

        # Build a simple system based on the pvLib.ModelChain()
        self.build_system()

    def set_configuration(self, **kwargs):
        """Sets the configuration of the PV Panel based on the input dictionary
        Passes default values if no appropriate key is found
        """

        # Read the arguments in the configuration dictionary.
        # Geometry
        self.latitude = kwargs.get("latitude", 53.14)
        self.longitude = kwargs.get("longitude", 8.20)
        self.elevation = kwargs.get("elevation", 0)
        self.inclination = kwargs.get("inclination", 0)
        self.timezone = kwargs.get("timezone", "Europe/Berlin")
        self.location_name = kwargs.get("timezone", "Germany")
        self.surface_azimuth = kwargs.get("surface_azimuth", 180)
        self.surface_tilt = self.latitude + self.inclination
        self.albedo = kwargs.get("albedo", 0.1)

        # Technical parameters
        if self.calc_mode == "simple":

            # Simplified Technical parameters
            self.p_dc = kwargs.get("p_dc", 0)

            # Temperature coefficient in units of 1/C. Typically -0.002 to -0.005
            # per degree C.
            self.module_temp_coeff = kwargs.get("module_temp_coeff", -0.003)

            # Dictionary with the module parameters (instead of full name of
            # module
            self.module_params = dict(pdc0=self.p_dc, gamma_pdc=self.module_temp_coeff)

            self.p_ac = kwargs.get("p_ac", self.p_dc)
            self.inverter_eff = kwargs.get("inverter_eff", 1)
            self.inverter_params = dict(pdc0=self.p_ac / self.inverter_eff)
            self.temp_model_params = TEMPERATURE_MODEL_PARAMETERS["sapm"]["open_rack_glass_polymer"]

        if self.calc_mode == "detailed":

            # A more detailed dictionary with more arguments for calculation
            self.modules_library = kwargs.get("modules_library", "SandiaMod")
            self.inverters_library = kwargs.get("inverters_library", "cecinverter")
            self.module = kwargs.get("module", "Canadian_Solar_CS5P_220M___2009_")
            self.inverter = kwargs.get("inverter", "ABB__MICRO_0_25_I_OUTD_US_208__208V_")
            self.array = kwargs.get("array", [1, 1])

            # Normalize module names in case they contain unwanted characters
            self.module = normalize_product_names(self.module)
            self.inverter = normalize_product_names(self.inverter)

            # Temperature Model Parameters
            self.tmp = kwargs.get("temperature_model_parameters", {"sapm": "open_rack_glass_glass"})
            self.temp_model_params = TEMPERATURE_MODEL_PARAMETERS[list(self.tmp.keys())[0]][
                list(self.tmp.values())[0]
            ]

    def set_date(self, date):
        """Sets the date of the current object to the given vale
        Useful for not creating copies of the class when only a change in the Datetime is required

        Not used by MOSAIK

        Args:
            date (str): String with date in the format "YYYY-MM-DD HH:MM:SS"
        """
        # Timestamp
        self.datetime = pd.date_range(date, periods=1, freq="H")
        self.date = arrow.get(date, DATE_FORMAT)

    def step(self, step_size):
        """Advance the current PVSystem time. Resets the timestamps of the class.

        Args:
            step_size (int): Interval in seconds of the time step for co-simulations
        """
        self.date = self.date.shift(seconds=step_size)
        a = self.datetime[0]
        a += datetime.timedelta(seconds=step_size)
        self.datetime = pd.date_range(a, periods=1, freq="H")

    def build_system(self):
        """Builds a PV System based on the PVLibSystem() class.
        Creates a ModelChain() class for calculation based on the PVSysstem and Location
        """
        # Create a Location object based on the passed properties
        self.location = Location(
            latitude=self.latitude,
            longitude=self.longitude,
            tz=self.timezone,
            altitude=self.elevation,
            name=self.location_name,
        )
        if self.calc_mode == "simple":
            # Create a PVSystem based on the configuration
            self.system = PVLibSystem(
                surface_tilt=self.surface_tilt,
                surface_azimuth=self.surface_azimuth,
                module_parameters=self.module_params,
                inverter_parameters=self.inverter_params,
                temperature_model_parameters=self.temp_model_params,
            )

            # Create a Model Chain
            self.model_chain = ModelChain.with_pvwatts(
                system=self.system, location=self.location, name=self.location_name
            )

        if self.calc_mode == "detailed":
            # Get the inverter and modules from the PVLIB libraries
            self.get_technologies()

            # Now with an array
            module_parameters = self.module
            inverter_parameters = self.inverter

            self.system = PVLibSystem(
                module_parameters=module_parameters,
                inverter_parameters=inverter_parameters,
                modules_per_string=self.array[0],
                strings_per_inverter=self.array[1],
                surface_tilt=self.surface_tilt,
                surface_azimuth=self.surface_azimuth,
                albedo=self.albedo,
                temperature_model_parameters=self.temp_model_params,
            )

            self.model_chain = ModelChain(self.system, self.location)

    def get_technologies(self):
        """Sets the technologies based on the PVLib libraries
        Used in the "detailed" calculation mode
        """
        modules = pvlib.pvsystem.retrieve_sam(self.modules_library)
        inverters = pvlib.pvsystem.retrieve_sam(self.inverters_library)
        self.module = modules[self.module]
        self.inverter = inverters[self.inverter]

    def power(self, ghi=1000.0, dni=None, dhi=None, temp_air=None, wind_speed=None, pressure=None):
        """Sets the value of the parameter self.power to the output power.

        Calculates the output AC power based on the input environmental parameters

        If the array is 0*0 (dummy system) the power is always 0

        Args:
            ghi (float, optional): Global Horizontal Irradiation, W/m2. Defaults to 1000.
            dni (float, optional): Direct Normal Irradiation, W/m2. Defaults to None.
            dhi (float, optional): Direct Horizontal Irradiation, W/m2. Defaults to None.
            temp_air (float, optional): Air Temperature, C. Defaults to None.
            wind_speed (float, optional): Wind Speed, m/s. Defaults to None.
            pressure (float, optional): Air pressure, Pa. If value not given, takes from the altitude of the location. Defaults to None.
        """

        if self.calc_mode == "detailed":
            if self.array[0] * self.array[1] == 0:
                self.dc = 0
                self.ac = 0
                self.eff = np.nan
                self.P = self.ac

            self.P = self.calculate_power(ghi, dni, temp_air, wind_speed, pressure)

        if self.calc_mode == "simple":
            self.P = self.calculate_power(ghi, dni, temp_air, wind_speed, pressure)

    def prepare_weather_df(
        self, ghi=1000.0, dni=None, dhi=None, temp_air=20.0, wind_speed=0.0, pressure=None
    ):
        """Creates a pandas Dataframe with the mentioned parameters.
        If dni or dhi are none, they are calculated using PVLib methods.

        Args:
            ghi (float, optional): Global Horizontal Irradiation, W/m2. Defaults to 1000.
            dni (float, optional): Direct Normal Irradiation, W/m2. Defaults to None.
            dhi (float, optional): Direct Horizontal Irradiation, W/m2. Defaults to None.
            temp_air (float, optional): Air Temperature, C. Defaults to 20.
            wind_speed (float, optional): Wind Speed, m/s. Defaults to 0.
            pressure (float, optional): .Air pressure, Pa. If value not given, takes from the altitude of the location Defaults to None.
        """
        # Create an empty dataframe
        if not dhi or not dni:
            zenith = self.location.get_solarposition(times=self.datetime[0], temperature=temp_air)
            missing_radiation_pars = pvlib.irradiance.erbs(ghi, zenith["zenith"], self.datetime[0])

        if not dhi:
            dhi = missing_radiation_pars["dhi"][0]

        if not dni:
            dni = missing_radiation_pars["dni"][0]

        self.weather_df = pd.DataFrame(
            [[ghi, dni, dhi, temp_air, wind_speed]],
            columns=["ghi", "dni", "dhi", "temp_air", "wind_speed"],
            index=[pd.Timestamp(self.datetime[0])],
        )

    def calculate_power(
        self, ghi=1000, dni=None, dhi=None, temp_air=None, wind_speed=None, pressure=None
    ):
        """Calculates the output AC power based on the input environmental parameters.
        Writes the operational parameters into the class dictionary

        Args:
            ghi (float, optional): Global Horizontal Irradiation, W/m2. Defaults to 1000.
            dni (float, optional): Direct Normal Irradiation, W/m2. Defaults to None.
            dhi (float, optional): Direct Horizontal Irradiation, W/m2. . Defaults to None.
            temp_air (float, optional): Air Temperature, C. Defaults to None.
            wind_speed (float, optional): Wind Speed, m/s. Defaults to None.
            pressure (float, optional): Air pressure, Pa. If value not given, takes from the altitude of the location. Defaults to None.

        Returns:
            float: Output AC Power, W
        """
        if self.calc_mode == "simple" and ghi <= 0:
            # DC Energy Output dictionary (MPPP Tracking)
            self.dc = 0
            self.ac = 0
            self.eff = np.nan
            return 0

        if self.calc_mode == "detailed" and ghi <= 0:
            # Bypass all of the calculations if GHI is 0
            self.dc = 0
            self.eff = np.nan
            self.ac = pvlib.inverter.sandia(0, 0, self.inverter)
            return self.ac

        if pressure is None:
            pressure = pvlib.atmosphere.alt2pres(self.elevation)

        if temp_air is None:
            temp_air = 20

        if wind_speed is None:
            wind_speed = 0

        self.prepare_weather_df(
            ghi=ghi, dni=dni, dhi=dhi, temp_air=temp_air, wind_speed=wind_speed, pressure=pressure
        )

        self.model_chain.run_model(self.weather_df)

        # DC Energy Output dictionary (MPPP Tracking)
        if self.calc_mode == "simple":
            self.dc = self.model_chain.dc.iloc[0]
            self.ac = self.model_chain.ac.iloc[0]

        if self.calc_mode == "detailed":
            self.dc = self.model_chain.dc["p_mp"].iloc[0]
            self.ac = self.model_chain.ac.iloc[0]

        if self.dc > 0:
            self.eff = self.ac / self.dc
        else:
            self.eff = np.nan

        return self.ac

    def __repr__(self, *args, **kwargs):
        """Prints the configuration dictionary and the expected power output at
        GHI = 1000 W/m2 at the set time
        """

        self.power()

        string = f"""
Working parameters @ 1000 W/m2
Time : {self.datetime[0]}
DC : {round(self.dc,1)} W
AC : {round(self.ac,1)} W
Eff: {round(100*self.eff,2)} %
"""
        return string


class Simulator(object):
    """Simulator class for the PVSystem() class
    Creates multiple instances and saves the results in an accesible list

    Args:
        object (Class): Class inheritance
    """

    # costructor
    def __init__(self):
        """Class constructor"""
        # init data elments
        self.models = []  # List with all the models
        self.results = []  # List with the results

    def add_model(self, start_date="2020-06-12 12:00:00", calc_mode="simple", **kwargs):
        """Adds models to the Simulator class

        Args:
            start_date (str, optional): Start Date in "YYYY-MM-DD hh:mm:ss". Defaults to "2020-06-12 12:00:00".
            calc_mode (str, optional): Calculation mode: "detailed" or "simple". Defaults to "simple".

        Returns:
            PVSystem: A PVSystem() class model
        """
        # create grid_observer model
        model = PVSystem(start_date=start_date, calc_mode=calc_mode, **kwargs)

        # add model to model grid_observer
        self.models.append(model)

        # add list for simulation data
        self.results.append([])

        # return model
        return model

    def step(self, time, dict_input):
        """Advances the simulation time for all the models

        Args:
            time (int): Simulation step time.
            dict_input (dict): Input dictionary with the weather information::
                dict_input = {"ghi": 1000,
                              "dni": None,
                              "dhi": None,
                              "temp_air": 25,
                              "wind_speed": 4,
                              "pressure": 102500}

        """
        # Enumeration over all models in simulator
        for i, model in enumerate(self.models):
            # perform simulation step
            model.power(
                ghi=dict_input["ghi"],
                dni=dict_input["dni"],
                dhi=dict_input["dhi"],
                temp_air=dict_input["temp_air"],
                wind_speed=dict_input["wind_speed"],
                pressure=dict_input["pressure"],
            )
            model.step(time)

            # collect data of model and storage local
            for _, signal in enumerate(model.results):
                self.results[i].append(getattr(model, signal))

if __name__ == "__main__":
    # Detailed Configuration
    # TODO migrate this tests to the test folder
    configuration = generate_configurations(Scenarios.BASE)
    pvSys = PVSystem("2020-06-12 12:00:00", **configuration)
    print(
        "Oldenburg, Single Module: ",
        pvSys.power(ghi=1000, temp_air=20, wind_speed=0, pressure=101252),
    )

    print(pvSys)

    # Simple Configuration
    config_simple = generate_configurations(scenario=Scenarios.SIMPLE)
    pvSysSimple = PVSystem("2020-06-12 12:00:00", calc_mode="simple", **config_simple)
    print(
        "Oldenburg, Simple Single Module: ",
        pvSysSimple.power(ghi=1000, temp_air=20, wind_speed=0, pressure=101252),
    )

    print(config_simple)
