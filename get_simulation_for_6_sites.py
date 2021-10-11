import json
import application.helpers.getter as getter
import application.helpers.constant as C
import system.config.config as config

f = open(C.LOG_PROD_PATH + 'simulation.json')
data = json.load(f)

# simulation for 6 sites 
PARAM = config.get_scenario()

sim_name = []
for method in PARAM['method']:
    for data_type in PARAM['dataset_type']:
        sim_name.append(getter.simulation_name(method, data_type, PARAM['const_cardinality'], PARAM['const_dimension'], PARAM['const_grid_size']))

sim_id = []
for name in sim_name:
    if name in data:
        dir_name = '_'.join(name.split('_')[0:-4] + [data[name]])
        sim_id.append(dir_name)
        print(name, "=>", dir_name)
    else:
        print(name, "=> No simulation")

print("")
print("Result:")
for sid in sim_id:
    print(sid)