# Attempting to reproduce serdes errors

See: https://github.com/SiliconLabs/pybgapi-examples/issues/2

This script, will run happily ~forever on my linux laptop, but when running on a 
lower powered cortex-a7, it rapidly crashes with errors such as captured below.

This only happens in an advertising rich environment.  If you implement NCP local filtering,
such as https://docs.silabs.com/bluetooth/5.0/general/ncp/local-event-handling-on-bluetooth-ncp-firmware
you will not see this issue.

```
2023-02-25 10:39:52,443 Thread-2 [WARNING] bgapi Received message 'bt_evt_scanner_legacy_advertisement_report' with 28 byte(s) extra payload.
2023-02-25 10:39:52,447 Thread-2 [DEBUG] bgapi.adv 3060356248 < bt_evt_scanner_legacy_advertisement_report(event_flags=2, address='7f:ae:26:dc:77:1b', address_type=1, bonding=255, rssi=-91, channel=39, target_address='28:a0:00:00:00:00', target_address_type=5, data=b'')
2023-02-25 10:39:52,448 MainThread [INFO] App#0 raw advertising: bt_evt_scanner_legacy_advertisement_report(event_flags=2, address='7f:ae:26:dc:77:1b', address_type=1, bonding=255, rssi=-91, channel=39, target_address='28:a0:00:00:00:00', target_address_type=5, data=b'')
Exception in thread Thread-2:
Traceback (most recent call last):
  File "/usr/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
  File "/usr/lib/python3.10/site-packages/bgapi/bglib.py", line 188, in run
    (apicmdevt, headers, params) = self.deser.parse(header, payload, fromHost=False)
  File "/usr/lib/python3.10/site-packages/bgapi/serdeser.py", line 226, in parse
    cmdevt = api[classIndex].commands[cmdEvtIndex]
KeyError: 160
```

or

```
2023-02-25 10:41:10,058 Thread-2 [DEBUG] bgapi.adv 3059930264 < bt_evt_scanner_legacy_advertisement_report(event_flags=3, address='f1:cf:54:1c:e8:55', address_type=1, bonding=255, rssi=-86, channel=37, target_address='00:00:00:00:00:00', target_address_type=0, data=b'\x07\xffL\x00\x12\x029\x01')
2023-02-25 10:41:10,060 MainThread [INFO] App#0 raw advertising: bt_evt_scanner_legacy_advertisement_report(event_flags=3, address='f1:cf:54:1c:e8:55', address_type=1, bonding=255, rssi=-86, channel=37, target_address='00:00:00:00:00:00', target_address_type=0, data=b'\x07\xffL\x00\x12\x029\x01')
Exception in thread Thread-2:
Traceback (most recent call last):
  File "/usr/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
  File "/usr/lib/python3.10/site-packages/bgapi/bglib.py", line 188, in run
    (apicmdevt, headers, params) = self.deser.parse(header, payload, fromHost=False)
  File "/usr/lib/python3.10/site-packages/bgapi/serdeser.py", line 309, in parse
    vals = struct.unpack("<%s" % pack_format, payload)
struct.error: unpack requires a buffer of 179 bytes
```