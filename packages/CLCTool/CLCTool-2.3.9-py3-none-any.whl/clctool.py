import argparse
import subprocess
import yaml
import os

def run_task(task, parameters, udfs):
    for action in task:
        if 'command' in action:
            formatted_command = action['command'].format(**parameters)
            subprocess.run(formatted_command, shell=True)
        elif 'install_package' in action:
            install_package(action['install_package'].format(**parameters))
        elif 'enable_service' in action:
            enable_service(action['enable_service'].format(**parameters))
        elif 'configure_firewall' in action:
            configure_firewall([rule.format(**parameters) for rule in action['configure_firewall']])
        elif 'prompt' in action:
            prompt_value = input(action['prompt'].format(**parameters))
            parameters[action['parameter']] = prompt_value
        elif 'udf' in action:
            udf_name = action['udf']
            if udf_name in udfs:
                udfs[udf_name](parameters)

def install_package(package):
    subprocess.run(["apt-get", "install", "-y", package])

def enable_service(service):
    subprocess.run(["systemctl", "enable", service])
    subprocess.run(["systemctl", "start", service])

def configure_firewall(rules):
    for rule in rules:
        subprocess.run(["ufw", "allow", rule])

def load_modules(module_paths):
    modules = {}
    for path in module_paths:
        module_name = os.path.splitext(os.path.basename(path))[0]
        with open(path, 'r') as file:
            module_data = yaml.safe_load(file)
            modules[module_name] = module_data
    return modules

def read_spoink_files(modules, order, parameters):
    for module_name in order:
        module_data = modules.get(module_name, {})
        tasks = module_data.get('tasks', [])
        udfs = module_data.get('udfs', {})

        for task in tasks:
            if 'condition' in task:
                condition = task['condition'].format(**parameters)
                if not eval(condition):
                    continue
            run_task(task, parameters, udfs)

def main():
    parser = argparse.ArgumentParser(description='CLCTool - Custom Linux configuration tool')
    parser.add_argument('-m', '--modules', help='Specify the paths to the module .spoink files separated by comma', required=True)
    parser.add_argument('-o', '--order', help='Specify the order in which modules should be executed, separated by comma', required=True)
    parser.add_argument('-p', '--profile', help='Specify the profile to use', default='default')
    parser.add_argument('-v', '--version', help='Specify the version', default='1.0')
    args = parser.parse_args()

    module_paths = args.modules.split(',')
    order = args.order.split(',')

    parameters = {
        'profile': args.profile,
        'version': args.version,
    }

    modules = load_modules(module_paths)
    read_spoink_files(modules, order, parameters)

if __name__ == "__main__":
    main()
