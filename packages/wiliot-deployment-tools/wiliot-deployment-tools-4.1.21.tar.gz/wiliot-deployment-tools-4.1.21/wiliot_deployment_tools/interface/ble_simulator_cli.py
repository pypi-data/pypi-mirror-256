from argparse import ArgumentParser
import time
from wiliot_deployment_tools.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.interface.uart_ports import get_uart_ports
from wiliot_deployment_tools.interface.uart_if import UARTInterface

def main():
    parser = ArgumentParser(prog='wlt-ble-sim',
                            description='BLE Simulator - CLI Tool to use GW BLE Simulator')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-p', type=str, help=f"USB UART Port (Available ports: {str(get_uart_ports())})", required=True)
    required.add_argument('-packet', type=str, help="packet", required=True)
    
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-c', type=int, help="channel (if not specified packet will be sent on all BLE adv. channels (37/38/39))")
    optional.add_argument('-delay', type=int, help="ms delay between packets (if not specified defaults to 20ms)")
    optional.add_argument('-dup', type=int, help="duplicates (defaults to 3)")
    optional.add_argument('-output', type=int, help="output power (defaults to 8dBm)")
    optional.add_argument('-ts', type=float, help="trigger by time stamp") 
    
    args = parser.parse_args()
    u = UARTInterface(args.p, update_fw=True)
    b = BLESimulator(u)
    b.set_sim_mode(True)
    b.trigger_by_time_stamp(args.ts)
    b.send_packet(args.packet, args.dup, args.output, args.c, args.delay)
    b.set_sim_mode(False)
    
def main_cli():
    main()


if __name__ == '__main__':
    main()
