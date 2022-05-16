import yaml

with open("./config.yaml", "r") as stream:
    data_loaded = yaml.safe_load(stream)
    print(data_loaded)
