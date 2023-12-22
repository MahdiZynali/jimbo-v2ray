from utils.Scanner import scanner

range_ip = "188.114.98.0/24"
final_range = range_ip.replace(range_ip[-4:], "")

scan = scanner(final_range, port=443, epoch=255, num_processes=8)