import hashlib

allowed_ips = ["66.249.73.185", "86.1.76.62"]

def analyze_log_file(log_file_path):
    response_codes = {}
    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                parts = line.split('"')
                if len(parts) > 2:
                    status_size = parts[2].strip().split()
                    if len(status_size) >= 2:
                        try:
                            status_code = int(status_size[0])
                            response_codes[status_code] = response_codes.get(status_code, 0) + 1
                        except ValueError:
                            continue
        print("Аналізатор лог-файлів:\n", response_codes)
        return response_codes
    except FileNotFoundError:
        print("Couldn't find the source file")
        return {}

def generate_file_hashes(file_paths):
    file_hashes = {}
    for path in file_paths:
        try:
            with open(path, 'rb') as file:
                content = file.read()
                file_hash = hashlib.sha256(content).hexdigest()
                file_hashes[path] = file_hash
        except FileNotFoundError:
            print("Couldn't found the source file")
    print("Генератор хешів файлів:\n", file_hashes)
    return file_hashes

def filter_ips(input_file_path, output_file_path, allowed_ips):
    try:
        dictionary = {}
        with open(input_file_path) as file:
            for line in file:
                split_result = line.split()
                ip_Address = split_result[0]
                if ip_Address in allowed_ips:
                    #dictonary {key = IP: counter}
                    if ip_Address in dictionary:
                        dictionary[ip_Address] += 1
                    else:
                        dictionary[ip_Address] = 1
        print("Фільтрація IP-адрес з файлу: \n", dictionary)
        #Import the result in result_logs.txt
        with open(output_file_path, "w") as file:
            for k,v in dictionary.items():
                file.write(k + " " + str(v) + "\n")
    except FileNotFoundError:
        print("Couldn't found the source file")


analyze_log_file("apache_logs.txt")
generate_file_hashes(["apache_logs.txt"])
filter_ips("apache_logs.txt", "result_logs.txt", allowed_ips)