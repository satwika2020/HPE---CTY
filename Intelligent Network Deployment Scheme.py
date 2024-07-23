import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

access_device = [
    {'name': 'ar6100', 'type': 'access', 'switching': 0.022, 'throughput': 98.6, 'arp': 1024, 'bandwidth': 0.022,
     'unicast_routes': 512, 'multicast_routes': 0, 'MAC_enteries': 8192, 'vrf': 0,
     'layer2': ['IGMP', 'STP','VxLAN'], 'layer3': ['DHCP', 'ARP']},
    {'name': 'ar6100', 'type': 'access', 'switching': 0.022, 'throughput': 98.6, 'arp': 1024, 'bandwidth': 0.022,
     'unicast_routes': 512, 'multicast_routes': 0, 'MAC_enteries': 8192, 'vrf': 0,
     'layer2': ['IGMP', 'STP','VxLAN'], 'layer3': ['DHCP', 'ARP','PIM']},
    {'name': 'ar6300', 'type': 'access', 'switching': 0.22, 'throughput': 1310, 'arp': 49152, 'bandwidth': 0.22,
     'unicast_routes': 61000, 'multicast_routes': 8192, 'MAC_enteries': 32768, 'vrf': 256,
     'layer2': ['IGMP', 'STP','VxLAN'], 'layer3': ['DHCP', 'ARP']},
    {'name': 'ar6300', 'type': 'access', 'switching': 0.22, 'throughput': 1310, 'arp': 49152, 'bandwidth': 0.22,
     'unicast_routes': 61000, 'multicast_routes': 8192, 'MAC_enteries': 32768, 'vrf': 256,
     'layer2': ['IGMP', 'STP','VxLAN'], 'layer3': ['DHCP', 'ARP','PIM']}
]
agg_device = [
    {'name': 'ar8325', 'type': 'aggregate', 'switching': 6.4, 'throughput': 2000, 'arp': 120000, 'bandwidth': 6.4,
     'unicast_routes': 32732, 'multicast_routes': 7000, 'MAC_enteries': 98304, 'vrf': 0,
     'layer2': ['BPDU', 'IGMP','VxLAN'], 'layer3': ['DHCP', 'ARP']},
    {'name': 'ar8360', 'type': 'aggregate', 'switching': 4.8, 'throughput': 1145, 'arp': 145780, 'bandwidth': 4.8,
     'unicast_routes': 630784, 'multicast_routes': 7000, 'MAC_enteries': 212992, 'vrf': 0,
     'layer2': ['BPDU', 'IGMP','VxLAN'], 'layer3': ['DHCP', 'ARP','UDP','OSPF','BGP']}
]
core_device = [
    {'name': 'ar6400', 'type': 'core', 'switching': 28, 'throughput': 11400, 'arp': 48152, 'bandwidth': 28,
     'unicast_routes': 61000, 'multicast_routes': 2, 'MAC_enteries': 32768, 'vrf': 256,
     'layer2': ['BPDU', 'IGMP','VxLAN'], 'layer3': ['DHCP', 'ARP','UDP','OSPF','BGP']}
]

def generate_campus_topology(switching, throughput, arp, bandwidth, unicast_routes, multicast_routes, MAC_enteries, vrf, layer2, layer3, nodes):
    compatible_devices = []

    remaining_switches = switching
    remaining_throughput = throughput
    remaining_arp = arp
    remaining_bandwidth = bandwidth
    remaining_unicast = unicast_routes
    remaining_multicast = multicast_routes
    remaining_mac = MAC_enteries
    remaining_vrf = vrf

    i = 0
    j = 0
    k = 0
    c1=0
    c2=0

    while i < (nodes // 48):
        for device in access_device:
            if (device["switching"] <= remaining_switches or
                device["throughput"] <= remaining_throughput or
                device["arp"] <= remaining_arp or
                device["bandwidth"] <= remaining_bandwidth or
                device["unicast_routes"] <= remaining_unicast or
                device["multicast_routes"] <= remaining_multicast or
                device["MAC_enteries"] <= remaining_mac or
                device["vrf"] <= remaining_vrf):
                
                i += 1
                compatible_devices.append(device)
                remaining_switches -= device["switching"]
                remaining_throughput -= device["throughput"]
                remaining_arp -= device["arp"]
                remaining_bandwidth -= device["bandwidth"]
                remaining_unicast -= device["unicast_routes"]
                remaining_multicast -= device["multicast_routes"]
                remaining_mac -= device["MAC_enteries"]
                remaining_vrf -= device["vrf"]

    while j < (i // 2):
        for device in agg_device:
            compatible_devices.append(device)
            
            j += 1
            c1+=1

    while k < (j // 2):
        for device in core_device:
            compatible_devices.append(device)
            
            k += 1

    G = nx.Graph()

    nodes_names = [f"{d['name']}-{i}" for i, d in enumerate(compatible_devices)]
    G.add_nodes_from(nodes_names)

    access_nodes=[]
    aggregate_nodes=[]
    core_nodes=[]
    for node in nodes_names:
        if('6100' in node or '6300' in node):
            access_nodes.append(node)
    for node in nodes_names:
        if('8325' in node or '8360' in node):
            aggregate_nodes.append(node)
    for node in nodes_names:
        if('6400' in node):
            core_nodes.append(node)

    pos = {}
    for i, node in enumerate(access_nodes):
        pos[node] = (i, 0)
    for i, node in enumerate(aggregate_nodes):
        pos[node] = (i, 1)
    for i, node in enumerate(core_nodes):
        pos[node] = (i, 2)

    for core in core_nodes:
        for aggregate in aggregate_nodes:
            G.add_edge(core, aggregate, color="green")

    x,y=0,0
    while(c2<(c1//2)):
        count=0
        for j in range(0,2):
            count+=1
            if count==1:
                for i in range(0,count+1):
                    G.add_edge(aggregate_nodes[x], access_nodes[y], color="yellow")
                    y+=1
                x+=1
            elif count==2:
                for i in range(2,count+2):
                    G.add_edge(aggregate_nodes[x], access_nodes[y], color="yellow")
                    y+=1
                x+=1
            
            #elif count==4:
                #for i in range(4,count+2):
                    #G.add_edge(aggregate, access_nodes[i+2], color="yellow")
        c2+=1

    return G,compatible_devices
                


def visualize_topology(G, compatible_devices):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Re-initialize pos and classify nodes
    pos = {}
    nodes_names = [f"{d['name']}-{i}" for i, d in enumerate(compatible_devices)]
    G.add_nodes_from(nodes_names)
    access_nodes = []
    aggregate_nodes = []
    core_nodes = []

    for node in nodes_names:
        if '6100' in node or '6300' in node:
            access_nodes.append(node)
    for node in nodes_names:
        if '8325' in node or '8360' in node:
            aggregate_nodes.append(node)
    for node in nodes_names:
        if '6400' in node:
            core_nodes.append(node)

    # Set positions for nodes
    for i, node in enumerate(access_nodes):
        pos[node] = (i, 0)
    for i, node in enumerate(aggregate_nodes):
        pos[node] = (i, 1)
    for i, node in enumerate(core_nodes):
        pos[node] = (i, 2)

    # Draw nodes with appropriate colors and labels
    nx.draw_networkx_nodes(G, pos, nodelist=access_nodes, node_color='r', node_size=500, alpha=0.8, label='Access')
    nx.draw_networkx_nodes(G, pos, nodelist=aggregate_nodes, node_color='b', node_size=500, alpha=0.8, label='Aggregate')
    nx.draw_networkx_nodes(G, pos, nodelist=core_nodes, node_color='g', node_size=500, alpha=0.8, label='Core')

    # Draw edges with colors
    edges = G.edges()
    colors = [G[u][v]['color'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color=colors)

    # Set labels for nodes
    labels = {node: node.split('-')[0] for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color='black')

    plt.title("Campus Network Topology")
    plt.legend()
    plt.axis('off')
    plt.show()

import matplotlib.pyplot as plt
import numpy as np


def show_topology():
    switching = float(switching_entry.get())
    throughput = float(throughput_entry.get())
    arp = float(arp_entry.get())
    bandwidth = float(bandwidth_entry.get())
    unicast_routes = float(unicast_routes_entry.get())
    multicast_routes = float(multicast_routes_entry.get())
    MAC_enteries = float(MAC_enteries_entry.get())
    vrf = float(vrf_entry.get())
    nodes = int(nodes_entry.get())

    layer2_values = [
        layer2_igmp_var.get(),
        layer2_stp_var.get(),
        layer2_vxlan_var.get(),
    ]
    layer2_labels = ["IGMP", "BPDU", "VxLAN"]
    layer2 = [label for label, value in zip(layer2_labels, layer2_values) if value]

    layer3_values = [
        layer3_dhcp_var.get(),
        layer3_arp_var.get(),
        #layer3_udp_var.get(),
        layer3_ospf_var.get(),
        layer3_bgp_var.get(),
    ]
    layer3_labels = ["DHCP", "ARP", "UDP", "OSPF", "BGP"]
    layer3 = [label for label, value in zip(layer3_labels, layer3_values) if value]

    G, compatible_devices = generate_campus_topology(switching, throughput, arp, bandwidth, unicast_routes,
                                                      multicast_routes, MAC_enteries, vrf, layer2, layer3, nodes)
    visualize_topology(G, compatible_devices)
    
def summarize_devices(compatible_devices):
    summary = "Devices used in the topology:\n\n"
    processed_device_names = set()  # Track processed device names to avoid repetition
    total_switching = 0
    total_throughput = 0
    total_arp = 0
    total_bandwidth = 0
    total_unicast=0
    total_multicast=0
    total_MAC_enteries=0
    total_vrf=0
    access_nodes=[]
    aggregate_nodes=[]
    core_nodes=[]
    for device in compatible_devices:
        if device['type']=='access':
            access_nodes.append(device)
        elif device['type']=='aggregate':
            aggregate_nodes.append(device)
        elif device['type']=='core':
            core_nodes.append(device)
    
    for device in compatible_devices:
        device_name = device['name']
        if device_name not in processed_device_names:
            summary += f"Name: {device_name}\n"
            summary += f"Type: {device['type']}\n"
            summary += f"Switching: {device['switching']}\n"
            summary += f"Throughput: {device['throughput']}\n"
            summary += f"ARP: {device['arp']}\n"
            summary += f"Bandwidth: {device['bandwidth']}\n"
            summary += f"unicast_routes: {device['unicast_routes']}\n"
            summary += f"multicast_routes: {device['multicast_routes']}\n"
            summary += f"MAC_enteries: {device['MAC_enteries']}\n"
            summary += f"vrf: {device['vrf']}\n"
            summary += f"Layer 2 Protocols: {', '.join(device['layer2'])}\n"
            summary += f"Layer 3 Protocols: {', '.join(device['layer3'])}\n\n"
            processed_device_names.add(device_name)
            
            # Accumulate property totals
    for device in compatible_devices:
        total_switching += device['switching']
        total_throughput += device['throughput']
        total_arp += device['arp']
        total_bandwidth += device['bandwidth']
        total_unicast += device['unicast_routes']
        total_multicast += device['multicast_routes']
        total_MAC_enteries+= device['MAC_enteries']
        total_vrf += device['vrf']
            
    
    total_devices = len(compatible_devices)
    total_access_devices=len(access_nodes)
    total_aggregate_devices=len(aggregate_nodes)
    total_core_devices=len(core_nodes)
    summary += f"Total Devices: {total_devices}\n"
    summary += f"Total_access_Devices: {total_access_devices}\n"
    summary += f"Total_aggregate_Devices: {total_aggregate_devices}\n"
    summary += f"Total_core_Devices: {total_core_devices}\n"
    summary += f"Total Switching Capacity: {total_switching}\n"
    summary += f"Total Throughput Capacity: {total_throughput}\n"
    summary += f"Total ARP Entries: {total_arp}\n"
    summary += f"Total Bandwidth: {total_bandwidth}\n"
    summary += f"Total unicast_routes: {total_unicast}\n"
    summary += f"Total multicast_routes: {total_multicast}\n"
    summary += f"Total MAC_entries: {total_MAC_enteries}\n"
    summary += f"Total vrf: {total_vrf}\n"
    
    
    return summary
def show_summary_window(summary):
    summary_window = tk.Toplevel(root)
    summary_window.title("Device Summary")

    summary_label = tk.Label(summary_window, text="Device Summary", font=("Arial", 14, "bold"))
    summary_label.pack(pady=10)

    summary_text = tk.Text(summary_window, height=30, width=90)
    summary_text.pack()

    summary_text.insert(tk.END, summary)
    summary_text.config(state=tk.DISABLED)  # Make the text widget read-only

def summarize():
    switching = float(switching_entry.get())
    throughput = float(throughput_entry.get())
    arp = int(arp_entry.get())
    bandwidth = int(bandwidth_entry.get())
    unicast_routes=float(unicast_routes_entry.get())
    multicast_routes=float(multicast_routes_entry.get())
    MAC_enteries=float(MAC_enteries_entry.get())
    nodes=int(nodes_entry.get())
    vrf=float(vrf_entry.get())
    layer2 = [l for l, v in zip(['IGMP', 'BPDU', 'VxLAN'], [layer2_igmp_var.get(), layer2_stp_var.get(), layer2_vxlan_var.get()]) if v]
    layer3 = [l for l, v in zip(['DHCP', 'ARP', 'UDP', 'OSPF', 'BGP'], [layer3_dhcp_var.get(), layer3_arp_var.get(), #layer3_udp_var.get(),
                                                                        layer3_ospf_var.get(), layer3_bgp_var.get()]) if v]

    G, compatible_devices = generate_campus_topology(switching, throughput, arp, bandwidth,unicast_routes,multicast_routes,MAC_enteries,vrf, layer2, layer3,nodes)

    summary = summarize_devices(compatible_devices)
    show_summary_window(summary)
def generate_feasibility_report(switching, throughput, arp, bandwidth, unicast_routes,
                                multicast_routes, MAC_enteries, vrf, topology_values):
    parameters = ['Switching Capacity', 'Throughput', 'ARP', 'Bandwidth', 'Unicast Routes', 'Multicast Routes', 'MAC Entries', 'VRF']

    user_values = [switching, throughput, arp, bandwidth, unicast_routes, multicast_routes, MAC_enteries, vrf]

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.2
    index = np.arange(len(parameters))

    user_bars = ax.bar(index - bar_width/2, user_values, bar_width, label='Business Goal', color='b')
    topology_bars = ax.bar(index + bar_width/2, topology_values, bar_width, label='Supported Scale', color='g')

    ax.set_xlabel('Parameters')
    ax.set_ylabel('Values')
    ax.set_title('Feasibility Report')
    ax.set_xticks(index)
    ax.set_xticklabels(parameters)
    ax.legend()

    # Function to calculate appropriate vertical offset for annotations
    def autolabel(bars, color):
        for bar in bars:
            height = bar.get_height()
            if color == 'b':
                ax.annotate(f'{height:.2f}',  # Rounded off to 2 decimal places
                            xy=(bar.get_x() + bar.get_width()/2, height),
                            xytext=(0, 4),  # Adjust y coordinate for vertical positioning
                            textcoords="offset points",
                            ha='right', va='bottom')
            else:
                ax.annotate(f'{height:.2f}',  # Rounded off to 2 decimal places
                            xy=(bar.get_x() + bar.get_width()/2, height),
                            xytext=(0, 4),  # Adjust y coordinate for vertical positioning
                            textcoords="offset points",
                            ha='left', va='bottom')

    autolabel(user_bars, 'b')
    autolabel(topology_bars, 'g')

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()


def show_device_summary1(compatible_devices):
    # Initialize totals and device type counts
    total_switching = total_throughput = total_arp = total_bandwidth = 0
    total_unicast = total_multicast = total_MAC_entries = total_vrf = 0
    access_nodes = []
    aggregate_nodes = []
    core_nodes = []
    
    # Process devices
    for device in compatible_devices:
        if device['type'] == 'access':
            access_nodes.append(device)
        elif device['type'] == 'aggregate':
            aggregate_nodes.append(device)
        elif device['type'] == 'core':
            core_nodes.append(device)

        total_switching += device['switching']
        total_throughput += device['throughput']
        total_arp += device['arp']
        total_bandwidth += device['bandwidth']
        total_unicast += device['unicast_routes']
        total_multicast += device['multicast_routes']
        total_MAC_entries += device['MAC_enteries']
        total_vrf += device['vrf']

    total_devices = len(compatible_devices)
    total_access_devices = len(access_nodes)
    total_aggregate_devices = len(aggregate_nodes)
    total_core_devices = len(core_nodes)
    
    # Data for bar chart
    metrics = ['Switching Capacity', 'Throughput Capacity', 'ARP Entries', 'Bandwidth', 'Unicast Routes', 'Multicast Routes', 'MAC Entries', 'VRF']
    totals = [total_switching, total_throughput, total_arp, total_bandwidth, total_unicast, total_multicast, total_MAC_entries, total_vrf]

    # Data for pie chart
    device_types = ['Access', 'Aggregate', 'Core']
    device_counts = [total_access_devices, total_aggregate_devices, total_core_devices]

    # Create bar chart
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(metrics, totals, color='skyblue')
    ax1.set_xlabel('Business Goal')
    ax1.set_ylabel('Supported Scale')
    ax1.set_title('Total Capacities for Each Business Goal')
    plt.xticks(rotation=45, ha='right')
    
    for i, v in enumerate(totals):
        ax1.text(i, v + max(totals)*0.01, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

    # Create pie chart
    fig, ax2 = plt.subplots(figsize=(8, 8))
    ax2.pie(device_counts, labels=device_types, autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'lightcoral', 'lightskyblue'])
    ax2.set_title('Distribution of Device Types')
    plt.axis('equal')
    plt.show()

    # Create separate bar charts for each metric
    for metric, total in zip(metrics, totals):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['Business Goal', 'Supported Scale'], [total/2, total], color=['orange', 'skyblue'])
        ax.set_ylabel('Value')
        ax.set_title(f'{metric}')
        
        for i, v in enumerate([total/2, total]):
            ax.text(i, v + total*0.01, str(v), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
def summarize1():
    switching = float(switching_entry.get())
    throughput = float(throughput_entry.get())
    arp = int(arp_entry.get())
    bandwidth = int(bandwidth_entry.get())
    unicast_routes=float(unicast_routes_entry.get())
    multicast_routes=float(multicast_routes_entry.get())
    MAC_enteries=float(MAC_enteries_entry.get())
    nodes=int(nodes_entry.get())
    vrf=float(vrf_entry.get())
    layer2 = [l for l, v in zip(['IGMP', 'STP', 'VxLAN'], [layer2_igmp_var.get(), layer2_stp_var.get(), layer2_vxlan_var.get()]) if v]
    layer3 = [l for l, v in zip(['DHCP', 'ARP', 'OSPF', 'BGP'], [layer3_dhcp_var.get(), layer3_arp_var.get(), #layer3_udp_var.get(),
                                                                        layer3_ospf_var.get(), layer3_bgp_var.get()]) if v]

    G, compatible_devices = generate_campus_topology(switching, throughput, arp, bandwidth,unicast_routes,multicast_routes,MAC_enteries,vrf, layer2, layer3,nodes)

    summary1 = show_device_summary1(compatible_devices)
    show_summary_window1(summary1)

def show_feasibility_report():
    switching = float(switching_entry.get())
    throughput = float(throughput_entry.get())
    arp = float(arp_entry.get())
    bandwidth = float(bandwidth_entry.get())
    unicast_routes = float(unicast_routes_entry.get())
    multicast_routes = float(multicast_routes_entry.get())
    MAC_enteries = float(MAC_enteries_entry.get())
    vrf = float(vrf_entry.get())
    nodes = int(nodes_entry.get())

    layer2_values = [
        layer2_igmp_var.get(),
        layer2_stp_var.get(),
        layer2_vxlan_var.get(),
    ]
    layer2_labels = ["IGMP", "STP", "VxLAN"]
    layer2 = [label for label, value in zip(layer2_labels, layer2_values) if value]

    layer3_values = [
        layer3_dhcp_var.get(),
        layer3_arp_var.get(),
        #layer3_udp_var.get(),
        layer3_ospf_var.get(),
        layer3_bgp_var.get(),
    ]
    layer3_labels = ["DHCP", "ARP", "UDP", "OSPF", "BGP"]
    layer3 = [label for label, value in zip(layer3_labels, layer3_values) if value]

    G, compatible_devices = generate_campus_topology(switching, throughput, arp, bandwidth, unicast_routes,
                                                      multicast_routes, MAC_enteries, vrf, layer2, layer3, nodes)
    
    print("Compatible devices:", compatible_devices)
    
    topology_values = [
        sum([device['switching'] for device in compatible_devices]),
        sum([device['throughput'] for device in compatible_devices]),
        sum([device['arp'] for device in compatible_devices]),
        sum([device['bandwidth'] for device in compatible_devices]),
        sum([device['unicast_routes'] for device in compatible_devices]),
        sum([device['multicast_routes'] for device in compatible_devices]),
        sum([device['MAC_enteries'] for device in compatible_devices]),
        sum([device['vrf'] for device in compatible_devices])
    ]
    
    print("Device Summary:", topology_values)
    parameters = ["switching", "throughput", "arp", "bandwidth", "unicast_routes", "multicast_routes", "MAC_enteries", "vrf"]
    user_values = [switching, throughput, arp, bandwidth, unicast_routes, multicast_routes, MAC_enteries, vrf]
    

    generate_feasibility_report(switching, throughput, arp, bandwidth, unicast_routes,
                                multicast_routes, MAC_enteries, vrf, topology_values)


import tkinter as tk
from tkinter import messagebox
import webbrowser

def pr_violation(switching_entry, throughput_entry, arp_entry, bandwidth_entry, unicast_routes_entry,
                 multicast_routes_entry, MAC_entries_entry, vrf_entry, nodes_entry):

    try:
        # Get the total values from the GUI
      
        switching = float(switching_entry.get())
        throughput = float(throughput_entry.get())
        arp = float(arp_entry.get())
        bandwidth = float(bandwidth_entry.get())
        unicast_routes = float(unicast_routes_entry.get())
        multicast_routes = float(multicast_routes_entry.get())
        MAC_entries = float(MAC_entries_entry.get())
        vrf = float(vrf_entry.get())
        nodes = int(nodes_entry.get())
        compatible_devices=[]
        i = 0
        j = 0
        k = 0
        total_switching = 0
        total_throughput = 0
        total_arp = 0
        total_bandwidth = 0
        total_unicast=0
        total_multicast=0
        total_MAC_enteries=0
        total_vrf=0
        
        

        while i < (nodes // 48):
            for device in access_device:
            
               i += 1
               compatible_devices.append(device)
                
        while j < (i // 2):
           for device in agg_device:
               compatible_devices.append(device)
            
               j += 1
            

        while k < (j // 2):
            for device in core_device:
                compatible_devices.append(device)
            
                k += 1
                 # Accumulate property totals
        for device in compatible_devices:
            total_switching += device['switching']
            total_throughput += device['throughput']
            total_arp += device['arp']
            total_bandwidth += device['bandwidth']
            total_unicast += device['unicast_routes']
            total_multicast += device['multicast_routes']
            total_MAC_enteries+= device['MAC_enteries']
            total_vrf += device['vrf']
        

        # Create a new window for PR Violations input
        pr_window = tk.Toplevel(root)
        pr_window.title("PR Violations")

        # Prompt user to input additional values
        switching_label = tk.Label(pr_window, text="Enter Switching Value:")
        switching_label.pack()
        switching_entry = tk.Entry(pr_window)
        switching_entry.pack()

        throughput_label = tk.Label(pr_window, text="Enter Throughput Value:")
        throughput_label.pack()
        throughput_entry = tk.Entry(pr_window)
        throughput_entry.pack()

        arp_label = tk.Label(pr_window, text="Enter ARP Value:")
        arp_label.pack()
        arp_entry = tk.Entry(pr_window)
        arp_entry.pack()

        bandwidth_label = tk.Label(pr_window, text="Enter Bandwidth Value:")
        bandwidth_label.pack()
        bandwidth_entry = tk.Entry(pr_window)
        bandwidth_entry.pack()

        unicast_routes_label = tk.Label(pr_window, text="Enter Unicast Routes Value:")
        unicast_routes_label.pack()
        unicast_routes_entry = tk.Entry(pr_window)
        unicast_routes_entry.pack()

        multicast_routes_label = tk.Label(pr_window, text="Enter Multicast Routes Value:")
        multicast_routes_label.pack()
        multicast_routes_entry = tk.Entry(pr_window)
        multicast_routes_entry.pack()

        MAC_entries_label = tk.Label(pr_window, text="Enter MAC Entries Value:")
        MAC_entries_label.pack()
        MAC_entries_entry = tk.Entry(pr_window)
        MAC_entries_entry.pack()

        vrf_label = tk.Label(pr_window, text="Enter VRF Value:")
        vrf_label.pack()
        vrf_entry = tk.Entry(pr_window)
        vrf_entry.pack()

        # Function to calculate PR Violations
        def calculate_violations():
            try:
                switching1 = float(switching_entry.get())
                throughput1 = float(throughput_entry.get())
                arp1 = float(arp_entry.get())
                bandwidth1 = float(bandwidth_entry.get())
                unicast_routes1 = float(unicast_routes_entry.get())
                multicast_routes1 = float(multicast_routes_entry.get())
                MAC_entries1 = float(MAC_entries_entry.get())
                vrf1 = float(vrf_entry.get())

                # Calculate PR Violations
                violation_message = ""
                if switching1+ switching > total_switching:
                    violation_message += f"Switching Capacity is being exceeded by {((switching1 +switching)- total_switching)/100}%.\n"
                if throughput1+throughput > total_throughput:
                    violation_message += f"Throughput is being exceeded by {((throughput1 +throughput)-total_throughput)/100}%.\n"
                if arp1+arp > total_arp:
                    violation_message += f"ARP is being exceeded by {((arp1 + arp)-total_arp)/100}.\n"
                if bandwidth1+bandwidth > total_bandwidth:
                    violation_message += f"Bandwidth is being exceeded by {((bandwidth1 + bandwidth)-total_bandwidth)/100}%.\n"
                if unicast_routes1+unicast_routes > total_unicast:
                    violation_message += f"Unicast Routes is being exceeded by {((unicast_routes1 +unicast_routes)-total_unicast)/100}%.\n"
                if multicast_routes1+multicast_routes > total_multicast:
                    violation_message += f"Multicast Routes is being exceeded by {((multicast_routes1 +multicast_routes)-total_multicast)/100}%.\n"
                if MAC_entries1+MAC_entries >  total_MAC_enteries:
                    violation_message += f"MAC Entries  is being exceeded by {((MAC_entries1 + MAC_entries)- total_MAC_enteries)/100}%.\n"
                if (vrf1+vrf) > total_vrf:
                    violation_message += f"VRF exceeded by {((vrf1 + vrf)-total_vrf)/100}%.\n"

                if violation_message:
                    show_violation_message(violation_message)
                else:
                    show_violation_message("No PR Violations detected.")
            except ValueError:
                show_violation_message("Please enter valid numerical values.")

        # Button to trigger calculations
        calculate_button = tk.Button(pr_window, text="Calculate", command=calculate_violations)
        calculate_button.pack()

    except ValueError:
        show_violation_message("Please enter valid numerical values.")
def show_violation_message(message):
    messagebox.showinfo("PR Violations", message)

root = tk.Tk()
root.title("Topology Generator")

def create_topology_label(text, row, column):
    label = tk.Label(root, text=text, font=("Helvetica", 10, "bold"))
    label.grid(row=row, column=column, padx=5, pady=5, sticky="w")

# Function to create checkboxes with a network topology theme
def create_topology_checkbox(text, var, row, column):
    checkbox = tk.Checkbutton(root, text=text, variable=var, font=("Helvetica", 10))
    checkbox.grid(row=row, column=column, padx=5, pady=5, sticky="w")

def create_topology_checkbox(text, var, row, column):
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Custom.TCheckbutton', background='#DADADA', font=('Helvetica', 10), borderwidth=0)
    checkbox = ttk.Checkbutton(root, text=text, variable=var, style='Custom.TCheckbutton')
    checkbox.grid(row=row, column=column, padx=5, pady=5, sticky="w")
    
switching_label = tk.Label(root, text="Switching Capacity(in Tbps):", font=("Helvetica", 10, "bold"))
switching_label.grid(row=0, column=0, padx=10, pady=5)
switching_entry = tk.Entry(root)
switching_entry.grid(row=0, column=1, padx=10, pady=5)
throughput_label = tk.Label(root, text="Throughput(in Mpps):", font=("Helvetica", 10, "bold"))
throughput_label.grid(row=1, column=0, padx=10, pady=5)
throughput_entry = tk.Entry(root)
throughput_entry.grid(row=1, column=1, padx=10, pady=5)

arp_label = tk.Label(root, text="ARP Entries:", font=("Helvetica", 10, "bold"))
arp_label.grid(row=2, column=0, padx=10, pady=5)
arp_entry = tk.Entry(root)
arp_entry.grid(row=2, column=1, padx=10, pady=5)

bandwidth_label = tk.Label(root, text="Bandwidth(in Tbps):", font=("Helvetica", 10, "bold"))
bandwidth_label.grid(row=3, column=0, padx=10, pady=5)
bandwidth_entry = tk.Entry(root)
bandwidth_entry.grid(row=3, column=1, padx=10, pady=5)

unicast_routes_label = tk.Label(root, text="Unicast Routes:", font=("Helvetica", 10, "bold"))
unicast_routes_label.grid(row=4, column=0, padx=10, pady=5)
unicast_routes_entry = tk.Entry(root)
unicast_routes_entry.grid(row=4, column=1, padx=10, pady=5)

multicast_routes_label = tk.Label(root, text="Multicast Routes:", font=("Helvetica", 10, "bold"))
multicast_routes_label.grid(row=5, column=0, padx=10, pady=5)
multicast_routes_entry = tk.Entry(root)
multicast_routes_entry.grid(row=5, column=1, padx=10, pady=5)

MAC_enteries_label = tk.Label(root, text="MAC Entries:", font=("Helvetica", 10, "bold"))
MAC_enteries_label.grid(row=6, column=0, padx=10, pady=5)
MAC_enteries_entry = tk.Entry(root)
MAC_enteries_entry.grid(row=6, column=1, padx=10, pady=5)

vrf_label = tk.Label(root, text="VRF:", font=("Helvetica", 10, "bold"))
vrf_label.grid(row=7, column=0, padx=10, pady=5)
vrf_entry = tk.Entry(root)
vrf_entry.grid(row=7, column=1, padx=10, pady=5)

layer2_label = tk.Label(root, text="Layer 2:", font=("Helvetica", 10, "bold"))
layer2_label.grid(row=8, column=0, padx=10, pady=5)
layer2_igmp_var = tk.IntVar()
layer2_igmp_check = tk.Checkbutton(root, text="IGMP", variable=layer2_igmp_var, font=("Helvetica", 10, "bold"))
layer2_igmp_check.grid(row=8, column=1, padx=5, pady=5, sticky="w")
layer2_stp_var = tk.IntVar()
layer2_stp_check = tk.Checkbutton(root, text="STP", variable=layer2_stp_var, font=("Helvetica", 10, "bold"))
layer2_stp_check.grid(row=8, column=2, padx=5, pady=5, sticky="w")
layer2_vxlan_var = tk.IntVar()
layer2_vxlan_check = tk.Checkbutton(root, text="VxLAN", variable=layer2_vxlan_var, font=("Helvetica", 10, "bold"))
layer2_vxlan_check.grid(row=8, column=3, padx=5, pady=5, sticky="w")

layer3_label = tk.Label(root, text="Layer 3:", font=("Helvetica", 10, "bold"))
layer3_label.grid(row=9, column=0, padx=10, pady=5)
layer3_dhcp_var = tk.IntVar()
layer3_dhcp_check = tk.Checkbutton(root, text="DHCP", variable=layer3_dhcp_var, font=("Helvetica", 10, "bold"))
layer3_dhcp_check.grid(row=9, column=1, padx=5, pady=5, sticky="w")
layer3_arp_var = tk.IntVar()
layer3_arp_check = tk.Checkbutton(root, text="ARP", variable=layer3_arp_var, font=("Helvetica", 10, "bold"))
layer3_arp_check.grid(row=9, column=2, padx=5, pady=5, sticky="w")
layer3_pim_var = tk.IntVar()
layer3_pim_check = tk.Checkbutton(root, text="PIM", variable=layer3_pim_var, font=("Helvetica", 10, "bold"))
layer3_pim_check.grid(row=9, column=3, padx=5, pady=5, sticky="w")
layer3_IPv6_var = tk.IntVar()
layer3_IPv6_check = tk.Checkbutton(root, text="IPv6", variable=layer3_IPv6_var, font=("Helvetica", 10, "bold"))
layer3_IPv6_check.grid(row=9, column=4, padx=5, pady=5, sticky="w")
##layer3_udp_var = tk.IntVar()
##layer3_udp_check = tk.Checkbutton(root, text="UDP", variable=layer3_udp_var, font=("Helvetica", 10, "bold"))
##layer3_udp_check.grid(row=9, column=3, padx=5, pady=5, sticky="w")
layer3_ospf_var = tk.IntVar()
layer3_ospf_check = tk.Checkbutton(root, text="OSPF", variable=layer3_ospf_var, font=("Helvetica", 10, "bold"))
layer3_ospf_check.grid(row=9, column=5, padx=5, pady=5, sticky="w")
layer3_bgp_var = tk.IntVar()
layer3_bgp_check = tk.Checkbutton(root, text="BGP", variable=layer3_bgp_var, font=("Helvetica", 10, "bold"))
layer3_bgp_check.grid(row=9, column=6, padx=5, pady=5, sticky="w")

nodes_label = tk.Label(root, text="No.of host/client devices:", font=("Helvetica", 10, "bold"))
nodes_label.grid(row=13, column=0, padx=10, pady=5)
nodes_entry = tk.Entry(root)
nodes_entry.grid(row=13, column=1, padx=10, pady=5)

show_topology_button = tk.Button(root, text="Show Topology", command=show_topology, font=("Helvetica", 10, "bold"))
show_topology_button.grid(row=14, column=1, padx=10, pady=10)

show_feasibility_button = tk.Button(root, text="Show Feasibility Report", command=show_feasibility_report, font=("Helvetica", 10, "bold"))
show_feasibility_button.grid(row=14, column=2, padx=10, pady=10)


summarize_button1 = tk.Button(root, text="Individual Feasibility", command=summarize1, font=("Helvetica", 10, "bold"))
summarize_button1.grid(row=14, column=3, padx=10, pady=10)

summarize_button = tk.Button(root, text="Summarize Devices", command=summarize, font=("Helvetica", 10, "bold"))
summarize_button.grid(row=14, column=5, padx=10, pady=10)


pr_button = tk.Button(root, text="PR Violations", command=lambda: pr_violation(
    switching_entry, throughput_entry, arp_entry, bandwidth_entry, unicast_routes_entry,
    multicast_routes_entry, MAC_enteries_entry, vrf_entry, nodes_entry), font=("Helvetica", 10, "bold"))
pr_button.grid(row=14, column=4, padx=10, pady=10)

root.mainloop()
