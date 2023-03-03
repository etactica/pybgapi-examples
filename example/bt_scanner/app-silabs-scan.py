#!/usr/bin/env python3
"""
Simple, silabs example style to just dump all advertisements forever
this _also_ crashes fairly promptly on my cortex-a7 system!
"""
import logging
import os.path
import sys
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from common.util import ArgumentParser, BluetoothApp, get_connector

logging.basicConfig(format='%(asctime)s %(threadName)s [%(levelname)s] %(name)s %(message)s',
                    level=logging.DEBUG,  # leave this, so that the trace handlers get enough info
                    )
logging.getLogger("bgapi").setLevel(logging.DEBUG)
logging.getLogger("bgapi.adv").setLevel(logging.DEBUG)


class App(BluetoothApp):

    def __init__(self, connector):
        self.ev_boot = threading.Event()
        self.log = logging.getLogger("AppMain")
        super().__init__(connector)

    def event_handler(self, evt):
        # This event indicates the device has started and the radio is ready.
        if evt == "bt_evt_system_boot":
            self.ev_boot.set()
            self.log.info("Marked as booted")
            # Ok, we're booted, turn on ALLL THE THINGS
            self.lib.bt.scanner.start(self.lib.bt.scanner.SCAN_PHY_SCAN_PHY_1M, self.lib.bt.scanner.DISCOVER_MODE_DISCOVER_OBSERVATION)
            self.log.info("scanning started")

        # This event is generated when an advertisement packet or a scan response
        # is received from a responder
        elif evt == "bt_evt_scanner_legacy_advertisement_report":
            self.log.info("raw advertising: %s", evt)
            #if evt.address.upper().startswith("F0:82") and evt.rssi > -70:


# Script entry point.
if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    args = parser.parse_args()
    connector = get_connector(args)
    # Instantiate the application.
    app = App(connector)
    # Running the application blocks execution until it terminates.
    app.run()
    print("started app, dangling now?")
