from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from mbientlab.warble import *
import time
from datetime import datetime
import csv

class IMU_READER():
    def __init__(self):
        self.device_id1 = "E7:21:4C:EE:1E:90"
        self.device_id2 = "D8:A6:2A:12:E7:68"
        self.d1 = MetaWear(self.device_id1)
        self.d2 = MetaWear(self.device_id2)
        self.device_count = 0
        self.d1_found = 0
        self.d2_found = 0
        self.d3_found = 0
        self.d1_a_file = "d1_accel_" + datetime.today().strftime('%Y_%m_%d')+".csv"
        self.d1_g_file = "d1_gyro_" + datetime.today().strftime('%Y_%m_%d')+".csv"
        self.d2_a_file = "d2_accel_" + datetime.today().strftime('%Y_%m_%d')+".csv"
        self.d2_g_file = "d2_gyro_" + datetime.today().strftime('%Y_%m_%d')+".csv"

        self.d1_acc_file = open(self.d1_a_file, "w", newline="\n")
        self.d1_acc_writer = csv.writer(self.d1_acc_file)
        self.d1_gyro_file = open(self.d1_g_file, "w", newline="\n")
        self.d1_gyro_writer = csv.writer(self.d1_gyro_file)

        self.d2_acc_file = open(self.d2_a_file, "w", newline="\n")
        self.d2_acc_writer = csv.writer(self.d2_acc_file)
        self.d2_gyro_file = open(self.d2_g_file, "w", newline="\n")
        self.d2_gyro_writer = csv.writer(self.d2_gyro_file)

    def scan_result_printer(self, result):
        print("mac: %s" % result.mac)
        print("name: %s" % result.name)
        print("rssi: %ddBm" % result.rssi)

        print("metawear service? %d" % result.has_service_uuid("326a9000-85cb-9195-d9dd-464cfbbae75a"))

        if result.mac == self.device_id1 and self.d1_found ==0:
            self.device_count += 1
            self.d1_found = 1

        if result.mac == self.device_id2 and self.d2_found ==0:
            self.device_count += 1
            self.d2_found = 1

        if self.device_count == 2:
            BleScanner.stop()

        print("======")

    # Callback function to process/parse the gyroscope data

    def data_handler_accel_d1(self, ctx, data):
        print("data_handler_accel_d1")
        value = parse_value(data)
        print("%s" % value)
        self.d1_acc_writer.writerow([time.time_ns(), value.x, value.y, value.z])

    def data_handler_accel_d2(self, ctx, data):
        print("data_handler_accel_d2")
        value = parse_value(data)
        print("%s" % value)
        self.d2_acc_writer.writerow([time.time_ns(), value.x, value.y, value.z])

    #      print("%s -> %s" % (self.d2.address, parse_value(data)))

    def data_handler_gyro_d1(self, ctx, data):
        print("data_handler_gyro_d1")
        value = parse_value(data)
        print("%s" % value)
        self.d1_gyro_writer.writerow([time.time_ns(), value.x, value.y, value.z])

    def data_handler_gyro_d2(self, ctx, data):
        print("data_handler_gyro_d2")
        value = parse_value(data)
        print("%s" % value)
        self.d2_gyro_writer.writerow([time.time_ns(), value.x, value.y, value.z])

    def stream_data_accel_d1(self):
        # Callback function pointer device 1
        callback_accel_d1 = FnVoid_VoidP_DataP(self.data_handler_accel_d1)
        # Setup the accelerometer sample frequency and range
        libmetawear.mbl_mw_acc_set_odr(self.d1.board, 100.0)
        libmetawear.mbl_mw_acc_set_range(self.d1.board, 4.0)
        libmetawear.mbl_mw_acc_write_acceleration_config(self.d1.board)
        # Get the accelerometer data signal
        signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.d1.board)
        # Subscribe to it
        libmetawear.mbl_mw_datasignal_subscribe(signal, None, callback_accel_d1)
        # Enable the accelerometer
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.d1.board)
        libmetawear.mbl_mw_acc_start(self.d1.board)

    def stream_data_accel_d2(self):
        # Callback function pointer device 2
        callback_accel_d2 = FnVoid_VoidP_DataP(self.data_handler_accel_d2)
        # Setup the accelerometer sample frequency and range
        libmetawear.mbl_mw_acc_set_odr(self.d2.board, 100.0)
        libmetawear.mbl_mw_acc_set_range(self.d2.board, 4.0)
        libmetawear.mbl_mw_acc_write_acceleration_config(self.d2.board)
        # Get the accelerometer data signal
        signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.d2.board)
        # Subscribe to it
        libmetawear.mbl_mw_datasignal_subscribe(signal, None, callback_accel_d2)
        # Enable the accelerometer
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.d2.board)
        libmetawear.mbl_mw_acc_start(self.d2.board)



    def stream_data_gyro_d1(self):
        #    print("Streaming Data")
        # Callback function pointer
        callback_gyro_d1 = FnVoid_VoidP_DataP(self.data_handler_gyro_d1)
        gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.d1.board)
        # Set ODR to 200Hz
        libmetawear.mbl_mw_gyro_bmi160_set_odr(self.d1.board, 200)
        #Set data range to +/250 degrees per second
        libmetawear.mbl_mw_gyro_bmi160_set_range(self.d1.board, 250)
        # Write the changes to the sensor
        libmetawear.mbl_mw_gyro_bmi160_write_config(self.d1.board)
        # Subscribe to it
        libmetawear.mbl_mw_datasignal_subscribe(gyro, None, callback_gyro_d1)
        libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(self.d1.board)
        libmetawear.mbl_mw_gyro_bmi160_start(self.d1.board)


    def stream_data_gyro_d2(self):
        #    print("Streaming Data")
        # Callback function pointer
        callback_gyro_d2 = FnVoid_VoidP_DataP(self.data_handler_gyro_d2)
        gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.d2.board)
        # Set ODR to 200Hz
        libmetawear.mbl_mw_gyro_bmi160_set_odr(self.d2.board, 200)
        #Set data range to +/250 degrees per second
        libmetawear.mbl_mw_gyro_bmi160_set_range(self.d2.board, 250)
        # Write the changes to the sensor
        libmetawear.mbl_mw_gyro_bmi160_write_config(self.d2.board)
        # Subscribe to it
        libmetawear.mbl_mw_datasignal_subscribe(gyro, None, callback_gyro_d2)
        libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(self.d2.board)
        libmetawear.mbl_mw_gyro_bmi160_start(self.d2.board)


    def scan(self):
        BleScanner.set_handler(self.scan_result_printer)
        print("-- active scan --")
        BleScanner.start()
        time.sleep(5.0)
        BleScanner.stop()



    def connect_to_devices(self):
        print("Connecting to device 1")
        self.d1.connect()
        libmetawear.mbl_mw_led_stop_and_clear(self.d1.board)  # turnoff all other LEDs
        pattern = LedPattern(repeat_count=Const.LED_REPEAT_INDEFINITELY)
        libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
        libmetawear.mbl_mw_led_write_pattern(self.d1.board, byref(pattern), LedColor.GREEN)
        libmetawear.mbl_mw_led_play(self.d1.board)
        print("Device 1 connected")

        print("Connecting to device 2")
        self.d2.connect()
        libmetawear.mbl_mw_led_stop_and_clear(self.d2.board)  # turnoff all other LEDs
        pattern = LedPattern(repeat_count=Const.LED_REPEAT_INDEFINITELY)
        libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
        libmetawear.mbl_mw_led_write_pattern(self.d2.board, byref(pattern), LedColor.GREEN)
        libmetawear.mbl_mw_led_play(self.d2.board)
        print("Device 2 connected")

        time.sleep(5)
        libmetawear.mbl_mw_led_stop_and_clear(self.d1.board)  # turnoff all other LEDs
        libmetawear.mbl_mw_led_stop_and_clear(self.d2.board)  # turnoff all other LEDs
        print("Beginning Data Streaming")
        self.stream_data()

    def stream_data(self):
        self.d1_acc_writer.writerow(["Epoch Time", "D1A X", "D1A Y", "D1A Z"])
        self.d1_gyro_writer.writerow(["Epoch Time", "D1G X", "D1G Y", "D1G Z"])
        self.d2_acc_writer.writerow(["Epoch Time", "D2A X", "D2A Y", "D2A Z"])
        self.d2_gyro_writer.writerow(["Epoch Time", "D2G X", "D2G Y", "D2G Z"])
        while True:
            self.stream_data_accel_d1()
            self.stream_data_accel_d2()
            self.stream_data_gyro_d1()
            self.stream_data_gyro_d2()



    def get_device_count(self):
        return self.device_count


if __name__ == '__main__':
    reader = IMU_READER()
    reader.scan()
    if reader.get_device_count() == 2:
        reader.connect_to_devices()
    else:
        print("ERROR: Not Enough Devices Found:", reader.get_device_count())
