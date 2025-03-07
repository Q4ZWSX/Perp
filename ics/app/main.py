from flask import Flask, render_template
from threading import Thread
from time import sleep
from pymodbus.server.asynchronous import StartTcpServer, StopServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Simulation variables
water_pump_status = [0, 0, 0]  # Status of water pumps 1, 2, 3
cooling_rods_engaged = 0       # Status of cooling rods
temperature = 25               # Initial temperature percentage (0-100%)
electricity_produced = 1       # Electricity production status

def update_simulation():
    global temperature, electricity_produced
    while True:
        # Calculate cooling effect
        cooling_effect = sum(water_pump_status) * .5 + cooling_rods_engaged * 1.5  # Arbitrary cooling values

        # Update temperature
        if cooling_effect > 0:
            temperature -= cooling_effect * 0.1
        else:
            temperature += 1  # Temperature rises when no cooling

        # Ensure temperature stays within bounds
        temperature = max(0, min(100, temperature))

        # Update electricity production based on temperature
        if temperature > 50:
            electricity_produced = 0
        else:
            electricity_produced = 1

        sleep(1)  # Update every second

def run_modbus_server():
    store = ModbusSlaveContext(
        di = ModbusSequentialDataBlock(0, [0]*10),
        co = ModbusSequentialDataBlock(0, [0]*10),
        hr = ModbusSequentialDataBlock(0, [0]*10),
        ir = ModbusSequentialDataBlock(0, [0]*10))
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'NuclearPowerPlantSim'
    identity.ProductCode = 'NPP_SIM'
    identity.VendorUrl = 'http://example.com'
    identity.ProductName = 'Nuclear Power Plant ICS Simulator'
    identity.ModelName = 'NPPModel'
    identity.MajorMinorRevision = '1.0'

    def modbus_update():
        global water_pump_status, cooling_rods_engaged
        while True:
            # Read coils for pump statuses and cooling rods
            coils = context[0].getValues(1, 1, count=4)  # Function code, address, count
            water_pump_status = coils[0:3]
            cooling_rods_engaged = coils[3]
            sleep(1)

    # Start thread to update simulation variables based on Modbus coils
    modbus_thread = Thread(target=modbus_update)
    modbus_thread.start()

    # Start Modbus TCP server
    StartTcpServer(context, identity=identity, address=("0.0.0.0", 502))

@app.route('/')
def index():
    return render_template('index.html',
                           pump_status=water_pump_status,
                           cooling_rods_engaged=cooling_rods_engaged,
                           temperature=int(temperature),
                           electricity_produced=electricity_produced)

if __name__ == '__main__':
    # Start simulation update thread
    simulation_thread = Thread(target=update_simulation)
    simulation_thread.start()

    # Start Modbus server thread
    modbus_server_thread = Thread(target=run_modbus_server)
    modbus_server_thread.start()

    # Start Flask web server
    app.run(host='0.0.0.0', port=80)
