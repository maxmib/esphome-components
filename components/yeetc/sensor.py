import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart

from esphome.const import (
    CONF_FORMALDEHYDE,
    CONF_HUMIDITY,
    CONF_ID,
    CONF_PM_10_0,
    CONF_PM_1_0,
    CONF_PM_2_5,
    CONF_PM_0_3UM,
    CONF_PM_0_5UM,
    CONF_PM_1_0UM,
    CONF_PM_2_5UM,
    CONF_PM_5_0UM,
    CONF_PM_10_0UM,
    CONF_UPDATE_INTERVAL,
    CONF_TEMPERATURE,
    CONF_TYPE,
    DEVICE_CLASS_PM1,
    DEVICE_CLASS_PM10,
    DEVICE_CLASS_PM25,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    ICON_CHEMICAL_WEAPON,
    STATE_CLASS_MEASUREMENT,
    UNIT_MICROGRAMS_PER_CUBIC_METER,
    UNIT_CELSIUS,
    UNIT_COUNT_DECILITRE,
    UNIT_PERCENT,
)

DEPENDENCIES = ["uart"]

yeetc_ns = cg.esphome_ns.namespace("yeetc")
yeetcComponent = yeetc_ns.class_("yeetcComponent", uart.UARTDevice, cg.Component)
yeetcSensor = yeetc_ns.class_("yeetcSensor", sensor.Sensor)

TYPE_AC4G = "AC4G"
TYPE_PMS5003T = "PMS5003T"
TYPE_PMS5003ST = "PMS5003ST"
TYPE_PMS5003S = "PMS5003S"

yeetcType = yeetc_ns.enum("yeetcType")

yeetc_TYPES = {
    TYPE_AC4G: yeetcType.yeetc_TYPE_AC4G,
    TYPE_PMS5003T: yeetcType.yeetc_TYPE_5003T,
    TYPE_PMS5003ST: yeetcType.yeetc_TYPE_5003ST,
    TYPE_PMS5003S: yeetcType.yeetc_TYPE_5003S,
}

SENSORS_TO_TYPE = {
    CONF_PM_1_0: [TYPE_AC4G, TYPE_PMS5003ST, TYPE_PMS5003S],
    CONF_PM_2_5: [TYPE_AC4G, TYPE_PMS5003T, TYPE_PMS5003ST, TYPE_PMS5003S],
    CONF_PM_10_0: [TYPE_AC4G, TYPE_PMS5003ST, TYPE_PMS5003S],
    CONF_TEMPERATURE: [TYPE_PMS5003T, TYPE_PMS5003ST],
    CONF_HUMIDITY: [TYPE_PMS5003T, TYPE_PMS5003ST],
    CONF_FORMALDEHYDE: [TYPE_PMS5003ST, TYPE_PMS5003S],
}


def validate_yeetc_sensors(value):
    for key, types in SENSORS_TO_TYPE.items():
        if key in value and value[CONF_TYPE] not in types:
            raise cv.Invalid(f"{value[CONF_TYPE]} does not have {key} sensor!")
    return value


def validate_update_interval(value):
    value = cv.positive_time_period_milliseconds(value)
    if value == cv.time_period("0s"):
        return value
    if value < cv.time_period("30s"):
        raise cv.Invalid(
            "Update interval must be greater than or equal to 30 seconds if set."
        )
    return value


CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(yeetcComponent),
            cv.Required(CONF_TYPE): cv.enum(yeetc_TYPES, upper=True),
            cv.Optional(CONF_PM_1_0): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PM_2_5): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PM_10_0): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PM_0_3UM): sensor.sensor_schema(
                unit_of_measurement=UNIT_COUNT_DECILITRE,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_PM_0_5UM): sensor.sensor_schema(
                unit_of_measurement=UNIT_COUNT_DECILITRE,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_PM_1_0UM): sensor.sensor_schema(
                unit_of_measurement=UNIT_COUNT_DECILITRE,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_PM_2_5UM): sensor.sensor_schema(
                unit_of_measurement=UNIT_COUNT_DECILITRE,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_PM_5_0UM): sensor.sensor_schema(
                unit_of_measurement=UNIT_COUNT_DECILITRE,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_PM_10_0UM): sensor.sensor_schema(
                unit_of_measurement=UNIT_COUNT_DECILITRE,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_HUMIDITY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_FORMALDEHYDE): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_UPDATE_INTERVAL, default="0s"): validate_update_interval,
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA)
)


def final_validate(config):
    require_tx = config[CONF_UPDATE_INTERVAL] > cv.time_period("0s")
    schema = uart.final_validate_device_schema(
        "yeetc", baud_rate=9600, require_rx=True, require_tx=require_tx
    )
    schema(config)


FINAL_VALIDATE_SCHEMA = final_validate


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    cg.add(var.set_type(config[CONF_TYPE]))

    if CONF_PM_1_0 in config:
        sens = await sensor.new_sensor(config[CONF_PM_1_0])
        cg.add(var.set_pm_1_0_sensor(sens))

    if CONF_PM_2_5 in config:
        sens = await sensor.new_sensor(config[CONF_PM_2_5])
        cg.add(var.set_pm_2_5_sensor(sens))

    if CONF_PM_10_0 in config:
        sens = await sensor.new_sensor(config[CONF_PM_10_0])
        cg.add(var.set_pm_10_0_sensor(sens))

    if CONF_PM_0_3UM in config:
        sens = await sensor.new_sensor(config[CONF_PM_0_3UM])
        cg.add(var.set_pm_particles_03um_sensor(sens))

    if CONF_PM_0_5UM in config:
        sens = await sensor.new_sensor(config[CONF_PM_0_5UM])
        cg.add(var.set_pm_particles_05um_sensor(sens))

    if CONF_PM_1_0UM in config:
        sens = await sensor.new_sensor(config[CONF_PM_1_0UM])
        cg.add(var.set_pm_particles_10um_sensor(sens))

    if CONF_PM_2_5UM in config:
        sens = await sensor.new_sensor(config[CONF_PM_2_5UM])
        cg.add(var.set_pm_particles_25um_sensor(sens))

    if CONF_PM_5_0UM in config:
        sens = await sensor.new_sensor(config[CONF_PM_5_0UM])
        cg.add(var.set_pm_particles_50um_sensor(sens))

    if CONF_PM_10_0UM in config:
        sens = await sensor.new_sensor(config[CONF_PM_10_0UM])
        cg.add(var.set_pm_particles_100um_sensor(sens))

    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(sens))

    if CONF_HUMIDITY in config:
        sens = await sensor.new_sensor(config[CONF_HUMIDITY])
        cg.add(var.set_humidity_sensor(sens))

    if CONF_FORMALDEHYDE in config:
        sens = await sensor.new_sensor(config[CONF_FORMALDEHYDE])
        cg.add(var.set_formaldehyde_sensor(sens))

    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))
