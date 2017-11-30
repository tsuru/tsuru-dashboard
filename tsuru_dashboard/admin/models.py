from dateutil import parser
from pytz import utc
from urlparse import urlparse
from collections import defaultdict


def extract_ip(address):
    if not urlparse(address).scheme:
        address = "http://"+address
    return urlparse(address).hostname


class Node():
    def __init__(self, data, units_responses=None):
        self.data = data or {}
        self.units = []
        if not units_responses:
            return
        for response in units_responses:
            if not response:
                continue

            if response.status_code != 200:
                continue

            node_units = response.json()
            if not node_units:
                continue

            addr = node_units[0].get('HostAddr') or node_units[0].get('hostaddr')
            if not addr:
                continue

            if extract_ip(addr) == extract_ip(self.address()):
                self.units = node_units

    def address(self):
        return self.data.get('Address')

    def last_success(self):
        date = self.metadata().get("LastSuccess")
        if date:
            last_success = parser.parse(date)
            if last_success.tzinfo:
                last_success = last_success.astimezone(utc)
            else:
                last_success = utc.localize(last_success)
            return last_success
        return date

    def metadata(self):
        return self.data.get("Metadata") or {}

    def pool(self):
        pool = self.data.get("Pool", self.data.get("pool"))
        if pool:
            return pool
        return str(self.metadata().get("pool"))

    def status(self):
        return self.data.get("Status")

    def units_stats(self):
        result = defaultdict(int)
        for unit in self.units:
            unit_status = unit.get('Status') or unit.get('status')
            if unit_status:
                result[unit_status] += 1

        len_units = len(self.units)
        if len_units > 0:
            result['total'] = len_units

        return result

    def to_dict(self):
        return {
            'address': self.address(),
            'metadata': self.metadata(),
            'last_success': self.last_success(),
            'pool': self.pool(),
            'status': self.status(),
            'units_stats': self.units_stats(),
            'units': self.units,
        }
