allowed_ips = ["66.249.73.185", "86.1.76.62"]

def filter_ips(input_file_path, output_file_path, allowed_ips):
    try:
        dictionary = {}
        with open(input_file_path) as file:
            for line in file:
                print(line)
                split_result = line.split()
                ip_Address = split_result[0]
                if ip_Address in allowed_ips:
                    #dictonary {key = IP: counter}
                    if ip_Address in dictionary:
                        dictionary[ip_Address] += 1
                    else:
                        dictionary[ip_Address] = 1
        print(dictionary)
        #Import the result in result_logs.txt
        with open(output_file_path, "w") as file:
            for k,v in dictionary.items():
                file.write(k + " " + str(v) + "\n")
    except FileNotFoundError:
        print("Couldn't found the source file")




filter_ips("apache_logs.txt", "result_logs.txt", allowed_ips)