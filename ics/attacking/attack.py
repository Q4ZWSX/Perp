from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('172.20.0.14', port=502)

# Turn on Water Pump 1
client.write_coil(0, True)  # Modbus address starts at 0
client.write_coil(1, True)
client.write_coil(2, True)
client.write_coil(3, True)
client.write_coil(4, True)

client.close()
