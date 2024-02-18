from .router_objects import MTObject, IPAddress
from .exceptions import exception_control, RouterError, InvalidSearchAttribute
from .utilites import print_color
import re


class Address(MTObject):
    """
    Address managemen
    /ip address (object)
    """
    def __init__(self, connection):
        self.connection = connection
        self.address: IPAddress | None = None
        self.network: IPAddress | None = None
        self.interface: str | None = None
        self.comment: str | None = None
        self.numbers: str | None = None

        self.disabled: bool | None = None
        self.flags: str | None = None

    @exception_control
    def add(self, address: str, interface: str, network: str = None,
            comment: str = None, disabled: bool = False) -> 'Address':
        """
        Create a new item

        :param address: Local IP address
        :param interface: Interface name
        :param network: Network
        :param comment: Short description of the item
        :param disabled: Disable items
        :return: 'Address'
        """
        new_address = Address(connection=self.connection)
        new_address.address = IPAddress(address)
        if network:
            new_address.network = IPAddress(network)
        new_address.interface = interface
        new_address.comment = comment
        new_address.disabled = disabled
        command = f'/ip address add address="{new_address.address}" interface="{interface}"'
        command += f' network="{new_address.network}"' if network else ''
        command += f' comment="{new_address.comment}"' if comment else ''
        command += f' disabled="yes"' if disabled is True else ''

        result = self.connection.send_command(command)
        if result:
            raise RouterError(result)
        print_color(f"IP address '{new_address.address}' added to interface '{new_address.interface}'", 'cyan')
        return new_address

    @exception_control
    def set(self, find_by: dict or int, address: str = None, interface: str = None,
            network: str = None, disabled: bool = None, comment: str = None) -> 'Address':
        """
        Change item properties

        :param find_by: Either a dictionary or an integer indicating how to look up the IP address.
                        If it is a dictionary, it must contain key-value pairs for identifying the IP address.
                        If it is an integer, it represents a number from a list of IP addresses.
        :param address: Local IP address
        :param interface: Interface name
        :param network: Network
        :param disabled: Disable items
        :param comment: Short description of the item
        :return: 'Address'
        """
        edit_address = Address(connection=self.connection)
        if isinstance(find_by, int):
            command = f'/ip address set {find_by}'
        elif find_by.get('numbers', None) is not None:
            command = f'/ip address set {int(find_by["numbers"])}'
        else:
            self._checking_find_by_field(find_by)
            find = '[find'
            for k, v in find_by.items():
                find += f' {k}="{v}"'
            find += ']'
            command = f'/ip address set {find}'
        if address:
            edit_address.address = IPAddress(address)
            command += f' address="{edit_address.address}"'
        if interface:
            edit_address.interface = interface
            command += f' interface="{edit_address.interface}"'
        if network:
            edit_address.network = IPAddress(network)
            command += f' network="{edit_address.network}"'
        if disabled:
            edit_address.disabled = disabled
            command += f' disabled="yes"'
        if comment:
            edit_address.comment = comment
            command += f' comment="{edit_address.comment}"'
        result = self.connection.send_command(command)
        if result:
            raise RouterError(result)
        print_color('IP address parameters changed', 'cyan')
        return edit_address

    def __functions(self, func: str, numbers: int) -> 'Address':
        addresses = self.get_all()
        addresses_numbers = [address.numbers for address in addresses]
        if numbers not in addresses_numbers:
            raise InvalidSearchAttribute(f'There is no number {numbers} in the address list.\n'
                                         f'Here is a list of available numbers\n'
                                         f'{addresses_numbers}')
        command = f'/ip address {func} {numbers}'
        result = self.connection.send_command(command)
        if result:
            raise RouterError(result)
        return self.get_all()[numbers]

    def disable(self, numbers: int) -> 'Address':
        """
        Disable items

        :param numbers: List of item numbers
        :return: 'Address'
        """
        address = self.__functions('disable', numbers)
        print_color(f'IP address {str(address)} disabled', 'cyan')
        return address

    def enable(self, numbers: int):
        """
        Enable items

        :param numbers: List of item numbers
        :return: 'Address'
        """
        address = self.__functions('enable', numbers)
        print_color(f'IP address {str(address)} enabled', 'cyan')
        return address

    def remove(self, numbers: int):
        """
        Remove item

        :param numbers: List of item numbers
        :return: 'Address'
        """
        address = self.__functions('remove', numbers)
        print_color(f'IP address {str(address)} deleted', 'cyan')
        return address

    def get_all(self) -> list['Address']:
        """
        Get all items

        :return: list['Address']
        """
        command = '/ip address print detail'
        result = self.connection.send_command(command)
        pattern = re.compile(r'\s*(\d+)\s+([DIX]?)\s*(?:\s*;;; (.*?))?\s*address=([0-9./]+)\s+network=([0-9.]+)\s+interface=([^\s]+)')
        addresses_string = pattern.findall(result)

        addresses: list[Address] = []
        for _address in addresses_string:
            _index, flag, comment, address, network, interface = _address
            addresses.append(self.__create_an_object(_index, flag, comment, address, network, interface))
        return addresses

    def get_one(self, find_by: dict):
        """
        Get one items

        :param find_by: Either a dictionary or an integer indicating how to look up the IP address.
                        If it is a dictionary, it must contain key-value pairs for identifying the IP address.
                        If it is an integer, it represents a number from a list of IP addresses.
        """
        if isinstance(find_by, int):
            try:
                item = self.get_all()[0]
                return item
            except IndexError:
                raise InvalidSearchAttribute('Not find')
        else:
            self._checking_find_by_field(find_by)
            command = '/ip address print detail where '
            for k, v in find_by.items():
                if v:
                    command += f'{k}="{v}" '
            result = self.connection.send_command(command)
            pattern = re.compile(
                r'\s*(\d+)\s+([DIX]?)\s*(?:\s*;;; (.*?))?\s*address=([0-9./]+)\s+network=([0-9.]+)\s+interface=([^\s]+)')
            try:
                address_ = pattern.findall(result)[0]
            except IndexError:
                raise InvalidSearchAttribute('Not find')
            address = self.__create_an_object(*address_)
            return address

    def print_all(self) -> str:
        """
        Print out all items

        :return: String listing all items
        """
        addresses = self.get_all()
        text = ''
        for address in addresses:
            text += f'\n{str(address)}'
        print_color(text, 'cyan')
        return text

    def __create_an_object(self, _index, flag, comment, address, network, interface):
        ip_address = Address(connection=self.connection)
        ip_address.address = IPAddress(address)
        ip_address.network = IPAddress(network)
        ip_address.interface = interface
        ip_address.numbers = int(_index)
        ip_address.flags = flag
        if flag == 'X':
            ip_address.disabled = True
        if comment:
            ip_address.comment = comment
        return ip_address

    def __str__(self):
        st = f'{self.numbers} ' if self.numbers is not None else ''
        st += f'{self.flags} address={self.address} network={self.network} interface={self.interface}'
        if self.comment:
            st += f' comment={self.comment}'
        return st


class Ip:
    def __init__(self, connection):
        self.connection = connection

    @property
    def address(self):
        address = Address(connection=self.connection)
        return address



