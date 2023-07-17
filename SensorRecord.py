from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from mbientlab.warble import *
import time


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
        print("%s" % (parse_value(data)))
#      print("%s -> %s" % (self.d2.address, parse_value(data)))

    def data_handler_accel_d2(self, ctx, data):
        print("data_handler_accel_d2")
        print("%s" % (parse_value(data)))

    #      print("%s -> %s" % (self.d2.address, parse_value(data)))

    def data_handler_gyro(self, ctx, data):
        print("data_handler_gyro")
        print("%s" % (parse_value(data)))
#       print("%s -> %s" % (self.d2.address, parse_value(data)))

    def stream_data_accel_d1(self):
        # Callback function pointer device 1
        callback_accel_d1 = FnVoid_VoidP_DataP(self.data_handler_accel_d1)
        # Setup the accelerometer sample frequency and range
        libmetawear.mbl_mw_acc_set_odr(self.d1.board, 16000.0)
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
        libmetawear.mbl_mw_acc_set_odr(self.d2.board, 16000.0)
        libmetawear.mbl_mw_acc_set_range(self.d2.board, 4.0)
        libmetawear.mbl_mw_acc_write_acceleration_config(self.d2.board)
        # Get the accelerometer data signal
        signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.d2.board)
        # Subscribe to it
        libmetawear.mbl_mw_datasignal_subscribe(signal, None, callback_accel_d2)
        # Enable the accelerometer
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.d2.board)
        libmetawear.mbl_mw_acc_start(self.d2.board)



    def stream_data_gyro(self):
        #    print("Streaming Data")
        # Callback function pointer
        callback_gyro_d1 = FnVoid_VoidP_DataP(self.data_handler_gyro)
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
        while True:
            self.stream_data_accel_d1()
            self.stream_data_accel_d2()
            self.stream_data_gyro()


    def get_device_count(self):
        return self.device_count


if __name__ == '__main__':
    reader = IMU_READER()
    reader.scan()
    if reader.get_device_count() == 2:
        reader.connect_to_devices()
    else:
        print("ERROR: Not Enough Devices Found:", reader.get_device_count())
