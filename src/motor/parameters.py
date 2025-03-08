from enum import Enum
from typing import Literal

# Access types
READ_ONLY = "r"
READ_WRITE = "rw"


# Data types
class DataType(Enum):
    STRING = "string"
    FLOAT = "float"
    INT16 = "int16"
    INT32 = "int32"
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"


Parameters = (
    ####
    ## First table params
    ####
    # (0x0000, "Name", ParameterDataType.STRING, None, READ_WRITE),
    # (0x0001, "BarCode", ParameterDataType.STRING, None, READ_WRITE),
    # (0x1000, "BootCodeVersion", ParameterDataType.STRING, None, READ_ONLY),
    # (0x1001, "BootBuildDate", ParameterDataType.STRING, None, READ_ONLY),
    # (0x1002, "BootBuildTime", ParameterDataType.STRING, None, READ_ONLY),
    # (0x1003, "AppCodeVersion", ParameterDataType.STRING, None, READ_ONLY),
    # (0x1004, "AppGitVersion", ParameterDataType.STRING, None, READ_ONLY),
    # (0x1005, "AppBuildDate", ParameterDataType.STRING, None, READ_ONLY),
    # (0x1006, "AppBuildTime", ParameterDataType.STRING, None, READ_ONLY),
    # (0x1007, "AppCodeName", ParameterDataType.STRING, None, READ_ONLY),
    # (0x2000, "echoPara1", ParameterDataType.UINT16, (5, 74), READ_WRITE),
    # (0x2001, "echoPara2", ParameterDataType.UINT16, (5, 74), READ_WRITE),
    # (0x2002, "echoPara3", ParameterDataType.UINT16, (5, 74), READ_WRITE),
    # (0x2003, "echoPara4", ParameterDataType.UINT16, (5, 74), READ_WRITE),
    # (0x2004, "echoFreHz", ParameterDataType.UINT32, (1, 10000), READ_WRITE),
    # (0x2005, "MechOffset", ParameterDataType.FLOAT, (-7, 7), READ_ONLY),
    # (0x2006, "MechPos_init", ParameterDataType.FLOAT, (-50, 50), READ_WRITE),
    # (0x2008, "I_FW_MAX", ParameterDataType.FLOAT, (0, 33), READ_WRITE),
    # (0x2009, "motor_index", ParameterDataType.UINT8, (0, 20), READ_ONLY),
    # (0x200A, "CAN_ID", ParameterDataType.UINT8, (0, 127), READ_ONLY),
    # (0x200B, "CAN_MASTER", ParameterDataType.UINT8, (0, 127), READ_ONLY),
    # (0x200C, "CAN_TIMEOUT", ParameterDataType.UINT32, (0, 100000), READ_WRITE),
    # (0x200D, "motorOverTemp", ParameterDataType.INT16, (0, 1500), READ_WRITE),
    # (0x200E, "overTempTime", ParameterDataType.UINT32, (1000, 1000000), READ_WRITE),
    # (0x200F, "GearRatio", ParameterDataType.FLOAT, (1, 64), READ_WRITE),
    # (0x2010, "Tq_caliType", ParameterDataType.UINT8, (0, 1), READ_WRITE),
    # (0x2017, "spd_filt_gain", ParameterDataType.FLOAT, (0, 1), READ_WRITE),
    # (0x3000, "timeUse0", ParameterDataType.UINT16, None, READ_ONLY),
    # (0x3001, "timeUse1", ParameterDataType.UINT16, None, READ_ONLY),
    # (0x3002, "timeUse2", ParameterDataType.UINT16, None, READ_ONLY),
    # (0x3003, "timeUse3", ParameterDataType.UINT16, None, READ_ONLY),
    # (0x3004, "encoderRaw", ParameterDataType.UINT16, None, READ_ONLY),
    # (0x3005, "mcuTemp", ParameterDataType.INT16, None, READ_ONLY),
    # (0x3006, "motorTemp", ParameterDataType.INT16, None, READ_ONLY),
    # (0x3007, "vBus(mv)", ParameterDataType.UINT16, None, READ_ONLY),
    # (0x3008, "adc1Offset", ParameterDataType.INT32, None, READ_ONLY),
    # (0x3009, "adc2Offset", ParameterDataType.INT32, None, READ_ONLY),
    # (0x300A, "adc1Raw", ParameterDataType.UINT16, None, READ_ONLY),
    # (0x300B, "adc2Raw", ParameterDataType.UINT16, None, READ_ONLY),
    # (0x300D, "cmdId", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x300E, "cmdIq", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x300F, "cmdlocref", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3010, "cmdspdref", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3011, "cmdTorque", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3012, "cmdPos", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3013, "cmdVel", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3015, "modPos", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3018, "elecPos", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3019, "ia", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x301A, "ib", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x301B, "ic", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x301C, "tick", ParameterDataType.UINT32, None, READ_ONLY),
    # (0x301D, "phaseOrder", ParameterDataType.UINT8, None, READ_ONLY),
    # (0x301F, "boardTemp", ParameterDataType.INT16, None, READ_ONLY),
    # (0x3020, "iq", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3021, "id", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3022, "faultSta", ParameterDataType.UINT32, None, READ_ONLY),  # Fault status value
    # (0x3023, "warnSta", ParameterDataType.UINT32, None, READ_ONLY),  # Warning status value
    # (0x3024, "drv_fault", ParameterDataType.UINT16, None, READ_ONLY),
    # (0x3025, "drv_temp", ParameterDataType.INT16, None, READ_ONLY),
    # (0x3026, "Uq", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3027, "Ud", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3028, "dtc_u", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x3029, "dtc_v", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x302A, "dtc_w", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x302B, "v_bus", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x302C, "v_ref", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x302D, "torque_fdb", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x302E, "rated_i", ParameterDataType.FLOAT, None, READ_ONLY),
    # (0x302F, "limit_i", ParameterDataType.FLOAT, None, READ_ONLY),
    ####
    ## Second table params
    ####
    (0x7005, "run_mode", DataType.UINT8, (0, 3), READ_WRITE),
    (
        0x7006,
        "iq_ref",
        DataType.FLOAT,
        (-23, 23),
        READ_WRITE,
    ),  # Current Mode Iq Command
    (
        0x700A,
        "spd_ref",
        DataType.FLOAT,
        (-30, 30),
        READ_WRITE,
    ),  # Speed mode speed command
    (
        0x700B,
        "limit_torque",
        DataType.FLOAT,
        (0, 12),
        READ_WRITE,
    ),  # Torque limit
    (
        0x7010,
        "cur_kp",
        DataType.FLOAT,
        (0.0, 200.0),
        READ_WRITE,
    ),  # Kp of current
    (0x7011, "cur_ki", DataType.FLOAT, (0.0, 200.0), READ_WRITE),  # Current Ki
    (
        0x7014,
        "cur_filt_gain",
        DataType.FLOAT,
        (0, 1),
        READ_WRITE,
    ),  # Current filter coefficient filt_gain
    (
        0x7016,
        "loc_ref",
        DataType.FLOAT,
        (-12.56, 12.56),
        READ_WRITE,
    ),  # Position mode angle command
    (
        0x7017,
        "limit_spd",
        DataType.FLOAT,
        (0, 30),
        READ_WRITE,
    ),  # Position mode speed limit
    (
        0x7018,
        "limit_cur",
        DataType.FLOAT,
        (0, 23),
        READ_WRITE,
    ),  # Speed Position Mode Current Limit
    (
        0x7019,
        "mechPos",
        DataType.FLOAT,
        (-12.56, 12.56),
        READ_ONLY,
    ),  # Load end lap counting mechanical angle
    (0x701A, "iqf", DataType.FLOAT, (-23, 23), READ_ONLY),  # iq filter value
    (
        0x701B,
        "mechVel",
        DataType.FLOAT,
        (-30, 30),
        READ_ONLY,
    ),  # Load end speed
    (0x701C, "VBUS", DataType.FLOAT, None, READ_ONLY),  # bus voltage
    (0x701D, "rotation", DataType.INT16, None, READ_WRITE),  # Number of turns
    (
        0x701E,
        "loc_kp",
        DataType.FLOAT,
        (0, 200.0),
        READ_WRITE,
    ),  # kp of position
    (0x701F, "spd_kp", DataType.FLOAT, (0, 200.0), READ_WRITE),  # Speed in kp
    (0x7020, "spd_ki", DataType.FLOAT, (0, 200.0), READ_WRITE),  # Speed of ki
)

# Create the type for parameter names
ParamNames = set(param[1] for param in Parameters)

# For type hints
ParameterName = Literal[
    # "Name",
    # "BarCode",
    # "BootCodeVersion",
    # "BootBuildDate",
    # "BootBuildTime",
    # "AppCodeVersion",
    # "AppGitVersion",
    # "AppBuildDate",
    # "AppBuildTime",
    # "AppCodeName",
    # "echoPara1",
    # "echoPara2",
    # "echoPara3",
    # "echoPara4",
    # "echoFreHz",
    # "MechOffset",
    # "MechPos_init",
    # "limit_torque",
    # "I_FW_MAX",
    # "motor_index",
    # "CAN_ID",
    # "CAN_MASTER",
    # "CAN_TIMEOUT",
    # "motorOverTemp",
    # "overTempTime",
    # "GearRatio",
    # "Tq_caliType",
    # "cur_filt_gain",
    # "cur_kp",
    # "cur_ki",
    # "spd_kp",
    # "spd_ki",
    # "loc_kp",
    # "spd_filt_gain",
    # "limit_spd",
    # "limit_cur",
    # "timeUse0",
    # "timeUse1",
    # "timeUse2",
    # "timeUse3",
    # "encoderRaw",
    # "mcuTemp",
    # "motorTemp",
    # "vBus(mv)",
    # "adc1Offset",
    # "adc2Offset",
    # "adc1Raw",
    # "adc2Raw",
    # "VBUS",
    # "cmdId",
    # "cmdIq",
    # "cmdlocref",
    # "cmdspdref",
    # "cmdTorque",
    # "cmdPos",
    # "cmdVel",
    # "rotation",
    # "modPos",
    # "mechPos",
    # "mechVel",
    # "elecPos",
    # "ia",
    # "ib",
    # "ic",
    # "tick",
    # "phaseOrder",
    # "iqf",
    # "boardTemp",
    # "iq",
    # "id",
    # "faultSta",
    # "warnSta",
    # "drv_fault",
    # "drv_temp",
    # "Uq",
    # "Ud",
    # "dtc_u",
    # "dtc_v",
    # "dtc_w",
    # "v_bus",
    # "v_ref",
    # "torque_fdb",
    # "rated_i",
    # "limit_i",
    "run_mode",
    "iq_ref",
    "spd_ref",
    "limit_torque",
    "cur_kp",
    "cur_ki",
    "cur_filt_gain",
    "loc_ref",
    "limit_spd",
    "limit_cur",
    "mechPos",
    "iqf",
    "mechVel",
    "VBUS",
    "rotation",
    "loc_kp",
    "spd_kp",
    "spd_ki",
]


def get_parameter_by_name(name: str) -> tuple:
    """Get a parameter config value, by name"""
    return next(p for p in Parameters if p[1] == name)


def get_parameter_by_addr(addr: int) -> tuple:
    """Get a parameter config value by address"""
    return next(p for p in Parameters if p[0] == addr)
