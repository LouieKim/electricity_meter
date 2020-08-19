POINT_ID = 0
SLAVE = 1
FUNCTION_CODE = 2
MAP_ADDRESS = 3
DESCRIPTION = 4

class ModbusPointInfo():
    def __init__(self, modbus_info_tuple):
        self.point_id = modbus_info_tuple[POINT_ID]
        self.slave = modbus_info_tuple[SLAVE]
        self.function_code = modbus_info_tuple[FUNCTION_CODE]
        self.map_address = modbus_info_tuple[MAP_ADDRESS]
        self.description = modbus_info_tuple[DESCRIPTION]
    
    def get_point_id(self):
        return self.point_id

    def set_point_id(self, point_id):
        self.point_id = point_id
    
    def get_slave(self):
        return self.slave
    
    def set_slave(self, slave):
        self.slave = slave
    
    def get_function_code(self):
        return self.function_code

    def set_function_code(self, function_code):
        self.function_code = function_code
    
    def get_map_address(self):
        return self.map_address
    
    def set_map_address(self, map_address):
        self.map_address = map_address

    def get_description(self):
        return self.description
    
    def set_description(self, description):
        self.description = description

#if __name__ == "__main__":




    # exam_tuple01 = (1, 2, 3, 4, 'a')
    # exam_tuple02 = (5, 6, 7, 8, 'b')
    # exam_tuple03 = (9, 10, 11, 12, 'c')
    # exam_tuple04 = (13, 14, 15, 16, 'd')
    # exam_tuple05 = (17, 18, 19, 20, 'e')
    # exam_tuple06 = (21, 22, 23, 24, 'f')
    # exam_tuple07 = (25, 26, 27, 28, 'g')
    # exam_tuple08 = (29, 30, 31, 32, 'h')
    # exam_tuple09 = (33, 34, 35, 36, 'i')
    # exam_tuple10 = (37, 38, 39, 40, 'j')

    # exam_list = list()
    # exam_list = [exam_tuple01, exam_tuple02, exam_tuple03, exam_tuple04, exam_tuple05, exam_tuple06, exam_tuple07, exam_tuple08, exam_tuple09, exam_tuple10]

    # point_list = list()

    # for i in exam_list:
    #     point_list.append(ModbusPointInfo(i))

    # for j in point_list:
    #     if j.get_point_id() == 33:
    #         print(j.get_description())