import train
import yaml

config = yaml.safe_load(open("./config.yaml"))

if __name__ == '__main__':
    train.training_pipeline(config)