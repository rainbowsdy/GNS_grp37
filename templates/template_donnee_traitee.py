routers = [
    {
        # ================= ROUTEUR R1 =================
        "hostname": "R1",
        "loopback": {
            "name": "Loopback0",
            "ipv6": "2001:db8:ffff::1/128"
        },
        "interfaces": [
            {
                "name": "Ethernet0/0",
                "shutdown": True,
                "duplex": "auto",
                "ipv6_addresses": [],
                "ipv6_enable": False
            },
            {
                "name": "GigabitEthernet0/0",
                "shutdown": True,
                "media_type": "gbic",
                "speed": 1000,
                "duplex": "full",
                "negotiation": "auto",
                "ipv6_addresses": [
                    "2001:100:4:4::/64 eui-64"
                ],
                "ipv6_enable": True
            },
            {
                "name": "GigabitEthernet1/0",
                "shutdown": False,
                "negotiation": "auto",
                "ipv6_addresses": [
                    "2001:100:1:1::/64 eui-64",
                    "2001:100:1:11::1/64",
                    "2001:100:1:12::1/64",
                    "2001:100:1:13::1/64",
                    "2001:200:200:201::1/64"
                ],
                "ipv6_enable": True,
                "ospf_area": 0,
                "rip_enable": True
            },
            {
                "name": "GigabitEthernet2/0",
                "shutdown": False,
                "negotiation": "auto",
                "ipv6_addresses": [
                    "2001:100:4:1::/64 eui-64"
                ],
                "ipv6_enable": True,
                "ospf_area": 0,
                "rip_enable": False
            }
        ],

        # ================= BGP =================
        "bgp": {
            "as": 111,
            "router_id": "1.1.1.1",
            "neighbors": [
                {
                    "address": "2001:100:4:1:C802:3EFF:FE4C:1C",
                    "remote_as": 112
                }
            ],
            "networks": [
                "2001:100:1:1::/64",
                "2001:100:1:11::/64",
                "2001:100:1:12::/64",
                "2001:100:1:13::/64",
                "2001:100:4:1::/64",
                "2001:100:4:4::/64",
                "2001:200:200:201::/64"
            ]
        },

        # ================= OSPFv3 =================
        "ospf": {
            "process_id": 1,
            "router_id": "1.1.1.1",
            "ipv6": True
        },

        # ================= RIPng =================
        "rip": {
            "process_name": "RIPNG",
            "default_metric": 1
        }
    },

    {
        # ================= ROUTEUR R2 =================
        "hostname": "R2",
        "loopback": {
            "name": "Loopback0",
            "ipv6": "2001:db8:ffff::1/128"
        },
        "interfaces": [
            {
                "name": "GigabitEthernet0/0",
                "shutdown": False,
                "ipv6_addresses": [
                    "2001:100:4:1::2/64"
                ],
                "ipv6_enable": True,
                "ospf_area": 0,
                "rip_enable": True
            }
        ],
        

        # R2 ne fait PAS de BGP
        # Pas de clé "bgp"

        "ospf": {
            "process_id": 1,
            "router_id": "2.2.2.2",
            "ipv6": True
        },

        "rip": {
            "process_name": "RIPNG"
        }
    }
]
