# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

#import flask_restful
import json
import requests

url = "http://211.252.85.242:55010/api/v1/query?query="

############################################################
##########################  Main  ##########################
############################################################
# @blueprint.route('/index')
# @login_required
# def index():
#     return render_template('index.html', segment='index')

############################################################
########################  Metrics  #########################
############################################################
#@blueprint.route('/metrics')
@blueprint.route('/index')
def index():
    result_mem = []
    result_mem_use = []
    result_mem_total = []
    result_net_in = []
    result_net_out = []
    result_disk = []
    result_disk_use = []
    result_disk_total = []
    result_disk_read = []
    result_disk_write = []
    result_cpu = []

    # memory = memory_usage()
    # result_mem.append(memory)

    memory = [i[0] for i in memory_usage()]
    result_mem.append(memory)

    memory_use = [i[1] for i in memory_usage()]
    result_mem_use.append(memory_use)

    memory_total = [i[2] for i in memory_usage()]
    result_mem_total.append(memory_total)

    net_in = network_in_data()
    result_net_in.append(net_in)

    net_out = network_out_data()
    result_net_out.append(net_out)

    # disk = disk_usage()
    # result_disk.append(disk)
    disk = [i[0] for i in disk_usage()]
    result_disk.append(disk)

    disk_use = [i[1] for i in disk_usage()]
    result_disk_use.append(disk_use)

    disk_total = [i[2] for i in disk_usage()]
    result_disk_total.append(disk_total)

    disk_read = disk_read_speed()
    result_disk_read.append(disk_read)

    disk_write = disk_write_speed()
    result_disk_write.append(disk_write)

    cpu = cpu_usage()
    result_cpu.append(cpu)

    result_alerts = alert_gen()

    return render_template('index.html', result_mem=result_mem, result_net_in=result_net_in,
                           result_net_out=result_net_out, result_disk=result_disk, result_disk_read=result_disk_read,
                           result_disk_write=result_disk_write, result_cpu=result_cpu, result_alerts=result_alerts,
                           segment='index')


@blueprint.route('/update', methods=['GET','POST'])
def update():
    result_mem = []
    result_mem_use = []
    result_mem_total = []
    result_net_in = []
    result_net_out = []
    result_disk = []
    result_disk_use=[]
    result_disk_total=[]
    result_disk_read = []
    result_disk_write = []
    result_cpu = []

    memory = [i[0] for i in memory_usage()]
    result_mem.append(memory)

    memory_use=[i[1] for i in memory_usage()]
    result_mem_use.append(memory_use)

    memory_total=[i[2] for i in memory_usage()]
    result_mem_total.append(memory_total)

    net_in = network_in_data()
    result_net_in.append(net_in)

    net_out = network_out_data()
    result_net_out.append(net_out)

    disk = [i[0] for i in disk_usage()]
    result_disk.append(disk)

    disk_use = [i[1] for i in disk_usage()]
    result_disk_use.append(disk_use)

    disk_total = [i[2] for i in disk_usage()]
    result_disk_total.append(disk_total)

    disk_read = disk_read_speed()
    result_disk_read.append(disk_read)

    disk_write = disk_write_speed()
    result_disk_write.append(disk_write)

    cpu = cpu_usage()
    result_cpu.append(cpu)

    result_alerts = alert_gen()

    return jsonify({
        'result_mem0': result_mem[0][0],
        'result_mem1': result_mem[0][1],
        'result_mem2': result_mem[0][2],

        'result_mem_use0': result_mem_use[0][0],
        'result_mem_use1': result_mem_use[0][1],
        'result_mem_use2': result_mem_use[0][2],

        'result_mem_total0': result_mem_total[0][0],
        'result_mem_total1': result_mem_total[0][1],
        'result_mem_total2': result_mem_total[0][2],

        'result_net_in0' : result_net_in[0][0],
        'result_net_in1' : result_net_in[0][1],
        'result_net_in2' : result_net_in[0][2],
        'result_net_out0' : result_net_out[0][0],
        'result_net_out1' : result_net_out[0][1],
        'result_net_out2' : result_net_out[0][2],
        'result_disk0' : result_disk[0][0],
        'result_disk1' : result_disk[0][1],
        'result_disk2' : result_disk[0][2],

        'result_disk_use0': result_disk_use[0][0],
        'result_disk_use1': result_disk_use[0][1],
        'result_disk_use2': result_disk_use[0][2],

        'result_disk_total0': result_disk_total[0][0],
        'result_disk_total1': result_disk_total[0][1],
        'result_disk_total2': result_disk_total[0][2],

        'result_disk_read0' : result_disk_read[0][0],
        'result_disk_read1' : result_disk_read[0][1],
        'result_disk_read2' : result_disk_read[0][2],
        'result_disk_write0' : result_disk_write[0][0],
        'result_disk_write1' : result_disk_write[0][1],
        'result_disk_write2' : result_disk_write[0][2],
        'result_cpu0' : result_cpu[0][0],
        'result_cpu1' : result_cpu[0][1],
        'result_cpu2' : result_cpu[0][2],
        'result_alerts' : result_alerts,
    })
############################################################
########################  function  ########################
############################################################
def memory_usage():
    memory = []
    try:
        for i in range(1,4):
            url_MemAvail = url+"node_memory_MemAvailable_bytes{job='node-exporter_"+str(i)+"'}"
            url_MemTotal = url+"node_memory_MemTotal_bytes{job='node-exporter_"+str(i)+"'}"

            res_MemAvail = requests.get(url_MemAvail)
            data_MemAvail = res_MemAvail.json()
            if len(data_MemAvail['data']['result'])==0:
                mem_usage = 0
                mem_use_val = 0
                mem_tot_val = 0

            else:
                val_MemAvail = int(data_MemAvail['data']['result'][0]['value'][1])

                res_MemTotal = requests.get(url_MemTotal)
                data_MemTotal = res_MemTotal.json()
                val_MemTotal = int(data_MemTotal['data']['result'][0]['value'][1])

                mem_usage = 100-(val_MemAvail/val_MemTotal*100)
                mem_usage = round(mem_usage,2)
                mem_use_val = round((val_MemTotal-val_MemAvail)/(1000*1000*1000),2)
                mem_tot_val = round((val_MemTotal)/(1000*1000*1000),2)

            memory.append([mem_usage,mem_use_val,mem_tot_val])

        return memory
    except:
        return None

def network_in_data():
    net_in = []
    try:
        for i in range(1,4):
            url_Network_in = url +"rate(node_network_receive_bytes_total{job='node-exporter_"+str(i)+"'}[2m])"

            res_Network_in = requests.get(url_Network_in)
            data_Network_in = res_Network_in.json()
            if len(data_Network_in['data']['result'])==0:
                network_in=0
            else:
                val_Network_in = int(float(data_Network_in['data']['result'][0]['value'][1]))

                network_in = val_Network_in/1024/1024
                network_in = format(network_in,'.8f')
            net_in.append(network_in)

        return net_in
    except:
        return None

def network_out_data():
    net_out = []
    try:
        for i in range(1,4):
            url_Network_out = url +"rate(node_network_transmit_bytes_total{job='node-exporter_"+str(i)+"'}[2m])"

            res_Network_out = requests.get(url_Network_out)
            data_Network_out = res_Network_out.json()
            if len(data_Network_out['data']['result'])==0:
                network_out=0
            else:
                val_Network_out = int(float(data_Network_out['data']['result'][0]['value'][1]))

                network_out = val_Network_out/1024/1024
                network_out = round(network_out,8)
            net_out.append(network_out)

        return net_out
    except:
        return None

def disk_usage():
    disk = []
    try:
        for i in range(1,4):
            url_FileAvail = url+"node_filesystem_avail_bytes{job='node-exporter_"+str(i)+"'}"
            url_FileSize = url+"node_filesystem_size_bytes{job='node-exporter_"+str(i)+"'}"

            res_FileAvail = requests.get(url_FileAvail)
            data_FileAvail = res_FileAvail.json()
            if len(data_FileAvail['data']['result'])==0:
                disk_usage=0
                disk_use_val=0
                disk_tot_val=0
            else:
                val_FileAvail = int(data_FileAvail['data']['result'][0]['value'][1])

                res_FileSize = requests.get(url_FileSize)
                data_FileSize = res_FileSize.json()
                val_FileSize = int(data_FileSize['data']['result'][0]['value'][1])

                disk_usage = 100-(val_FileAvail*100)/val_FileSize
                disk_usage = round(disk_usage,2)
                disk_use_val = round((val_FileSize-val_FileAvail)/(1000*1000*1000),2)
                disk_tot_val = round((val_FileSize)/(1000*1000*1000),2)

            disk.append([disk_usage,disk_use_val,disk_tot_val])

        return disk
    except:
        return None

def disk_read_speed():
    disk_read = []
    try:
        for i in range(1,4):
            url_disk_read = url+"rate(node_disk_read_bytes_total{job='node-exporter_"+str(i)+"'}[2m])"

            res_disk_read = requests.get(url_disk_read)
            data_disk_read = res_disk_read.json()
            if len(data_disk_read['data']['result'])==0:
                read_speed=0
            else:
                val_disk_read = int(float(data_disk_read['data']['result'][1]['value'][1]))

                read_speed = val_disk_read/1024/1024
                read_speed = round(read_speed,5)
            disk_read.append(read_speed)

        return disk_read
    except:
        return None

def disk_write_speed():
    disk_write = []
    try:
        for i in range(1,4):
            url_disk_write = url+"rate(node_disk_written_bytes_total{job='node-exporter_"+str(i)+"'}[2m])"

            res_disk_write = requests.get(url_disk_write)
            data_disk_write = res_disk_write.json()
            if len(data_disk_write['data']['result'])==0:
                write_speed=0
            else:
                val_disk_write = int(float(data_disk_write['data']['result'][1]['value'][1]))

                write_speed = val_disk_write/1024/1024
                write_speed = round(write_speed,5)
            disk_write.append(write_speed)

        return disk_write
    except:
        return None

def cpu_usage():
    cpu = []
    try:
        for i in range(1,4):
            url_cpu_usage = url+"rate(node_cpu_seconds_total{job='node-exporter_"+str(i)+"', mode='idle'}[2m])"

            res_cpu_usage= requests.get(url_cpu_usage)
            data_cpu_usage = res_cpu_usage.json()
            if len(data_cpu_usage['data']['result'])==0:
                cpu_usage=0
            else:
                val_cpu_usage = float(data_cpu_usage['data']['result'][0]['value'][1])

                cpu_usage = 100-((val_cpu_usage)*100)
                cpu_usage = round(cpu_usage,2)
            cpu.append(cpu_usage)

        return cpu
    except:
        return None

def alert_gen():
    try:
        url_alert = url + "ALERTS"
        res_alert=requests.get(url_alert)
        data_res_alert=res_alert.json()
        temp_alert=[]
        alert = []

        for metric in data_res_alert['data']['result']:
            temp_alert.clear()
            if metric['value'][1]=='1':
                temp_alert.append(metric['metric']['alertname'])
                temp_alert.append(metric['metric']['alertstate'])
                temp_alert.append(metric['metric']['instance'])
                temp_alert.append(metric['metric']['severity'])

                tmp=temp_alert.copy()
                alert.append(tmp)

        return alert
    except:
        return None

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request
def get_segment( request ):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
