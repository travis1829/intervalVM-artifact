import sys
import re

def edit_mpm_config(threads, max_threads, config_file_path='/usr/local/apache2/conf/extra/httpd-mpm.conf'):
    if threads > max_threads:
        print("Warning: threads is higher than max_threads. Increasing max_threads.")
        max_threads = threads

    try:
        # Read the current content of the config file
        with open(config_file_path, 'r') as file:
            config_content = file.read()

        # Define regex patterns for each directive
        max_spare_threads_pattern = r"(<IfModule mpm_event_module>.*?MaxSpareThreads\s+)\d+"
        threads_per_child_pattern = r"(<IfModule mpm_event_module>.*?ThreadsPerChild\s+)\d+"
        max_request_workers_pattern = r"(<IfModule mpm_event_module>.*?MaxRequestWorkers\s+)\d+"
        thread_limit_pattern = r"(<IfModule mpm_event_module>.*?ThreadLimit\s+)\d+"

        # Substitute the new `threads` value in the appropriate lines
        config_content = re.sub(max_spare_threads_pattern, r"\g<1>" + str(threads), config_content, flags=re.DOTALL)
        config_content = re.sub(threads_per_child_pattern, r"\g<1>" + str(threads), config_content, flags=re.DOTALL)
        config_content = re.sub(max_request_workers_pattern, r"\g<1>" + str(threads), config_content, flags=re.DOTALL)
        config_content = re.sub(thread_limit_pattern, r"\g<1>" + str(max_threads), config_content, flags=re.DOTALL)

        # Write the modified content back to the file
        with open(config_file_path, 'w') as file:
            file.write(config_content)

        print("Configuration updated successfully.")

    except FileNotFoundError:
        print(f"Error: The file '{config_file_path}' was not found.")
    except PermissionError:
        print(f"Error: Insufficient permissions to edit '{config_file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    threads = int(sys.argv[1])
    max_threads = int(sys.argv[2])
    edit_mpm_config(threads, max_threads)