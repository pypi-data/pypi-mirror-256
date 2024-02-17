import argparse
import subprocess
import yaml
import os

def run_task(task, parameters, udfs):
    for action in task:
        action_type, action_data = action.popitem()
        if action_type == 'command':
            formatted_command = action_data.format(**parameters)
            subprocess.run(formatted_command, shell=True)
        elif action_type == 'install_package':
            install_package(str(action_data).format(**parameters))
        elif action_type == 'enable_service':
            enable_service(str(action_data).format(**parameters))
        elif action_type == 'configure_firewall':
            configure_firewall([str(rule).format(**parameters) for rule in action_data])
        elif action_type == 'prompt':
            prompt_value = input(str(action_data).format(**parameters))
            parameters[str(action['parameter'])] = prompt_value
        elif action_type == 'udf':
            udf_name = str(action_data)
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

def load_module(module_path):
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    with open(module_path, 'r') as file:
        module_data = yaml.safe_load(file)
    return module_name, module_data

def main():
    parser = argparse.ArgumentParser(description='CLCTool - Custom Linux configuration tool')
    parser.add_argument('-i', '--input', help='Specify the path to a module .spoink file for standalone execution')
    parser.add_argument('-p', '--profile', help='Specify the profile to use', default='default')
    parser.add_argument('-v', '--version', help='Specify the version', default='1.0')
    parser.add_argument('-m', '--module-args', help='Specify additional module-specific arguments as key-value pairs separated by commas')
    args = parser.parse_args()

    parameters = {
        'profile': args.profile,
        'version': args.version,
    }

    if args.input:
        module_name, module_data = load_module(args.input)
        run_task(module_data.get('tasks', []), parameters, module_data.get('udfs', {}))
    else:
        print("No module specified. Use the -i option to provide a module .spoink file.")

if __name__ == "__main__":
    main()
