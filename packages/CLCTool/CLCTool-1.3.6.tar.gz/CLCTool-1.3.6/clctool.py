# clctool.py

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
            install_package(action['install_package'], parameters)
        elif 'enable_service' in action:
            enable_service(action['enable_service'], parameters)
        elif 'configure_firewall' in action:
            configure_firewall(action['configure_firewall'], parameters)
        elif 'prompt' in action:
            prompt_value = input(action['prompt'].format(**parameters))
            parameters[action['parameter']] = prompt_value
        elif 'udf' in action:
            execute_udf(action['udf'], parameters, udfs)
        # Additional features as tasks
        elif 'configure_network' in action:
            interface = action['configure_network']['interface'].format(**parameters)
            ip_address = action['configure_network']['ip_address'].format(**parameters)
            netmask = action['configure_network']['netmask'].format(**parameters)
            subprocess.run(["ifconfig", interface, ip_address, "netmask", netmask])
        elif 'restart_service' in action:
            service_name = action['restart_service'].format(**parameters)
            subprocess.run(["systemctl", "restart", service_name])
        elif 'create_directory' in action:
            directory_path = action['create_directory'].format(**parameters)
            subprocess.run(["mkdir", directory_path])
        elif 'delete_file' in action:
            file_path = action['delete_file'].format(**parameters)
            subprocess.run(["rm", "-f", file_path])
        elif 'run_script' in action:
            script_path = action['run_script'].format(**parameters)
            subprocess.run(["bash", script_path])
        elif 'set_hostname' in action:
            hostname_value = action['set_hostname'].format(**parameters)
            subprocess.run(["hostnamectl", "set-hostname", hostname_value])
        elif 'add_user_to_group' in action:
            username = action['add_user_to_group']['username'].format(**parameters)
            groupname = action['add_user_to_group']['groupname'].format(**parameters)
            subprocess.run(["usermod", "-aG", groupname, username])
        elif 'install_deb_package' in action:
            package_path = action['install_deb_package'].format(**parameters)
            subprocess.run(["dpkg", "-i", package_path])
        elif 'start_service' in action:
            service_name = action['start_service'].format(**parameters)
            subprocess.run(["systemctl", "start", service_name])
        elif 'stop_service' in action:
            service_name = action['stop_service'].format(**parameters)
            subprocess.run(["systemctl", "stop", service_name])
        elif 'reload_service' in action:
            service_name = action['reload_service'].format(**parameters)
            subprocess.run(["systemctl", "reload", service_name])
        elif 'enable_autostart' in action:
            service_name = action['enable_autostart'].format(**parameters)
            subprocess.run(["systemctl", "enable", service_name])
        elif 'disable_autostart' in action:
            service_name = action['disable_autostart'].format(**parameters)
            subprocess.run(["systemctl", "disable", service_name])
        elif 'add_ssh_key' in action:
            user = action['add_ssh_key']['user'].format(**parameters)
            ssh_key_path = action['add_ssh_key']['ssh_key_path'].format(**parameters)
            subprocess.run(["mkdir", f"/home/{user}/.ssh"])
            subprocess.run(["cp", ssh_key_path, f"/home/{user}/.ssh/authorized_keys"])
            subprocess.run(["chown", f"{user}:{user}", f"/home/{user}/.ssh/authorized_keys"])
            subprocess.run(["chmod", "600", f"/home/{user}/.ssh/authorized_keys"])
        elif 'add_sudo_user' in action:
            username = action['add_sudo_user'].format(**parameters)
            subprocess.run(["adduser", username, "sudo"])
        elif 'configure_cron_job' in action:
            cron_job_command = action['configure_cron_job'].format(**parameters)
            subprocess.run(["echo", cron_job_command, ">>", "/etc/crontab"])
        elif 'install_from_source' in action:
            source_url = action['install_from_source']['source_url'].format(**parameters)
            destination_path = action['install_from_source']['destination_path'].format(**parameters)
            subprocess.run(["git", "clone", source_url, destination_path])
            subprocess.run(["make", "-C", destination_path])
            subprocess.run(["make", "-C", destination_path, "install"])
        elif 'set_timezone' in action:
            timezone_value = action['set_timezone'].format(**parameters)
            subprocess.run(["timedatectl", "set-timezone", timezone_value])
        elif 'set_locale' in action:
            locale_value = action['set_locale'].format(**parameters)
            subprocess.run(["update-locale", "LANG=" + locale_value])

def execute_udf(udf_name, parameters, udfs):
    if udf_name in udfs:
        udfs[udf_name](parameters)

# Load modules and user-defined functions (UDFs)

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

# Main function

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
