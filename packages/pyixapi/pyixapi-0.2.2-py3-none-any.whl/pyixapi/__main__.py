from pyixapi import api


def create_mac_address(ixapi, mac_address):
    """
    Create a new MAC address in IX-API. If the MAC already exists, return it
    without creation.
    """
    # Make sure to have a consistent case
    mac_address = str(mac_address).lower()

    # Return existing object if MAC already exists
    for mac in ixapi.macs.all():
        if mac["address"] == mac_address:
            return mac

    return ixapi.macs.create(
        address=mac_address, consuming_customer="2", managing_customer="2"
    )


# ixapi = api(
#    "https://api.de-cix.net/api/v1/",
#    "-GnNlMD8hBuxSSUJmpbfUkss9dyOKfTV1SnZibNyyr4",
#    "XKq8M6NVh5lCbPJ2Ml1h7V93QNIMsGVBfM6g2nRZF-E",
# )

ixapi = api(
    "https://api.de-cix.net/api/v2/",
    "lZJ_sV59gydj12RFATG4NaQFRI15iKRi9RC0oDqn2_A",
    "Yt_RImR_ymuhx2r9YQXerh5q9EyE6TxaREjzmEQNr1o",
)

# ixapi = api(
#    "http://localhost:8000/api/v1/",
#    "c25f077c899694fc",
#    "zZm-hzDIR5BZUhn5ULo4-_BQyx39ayRRn_0HFaSNDShqunrTiNY4a6n0Bnjqg62F-NsywRLvn3Dt3pRXWRgS1A",
# )

authentication = ixapi.authenticate()
print(authentication)

print(f"IX-API is at version {ixapi.version}")

authentication = ixapi.authenticate()
print(authentication)

print([i for i in ixapi.accounts.all()])

# for i in ixapi.ips.all():
#    print(f"{i.ip} - {i.network}")
# print(ixapi.network_service_configs.get("DXDB:PAS:509177"))

# for i in ixapi.ports.all():
#    print(i)

# print(len(ixapi.network_services.filter(consuming_customer="DXDB:CUST:1348")))
# print(len(ixapi.network_services.all()))

# mac = create_mac_address(ixapi, "e4:f7:ad:58:87:ff")

# for i in ixapi.macs.all():
#    print(dict(i))

# for i in ixapi.network_service_configs.all():
#    # i.macs = [mac]
#    # print(i.save())
#    i.update({"macs": [mac]})
#    print(dict(i))
