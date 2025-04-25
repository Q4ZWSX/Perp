# Define the base IP prefix and valid values for y
base_ip = "172.30.1"
y_values = [1, 2, 3, 5]

# Generate IPs for x from 1 to 23 and y from y_values
for x in range(1, 24):
    for y in y_values:
        ip = f"{base_ip}.{x}{y}"
        print(ip)
