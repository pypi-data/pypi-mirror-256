============
mosaik-pvlib
============

This component combines the PVLib and Mosaik co-simulation environment to calculate the active/reactive PV power output.
The original code by Fernando Penaherrera was part of the `ZDIN-ZLE <https://gitlab.com/zdin-zle/scenarios/grid-capacity-for-electric-mobility>`_ project.

The PV system simulator uses the following meteorological data as input:

* GHI[W/m2] - Global irradiance (direct normal irradiance)
* Wind[m/s] - Wind speed
* Air[C] - Air temperature
* Air[Pa] - Air pressure (hourly measurements, by default)

PV system output data:

* P[MW] - active power produced

The library provides three easily interpretable PV configurations:

* HOUSE
* BUILDING
* SIMPLE

An example scenario is located in the ´demo´ folder.

Other options
=============
Please pay attention to the input data. If you want to use only Direct Normal Irradiance input data as part of the co-simulation, 
then *mosaik-pv* is suitable, if you want to use full weather information (global irradiance, wind speed, air temperature and pressure) then *mosaik-pvlib* is suitable. 
If you are satisfied with historical performance estimates for a particular location or have no other input data, 
then *mosaik-pvgis* is the best solution which is based on PVGIS performance data.

Installation
============
* To use this project, you have to install at least version 3.2.0 of `mosaik <https://mosaik.offis.de/>`_
* It is recommended, to use the Mosaik-CSV Library to import meteo data

If you don't want to install this project through PyPI, you can use pip to install the requirements.txt file::

    pip install -r requirements.txt

How to Use
==========
Specify simulators configurations within your scenario script::

    SIM_CONFIG = {
        'MeteoSim': {
            'python': 'mosaik_csv:CSV'
        },  
        'PVSim': {
            'python': 'mosaik_components.pv.photovoltaic_simulator:PVSimulator'
        },
        ...
    }

Initialize the PV- and meteo-simulator::

    # Create weather/meteo simulator
    meteo_sim = world.start("MeteoSim", sim_start=START, datafile=METEO_DATA)
    
    # Create PV system with certain configuration
    pv_count = 5
    pv_config = {str(i) : generate_configurations(Scenarios.HOUSE) for i in range(pv_count)}
    pv_sim = world.start(
                    "PVSim",
                    start_date=START,
                    step_size=STEP_SIZE,
                    pv_data=pv_config,
                )


Instantiate model entities::

    meteo_model = meteo_sim.Braunschweig.create(1)
    pv_model = pv_sim.PVSim.create(pv_count)

Connect meteo input with PV-simulator::

    world.connect(
                        meteo_model[0],
                        pv_model[0],
                        ("GlobalRadiation", "GHI[W/m2]"),
                        ("AirPressHourly", "Air[Pa]"),
                        ("AirTemperature", "Air[C]"),
                        ("WindSpeed", "Wind[m/s]"),
                    )

CSV-Formatting
==============

For the simulator to work correctly, both .csv files have to be specifically formatted!

meteo-data
----------
The meteo_data.csv is formatted accordingly to the conventions of the `mosaik_csv <https://gitlab.com/mosaik/components/data/mosaik-csv>`_ simulator::

    Wind
    Date,wind_speed
    YYYY-MM-DD HH:mm:ss,v1
    YYYY-MM-DD HH:mm:ss,v2
    ...
    Braunschweig
    Time,GlobalRadiation,AirPressHourly,AirTemperature,WindSpeed
    YYYY-MM-DD HH:mm:ss,2.1,92.0,0.0,0.0

* Each entry in the .csv needs a Date in the YYYY-MM-DD HH:mm:ss format and a set of values.
