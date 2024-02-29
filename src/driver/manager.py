import threading
import collections


class DriverLockManager:
    def __init__(self):
        self._gvoice_phone_number_to_lock_map = collections.defaultdict()

    def get(self, gvoice_phone_number):
        if gvoice_phone_number not in self._gvoice_phone_number_to_lock_map:
            self._gvoice_phone_number_to_lock_map[gvoice_phone_number] = threading.Lock(
            )

        return self._gvoice_phone_number_to_lock_map[gvoice_phone_number]
