# -*- coding: utf-8 -*-
import sys
import socket
import psutil
import json


# cpu信息,float类型
cpu_idle = psutil.cpu_times_percent(interval=1).idle
cpu_use_per = 100 - cpu_idle

# 内存信息,float类型
mem_per = psutil.virtual_memory().percent

# 磁盘信息,float类型
root_usage = psutil.disk_usage("/").percent
home_usage = psutil.disk_usage("/home").percent

# 端口测试
def check_port(port_listen, port_type="AF_INET"):
    if port_type == "AF_INET":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif port_type == "AF_INET6":
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    else:
        sock = socket.socket()
    result = sock.connect_ex(('127.0.0.1', port_listen))
    sock.close()
    return result


def dict_input(input):
    "将dict格式的str转换成dict"
    result = {}
    content = input.split('{')[1].split('}')[0]
    for item in content.split(','):
        key, value = item.split(':')
        result[key] = value
    return result


if __name__ == "__main__":
    ser_port_str = ''.join(sys.argv[1:])
    if ser_port_str:
        ser_port = dict_input(ser_port_str)
        port_state = {}
        for ser in ser_port.values():
            ser_p = int(ser)
            if check_port(ser_p):
                port_state[ser_p] = "BAT"
            else:
                port_state[ser_p] = "OK"
    else:
        port_state = "no port pass!!"
    check_info = {}
    check_info["CPU"] = "%.2f" % cpu_use_per
    check_info["MEM"] = "%.2f" % mem_per
    check_info["DISK_ROOT"] = "%.2f" % root_usage
    check_info["DISK_HOOT"] = "%.2f" % home_usage
    check_info["PORT"] = port_state
	
    print check_info
    #print type(check_info)
    
    with open("/tmp/check_host.txt", "w") as f:
        json.dump(check_info,f)


