from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from mbientlab.warble import *
import time


address = "E7:21:4C:EE:1E:90"
#address = "FD:40:3C:33:A9:99"
device = MetaWear(address)
global found
found = 0


def scan_result_printer(result):
    print("mac: %s" % result.mac)
    print("name: %s" % result.name)
    print("rssi: %ddBm" % result.rssi)

    print("metawear service? %d" % result.has_service_uuid("326a9000-85cb-9195-d9dd-464cfbbae75a"))

    if(result.mac == address):
        global found
        found = 1
        BleScanner.stop()

    data = result.get_manufacturer_data(0x626d)
    if data != None:
        print("mbientlab manufacturer data? ")
        print("    value: [%s]" % (', '.join([("0x%02x" % d) for d in data])))
    else:
        print("mbientlab manufacturer data? false")
    print("======")





def connect_device():

    #connect to device and change color to green on connection
    print("Connecting to device")
    device.connect()

    libmetawear.mbl_mw_led_stop_and_clear(device.board) #turnoff all other LEDs
    pattern = LedPattern(repeat_count=Const.LED_REPEAT_INDEFINITELY)
    libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
    libmetawear.mbl_mw_led_write_pattern(device.board, byref(pattern), LedColor.GREEN)
    libmetawear.mbl_mw_led_play(device.board)

    print("Device connected")


    # Callback function to process/parse the gyroscope data
def data_handler_accel(ctx, data):
    print("data_handler_accel")
    print("%s -> %s" % (device.address, parse_value(data)))


def data_handler_gyro(ctx, data):
    print("data_handler_gyro")
    print("%s -> %s" % (device.address, parse_value(data)))

def stream_data_accel():
#    print("Streaming Data")
    # Callback function pointer
    callback_accel = FnVoid_VoidP_DataP(data_handler_accel)

    # Setup the accelerometer sample frequency and range
    libmetawear.mbl_mw_acc_set_odr(device.board, 16000.0)
    libmetawear.mbl_mw_acc_set_range(device.board, 4.0)
    libmetawear.mbl_mw_acc_write_acceleration_config(device.board)

#    print("b1")
    # Get the accelerometer data signal
    signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(device.board)
#    print("b2")
    # Subscribe to it
    libmetawear.mbl_mw_datasignal_subscribe(signal, None, callback_accel)
#    print("b3")
    # Enable the accelerometer
    libmetawear.mbl_mw_acc_enable_acceleration_sampling(device.board)
    libmetawear.mbl_mw_acc_start(device.board)
#    print("b4")



def stream_data_gyro():
#    print("Streaming Data")
    # Callback function pointer
    callback_gyro = FnVoid_VoidP_DataP(data_handler_gyro)

    gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(device.board)


# Set ODR to 200Hz
    libmetawear.mbl_mw_gyro_bmi160_set_odr(device.board, 200)

# Set data range to +/250 degrees per second
    libmetawear.mbl_mw_gyro_bmi160_set_range(device.board, 250)

# Write the changes to the sensor
    libmetawear.mbl_mw_gyro_bmi160_write_config(device.board)

#    print("b1")
    # Get the gyroscope data signal
#    signal = libmetawear.mbl_mw_gyro_get_gyroscope_data_signal(device.board)
#    print("b2")
    # Subscribe to it
    libmetawear.mbl_mw_datasignal_subscribe(gyro, None, callback_gyro)
    libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(device.board)
    libmetawear.mbl_mw_gyro_bmi160_start(device.board)
#    print("b4")





BleScanner.set_handler(scan_result_printer)

print("-- active scan --")
BleScanner.start()
time.sleep(5.0)
BleScanner.stop()

#print("-- passive scan --")
#BleScanner.start(**{'scan_type': 'passive'})
#sleep(5.0)
#BleScanner.stop()


if found == 1:
 connect_device()
 while (True):
     stream_data_accel()
     stream_data_gyro()

else:
    print(found)
    print("device not found")




#time.sleep(3.0)
#device.disconnect()