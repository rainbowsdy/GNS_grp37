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
    def __init__(self, ID: str, border: bool) -> None:
        self.ID: str = ID
        self.border: bool = border
        self.interfaces: list["Router"] = []


if __name__ == "__main__":
    pass