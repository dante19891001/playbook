#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import json
from pyh2 import *


class HostStatistics(object):
    """
       # 用来统计ansible批量fetch回来的巡检文件
       # 不同巡检项目修改host_list下面的service_list
    """

    def __init__(self, base, remote_file, html_title):
        """
       # base是本地储存fetch文件的根目录
       # remote_file是服务器端的文件绝对路径
       # html_title是时间标题
        """
        self.base = base
        self.remote_file = remote_file
        self.html_title = html_title

    def host_list(self):
        """
        返回ansible中的主机别名列表
        例如 ['ule_pcb_47', 'ule_web_61', 'ule_pcb_52', 'ule_pcb_132']
        """
        for x in os.listdir(self.base):
            yield x

    def txt_info(self):
        """
        传需要检测的服务器列表，
        返回一个列表类型数据
        """
        file_list = []
        listing = self.host_list()
        for info_name in listing:
            open_file_pwd = os.path.join(self.base, info_name, 'tmp', self.remote_file)
            with open(open_file_pwd) as file_pwd:
                file_dict = json.load(file_pwd)
                file_dict["NAME"] = info_name
            file_list.append(file_dict)
        return file_list

    def html_write(self):
        file_list = self.txt_info()
        # 阀值
        cpu_valve = 10
        mem_valve = 70
        disk_valve = 50

        page = PyH('check_info')
        page.addCSS('https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.2/css/bootstrap.css')
        page.addCSS('https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.2/css/bootstrap-responsive.css')
        page.addCSS('https://cdnjs.cloudflare.com/ajax/libs/datatables/1.9.1/css/jquery.dataTables.css')
        page.addJS('https://code.jquery.com/jquery-3.2.1.min.js')
        page.addJS('https://cdn.datatables.net/1.10.15/js/jquery.dataTables.min.js')
        page.addJS('https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.2/js/bootstrap.js')
        page.addJS('http://sandbox.runjs.cn/uploads/rs/238/n8vhm36h/dataTables.bootstrap.js')
        div1 = page << div(cl='container-fluid')
        div1 << h2(self.html_title) + p('可用功能：分页/ 排序/ 过滤')
        div2 = div1 << div(cl='row-fluid')
        div3 = div1 << div(cl='row-fluid')

        mytab = div3 << table(cl="table table-striped table-bordered table-hover datatable")
        tthr = mytab << tr()
        tr1 = tthr << th('项目') + th('CPU') + th('内存') + th('root磁盘') + th('home磁盘') + th(
            '端口状态') + th(
            '备注')
        for i in range(len(file_list)):
            port_list = []
            port_info = file_list[i]['PORT']
            cpu_num = file_list[i]['CPU']
            mem_num = file_list[i]['MEM']
            disk_root_num = file_list[i]['DISK_ROOT']
            disk_home_num = file_list[i]['DISK_HOOT']
            tr2 = mytab << tr()

            tr2 << td(file_list[i]['NAME'])
            tr2 << td(cpu_num)
            if float(cpu_num) > cpu_valve:
                tr2[1].attributes['style'] = 'color:red'
            tr2 << td(mem_num)
            if float(mem_num) > mem_valve:
                tr2[2].attributes['style'] = 'color:red'
            tr2 << td(disk_root_num)
            if float(disk_root_num) > disk_valve:
                tr2[3].attributes['style'] = 'color:red'
            tr2 << td(disk_home_num)
            if float(disk_home_num) > disk_valve:
                tr2[4].attributes['style'] = 'color:red'

            for i in port_info.keys():
                port = "the {0:>5} is {1}".format(i, port_info[i])
                port_list.append(port)
            port_txt = '<br />'.join(port_list)
            tr2 << td(port_txt)
            if 'BAT' in port_txt:
                tr2[5].attributes['style'] = 'color:red'
            tr2 << td()
        footjs = page << script('$(".datatable").DataTable({"dom": "lftip","language": {"lengthMenu": "每页显示 _MENU_ 条记录","zeroRecords": "找到零条记录","info": "总共_PAGES_页记录，目前在第_PAGE_页","infoEmpty": "对不起，找不到数据","infoFiltered": "(从_MAX_条数据中过滤)","paginate": {"previous": "上一页","next": "下一页"},"search": "搜索: "},"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "全部"]],})')
        footstyle = page << style('.table>tr:first-child>th{vertical-align: middle;} .table>tbody>tr>td{vertical-align: middle;}')
        theadstyle = page << style('.table.dataTable >thead { background-color: #23c9ff;}')
        oddstyle = page << style(
            '.table.dataTable tr.odd>td { background-color: #d9edf7;} .table.dataTable tr.odd:hover>td { background-color: #c4e3f3;}')
        evenstyle = page << style('.table.dataTable tr.even>td { background-color: #dff0d8;} .table.dataTable tr.even:hover>td { background-color: #d0e9c6;}')
        page.printOut("test.html")


if __name__ == "__main__":
    end_time = time.strftime("%Y%m%d", time.localtime(time.time() - 3 * 24 * 60 * 60))
    start_time = time.strftime('%Y%m%d', time.localtime(time.time() - 7 * 24 * 60 * 60))
    check_base = "tmp/"
    remote_file = "check_host.txt"
    html_title = "服务器 %s-%s 巡检报告" % (start_time, end_time)
    hs = HostStatistics(check_base, remote_file, html_title)
    hs.html_write()