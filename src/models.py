from enum import Enum
import ipaddress


# AS possible IGPs
class IGP(Enum):
    OSPF = 1
    RIP = 2


class AS:
    def __init__(self, number: int, igp: "IGP", loopback_space: ipaddress.IPv6Network) -> None:
        self.number: int = number
        self.igp: "IGP" = igp
        self.loopback_space: ipaddress.IPv6Network = loopback_space
        self.routers: list["Router"] = []

    def __repr__(self) -> str:
        return f'AS number {self.number} with {self.igp.name} as IGP. Contains {len(self.routers)} routers using IP addresses from {self.loopback_space}'


class Router:
    def __init__(self, ID: str, As: "AS", border: bool) -> None:
        self.ID: str = ID
        self.As: "AS" = As
        self.loopback: ipaddress.IPv6Address = ipaddress.IPv6Address("::")
        self.border: bool = border
        self.interfaces: list["Router"] = []
        self.border_interfaces: list["Router"] = [] # Should be left empty if border is false

    def __repr__(self) -> str:
        return f'Router of ID {self.ID} in AS {self.As} with loopback {self.loopback} and connected to {len(self.interfaces)} routers. Is{'' if self.border else ' NOT'} a border router'


if __name__ == "__main__":
    pass