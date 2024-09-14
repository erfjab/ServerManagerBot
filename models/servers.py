from enum import Enum


class Actions(str, Enum):
    PowerOn = 'power_on'
    PowerOff = 'power_off'
    Reboot = 'reboot'
    ResetPassword = 'reset_password'
    Delete = 'delete'
    Home = 'home'
    Info = 'info'
    Rebuild = 'rebuild'
    Update = 'update'
    Reset = 'reset'