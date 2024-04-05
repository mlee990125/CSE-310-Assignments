from scapy.all import *

sender_ip = "130.245.145.12"
receiver_ip = "128.208.2.198"
#Read pcap
packets = rdpcap('assignment2.pcap')
print(f'Reading packets...')
connections = list()

def main():
    filter_packets(packets, connections)
    print(f'\nNumber of unique TCP flows: {len(connections)}')
    print('\n-----------------------------\n')
    analyze_tcp_flows(connections)
    print_congest_window_sizes(connections)
    print('\n-----------------------------\n')
    print_retransmissions(connections)
  

def filter_packets(packets, connections):
  for packet in packets:
    if 'IP' in packet:
      ip_layer = packet['IP']
      if 'TCP' in ip_layer:
        tcp_layer = ip_layer['TCP']
        add_to_connections(tcp_layer.sport, tcp_layer.dport, connections, packet)

def add_to_connections(sport, dport, connections, packet):
  if(len(connections) == 0):
    incoming_tcp_flow = list()
    incoming_tcp_flow.append(packet)
    connections.append(incoming_tcp_flow)
    return
  else:
    for tcp_flow in connections:
      if tcp_flow[0].sport == sport or tcp_flow[0].sport == dport:
        tcp_flow.append(packet)
        return
    
    incoming_tcp_flow = list()
    incoming_tcp_flow.append(packet)
    connections.append(incoming_tcp_flow)
    return

def analyze_tcp_flows(connections):
  for tcp_flow in connections:
    print(f'Source port: {tcp_flow[0].sport}, source IP address: {tcp_flow[0]["IP"].src}, destination port: {tcp_flow[0].dport}, destination IP address: {tcp_flow[0]["IP"].dst}')
    print()
    send_to_recv_flow = list(filter(lambda x: x.sport == tcp_flow[0].sport, tcp_flow))
    print('First two:')
    print(f' - Sequence number: {send_to_recv_flow[2].seq}, {send_to_recv_flow[3].seq}')
    print(f' - Ack number: {send_to_recv_flow[2].ack}, {send_to_recv_flow[3].ack}')
    print(f' - Receive Window size: {send_to_recv_flow[2].window}, {send_to_recv_flow[3].window}')
    print()

    total_data = 0
    total_time = send_to_recv_flow[-1].time - send_to_recv_flow[0].time

    for packet in send_to_recv_flow:
      data = packet.len - (packet.ihl * 4 + packet.dataofs * 4)
      total_data += data
    
    throughput = total_data / total_time
    print(f'Sender throughput: {throughput} bytes/sec')
    print('\n-----------------------------\n')


def print_congest_window_sizes(connections):
  for tcp_flow in connections:
    print(f'cwnd for src port {tcp_flow[0].sport}:\n')
    index = 3
    cwnd_count = 0
    congest_window_size = 0
    while cwnd_count < 3 and index < len(tcp_flow):
      flag = 0
      packet = tcp_flow[index]
      if(packet['IP'].src != tcp_flow[0]['IP'].src):
        if index < len(tcp_flow) - 1:
          if tcp_flow[index + 1]['IP'].src != tcp_flow[0]['IP'].src:
            index += 1
            flag = 1
          else:
            pass
        
        if flag == 1:
          continue
        print(f' - Congestion window size {cwnd_count + 1}: {congest_window_size} segments')
        cwnd_count += 1
        congest_window_size = 0
      else:
        congest_window_size += 1
      index += 1
  
    print()

def print_retransmissions(connections):
  for tcp_flow in connections:
    triple_ack_count = 0
    timeout_count = 0
    send_to_recv_flow = list(filter(lambda x: x.sport == tcp_flow[0].sport, tcp_flow))
    for i, packet in enumerate(send_to_recv_flow):
      if(check_repeat(packet.seq, send_to_recv_flow, i)):
        if(check_triple(packet.seq, tcp_flow, packet.id)):
          triple_ack_count += 1
        else:
          timeout_count += 1
    
    print(f'Retransmissions for src port {tcp_flow[0].sport}:\n')
    print(f' - Triple ack count: {triple_ack_count}')
    print(f' - Timeout count: {timeout_count - 1}\n')

def check_repeat(seq, send_to_recv_flow, index):
  j = 0
  while j < index:
    second_sequence = send_to_recv_flow[j].seq
    if(second_sequence == seq):
      return True
    j += 1
  return False

def check_triple(seq, tcp_flow, packet_id):
  ack_count = 0
  index = 0
  while index < len(tcp_flow):
    if tcp_flow[index].id == packet_id:
      break
    if ack_count > 2:
      return True
    elif tcp_flow[index].ack == seq:
      ack_count += 1
    else:
      pass

    index += 1
  return False

if __name__== "__main__":
    main()

