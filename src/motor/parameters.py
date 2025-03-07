from typing import Literal

# Access types
READ_ONLY = "r"
READ_WRITE = "rw"

# Data types
TYPE_STRING = "string"
TYPE_FLOAT = "float"
TYPE_INT16 = "int16"
TYPE_INT32 = "int32"
TYPE_UINT8 = "uint8"
TYPE_UINT16 = "uint16"
TYPE_UINT32 = "uint32"

Parameters = (
    ####
    ## First table params
    ####
    # (0x0000, "Name", TYPE_STRING, None, READ_WRITE),
    # (0x0001, "BarCode", TYPE_STRING, None, READ_WRITE),
    # (0x1000, "BootCodeVersion", TYPE_STRING, None, READ_ONLY),
    # (0x1001, "BootBuildDate", TYPE_STRING, None, READ_ONLY),
    # (0x1002, "BootBuildTime", TYPE_STRING, None, READ_ONLY),
    # (0x1003, "AppCodeVersion", TYPE_STRING, None, READ_ONLY),
    # (0x1004, "AppGitVersion", TYPE_STRING, None, READ_ONLY),
    # (0x1005, "AppBuildDate", TYPE_STRING, None, READ_ONLY),
    # (0x1006, "AppBuildTime", TYPE_STRING, None, READ_ONLY),
    # (0x1007, "AppCodeName", TYPE_STRING, None, READ_ONLY),
    # (0x2000, "echoPara1", TYPE_UINT16, (5, 74), READ_WRITE),
    # (0x2001, "echoPara2", TYPE_UINT16, (5, 74), READ_WRITE),
    # (0x2002, "echoPara3", TYPE_UINT16, (5, 74), READ_WRITE),
    # (0x2003, "echoPara4", TYPE_UINT16, (5, 74), READ_WRITE),
    # (0x2004, "echoFreHz", TYPE_UINT32, (1, 10000), READ_WRITE),
    # (0x2005, "MechOffset", TYPE_FLOAT, (-7, 7), READ_ONLY),
    # (0x2006, "MechPos_init", TYPE_FLOAT, (-50, 50), READ_WRITE),
    # (0x2008, "I_FW_MAX", TYPE_FLOAT, (0, 33), READ_WRITE),
    # (0x2009, "motor_index", TYPE_UINT8, (0, 20), READ_ONLY),
    # (0x200A, "CAN_ID", TYPE_UINT8, (0, 127), READ_ONLY),
    # (0x200B, "CAN_MASTER", TYPE_UINT8, (0, 127), READ_ONLY),
    # (0x200C, "CAN_TIMEOUT", TYPE_UINT32, (0, 100000), READ_WRITE),
    # (0x200D, "motorOverTemp", TYPE_INT16, (0, 1500), READ_WRITE),
    # (0x200E, "overTempTime", TYPE_UINT32, (1000, 1000000), READ_WRITE),
    # (0x200F, "GearRatio", TYPE_FLOAT, (1, 64), READ_WRITE),
    # (0x2010, "Tq_caliType", TYPE_UINT8, (0, 1), READ_WRITE),
    # (0x2017, "spd_filt_gain", TYPE_FLOAT, (0, 1), READ_WRITE),
    # (0x3000, "timeUse0", TYPE_UINT16, None, READ_ONLY),
    # (0x3001, "timeUse1", TYPE_UINT16, None, READ_ONLY),
    # (0x3002, "timeUse2", TYPE_UINT16, None, READ_ONLY),
    # (0x3003, "timeUse3", TYPE_UINT16, None, READ_ONLY),
    # (0x3004, "encoderRaw", TYPE_UINT16, None, READ_ONLY),
    # (0x3005, "mcuTemp", TYPE_INT16, None, READ_ONLY),
    # (0x3006, "motorTemp", TYPE_INT16, None, READ_ONLY),
    # (0x3007, "vBus(mv)", TYPE_UINT16, None, READ_ONLY),
    # (0x3008, "adc1Offset", TYPE_INT32, None, READ_ONLY),
    # (0x3009, "adc2Offset", TYPE_INT32, None, READ_ONLY),
    # (0x300A, "adc1Raw", TYPE_UINT16, None, READ_ONLY),
    # (0x300B, "adc2Raw", TYPE_UINT16, None, READ_ONLY),
    # (0x300D, "cmdId", TYPE_FLOAT, None, READ_ONLY),
    # (0x300E, "cmdIq", TYPE_FLOAT, None, READ_ONLY),
    # (0x300F, "cmdlocref", TYPE_FLOAT, None, READ_ONLY),
    # (0x3010, "cmdspdref", TYPE_FLOAT, None, READ_ONLY),
    # (0x3011, "cmdTorque", TYPE_FLOAT, None, READ_ONLY),
    # (0x3012, "cmdPos", TYPE_FLOAT, None, READ_ONLY),
    # (0x3013, "cmdVel", TYPE_FLOAT, None, READ_ONLY),
    # (0x3015, "modPos", TYPE_FLOAT, None, READ_ONLY),
    # (0x3018, "elecPos", TYPE_FLOAT, None, READ_ONLY),
    # (0x3019, "ia", TYPE_FLOAT, None, READ_ONLY),
    # (0x301A, "ib", TYPE_FLOAT, None, READ_ONLY),
    # (0x301B, "ic", TYPE_FLOAT, None, READ_ONLY),
    # (0x301C, "tick", TYPE_UINT32, None, READ_ONLY),
    # (0x301D, "phaseOrder", TYPE_UINT8, None, READ_ONLY),
    # (0x301F, "boardTemp", TYPE_INT16, None, READ_ONLY),
    # (0x3020, "iq", TYPE_FLOAT, None, READ_ONLY),
    # (0x3021, "id", TYPE_FLOAT, None, READ_ONLY),
    # (0x3022, "faultSta", TYPE_UINT32, None, READ_ONLY),  # Fault status value
    # (0x3023, "warnSta", TYPE_UINT32, None, READ_ONLY),  # Warning status value
    # (0x3024, "drv_fault", TYPE_UINT16, None, READ_ONLY),
    # (0x3025, "drv_temp", TYPE_INT16, None, READ_ONLY),
    # (0x3026, "Uq", TYPE_FLOAT, None, READ_ONLY),
    # (0x3027, "Ud", TYPE_FLOAT, None, READ_ONLY),
    # (0x3028, "dtc_u", TYPE_FLOAT, None, READ_ONLY),
    # (0x3029, "dtc_v", TYPE_FLOAT, None, READ_ONLY),
    # (0x302A, "dtc_w", TYPE_FLOAT, None, READ_ONLY),
    # (0x302B, "v_bus", TYPE_FLOAT, None, READ_ONLY),
    # (0x302C, "v_ref", TYPE_FLOAT, None, READ_ONLY),
    # (0x302D, "torque_fdb", TYPE_FLOAT, None, READ_ONLY),
    # (0x302E, "rated_i", TYPE_FLOAT, None, READ_ONLY),
    # (0x302F, "limit_i", TYPE_FLOAT, None, READ_ONLY),
    ####
    ## Second table params
    ####
    (0x7005, "run_mode", TYPE_UINT8, (0, 3), READ_WRITE),
    (0x7006, "iq_ref", TYPE_FLOAT, (-23, 23), READ_WRITE),  # Current Mode Iq Command
    (0x700A, "spd_ref", TYPE_FLOAT, (-30, 30), READ_WRITE),  # Speed mode speed command
    (0x700B, "limit_torque", TYPE_FLOAT, (0, 12), READ_WRITE),  # Torque limit
    (0x7010, "cur_kp", TYPE_FLOAT, (0.0, 200.0), READ_WRITE),  # Kp of current
    (0x7011, "cur_ki", TYPE_FLOAT, (0.0, 200.0), READ_WRITE),  # Current Ki
    (
        0x7014,
        "cur_filt_gain",
        TYPE_FLOAT,
        (0, 1),
        READ_WRITE,
    ),  # Current filter coefficient filt_gain
    (
        0x7016,
        "loc_ref",
        TYPE_FLOAT,
        (-12.56, 12.56),
        READ_WRITE,
    ),  # Position mode angle command
    (0x7017, "limit_spd", TYPE_FLOAT, (0, 30), READ_WRITE),  # Position mode speed limit
    (
        0x7018,
        "limit_cur",
        TYPE_FLOAT,
        (0, 23),
        READ_WRITE,
    ),  # Speed Position Mode Current Limit
    (
        0x7019,
        "mechPos",
        TYPE_FLOAT,
        (-12.56, 12.56),
        READ_ONLY,
    ),  # Load end lap counting mechanical angle
    (0x701A, "iqf", TYPE_FLOAT, (-23, 23), READ_ONLY),  # iq filter value
    (0x701B, "mechVel", TYPE_FLOAT, (-30, 30), READ_ONLY),  # Load end speed
    (0x701C, "VBUS", TYPE_FLOAT, None, READ_ONLY),  # bus voltage
    (0x701D, "rotation", TYPE_INT16, None, READ_WRITE),  # Number of turns
    (0x701E, "loc_kp", TYPE_FLOAT, (0, 200.0), READ_WRITE),  # kp of position
    (0x701F, "spd_kp", TYPE_FLOAT, (0, 200.0), READ_WRITE),  # Speed in kp
    (0x7020, "spd_ki", TYPE_FLOAT, (0, 200.0), READ_WRITE),  # Speed of ki
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
