import usb_hid

SYSTEM_CONTROL_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls) (Vendor Defined 0xFF00)
    0x09, 0x80,  # Usage (System Control)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x05,  #   Report ID (5)
    0x15, 0x81,  #   Logical Minimum
    0x25, 0xBF,  #   Logical Maximum
    0x19, 0x81,  #   Usage Minimum
    0x29, 0xBF,  #   Usage Maximum
    0x75, 0x08,  #   Report Size
    0x95, 0x01,  #   Report Count
    0x81, 0x00,  #   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        # End Collection
))

system_control_usb_hid_device = usb_hid.Device(
    report_descriptor=SYSTEM_CONTROL_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x80,                # system_control
    report_ids=(5,),
    in_report_lengths=(1,),
    out_report_lengths=(0,),
)

usb_hid.enable((
    usb_hid.Device.KEYBOARD,
    usb_hid.Device.CONSUMER_CONTROL,
    system_control_usb_hid_device,
    )
)