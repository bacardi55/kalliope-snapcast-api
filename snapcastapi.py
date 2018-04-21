import telnetlib
import json
import time

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

import logging
logging.basicConfig()
logger = logging.getLogger("kalliope")


class Snapcastapi (NeuronModule):
    def __init__(self, **kwargs):
        super(Snapcastapi, self).__init__(**kwargs)

        # Get parameters:
        self.configuration = {
            "action": kwargs.get('action', None),
            "mac_addresses": kwargs.get('mac_addresses', '*'),
            "volume": kwargs.get('volume', '55'),
            "host": kwargs.get('host', '192.168.1.2'),
            "port": kwargs.get('port', '1705')
        }

        logger.debug(self.configuration)
        if self._is_parameters_ok():
            if self.configuration['action'] == 'mute':
                if isinstance(self.configuration['mac_addresses'], basestring) \
                        and self.configuration['mac_addresses'] == '*':
                    logger.debug("Muting all clients")
                    response = self.mute_all()
                else:
                    for mac in self.configuration['mac_addresses']:
                        logger.debug('Muting client %s' % mac)
                        self.mute(mac, True)
            elif self.configuration['action'] == 'unmute':
                if isinstance(self.configuration['mac_addresses'], basestring) \
                        and self.configuration['mac_addresses'] == '*':
                    logger.debug("Unmuting all clients")
                    self.mute_all(False)
                else:
                    for mac in self.configuration['mac_addresses']:
                        logger.debug('Unmuting client %s' % mac)
                        self.mute(mac, False)
            elif self.configuration['action'] == 'volume':
                if isinstance(self.configuration['mac_addresses'], basestring) \
                        and self.configuration['mac_addresses'] == '*':
                    logger.debug("Setting volume (%s) on all clients" % self.configuration['volume'])
                    self.set_volume_all(self.configuration['volume'])
                else:
                    for mac in self.configuration['mac_addresses']:
                        logger.debug("Setting volume (%s) on client %s" % (self.configuration['volume'], mac))
                        self.set_volume(mac, self.configuration['volume'])



    def mute(self, mac_address, toggle=True):
        payload = {
            "id": self.generate_id(),
            "jsonrpc": "2.0",
            "method": "Client.SetVolume",
            "params": {
                "id": mac_address,
                "volume": {
                    "muted": toggle
                }
            }
        }

        response = self.send_request(payload)
        return response


    def set_volume_all(self, volume):
        clients = self.get_clients()
        for client in clients:
            if client['connected'] is True:
                self.set_volume(client['host']['mac'], volume)


    def set_volume(self, mac_address, volume):
        payload = {
            "id": self.generate_id(),
            "jsonrpc": "2.0",
            "method": "Client.SetVolume",
            "params": {
                "id": mac_address,
                "volume": {
                    "muted": False,
                    "percent": int(volume)
                }
            }
        }

        response = self.send_request(payload)
        return response


    def mute_all(self, toggle=True):
        clients = self.get_clients()
        for client in clients:
            if client['connected'] is True:
                self.mute(client['host']['mac'], toggle)


    def get_server(self):
        payload = {
            "method": "Server.GetStatus",
            "jsonrpc": "2.0",
            "id": 56,  # todo
        }

        return self.send_request(payload)


    def send_request(self, payload):
        telnet = telnetlib.Telnet(self.configuration['host'], self.configuration['port'])
        if telnet is not None:
            logger.debug(payload)
            jobj = json.dumps(payload)
            requestId = payload['id']
            file = jobj.replace('\n', '')
            telnet.write(file + "\r\n")
            while (True):
                response = telnet.read_until("\r\n", 2)
                jResponse = json.loads(response)
                logger.debug(jResponse)
                if 'id' in jResponse:
                    if jResponse['id'] == requestId:
                        return jResponse

            return False


    def get_clients(self):
        s = self.get_server()
        clients = []
        for i, group in enumerate(s['result']['server']['groups']):
            for client in s['result']['server']['groups'][i]['clients']:
                clients.append(client)

        return clients


    def generate_id(self):
        return int(time.time())


    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """

        if self.configuration['action'] is None:
            raise InvalidParameterException("SnapcastAPI require Action parameter")

        if self.configuration['mac_addresses'] is None:
            raise InvalidParameterException("SnapcastAPI require mac_addresses parameter")
        elif isinstance(self.configuration['mac_addresses'], basestring) and \
                self.configuration['mac_addresses'] != '*':
            raise InvalidParameterException('Mac addresses should be a list of mac address or "*"')

        return True
