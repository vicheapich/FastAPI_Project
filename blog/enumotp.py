from enum import Enum


class OTPType(str, Enum):
    Phone = "Phone"
    Email = "Email"