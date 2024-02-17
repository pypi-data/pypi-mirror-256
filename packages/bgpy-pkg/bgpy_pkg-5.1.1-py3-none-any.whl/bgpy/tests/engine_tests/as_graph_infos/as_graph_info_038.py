from bgpy.as_graphs import PeerLink, CustomerProviderLink as CPLink

from bgpy.as_graphs import ASGraphInfo
from bgpy.enums import ASNs


as_graph_info_038 = ASGraphInfo(
    peer_links=frozenset(
        [
            PeerLink(135, ASNs.VICTIM.value),
            PeerLink(7, 8),
            PeerLink(34, ASNs.ATTACKER.value),
            PeerLink(12, 34),
            PeerLink(11, 33),
        ]
    ),
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=ASNs.VICTIM.value, customer_asn=34),
            CPLink(provider_asn=135, customer_asn=34),
            CPLink(provider_asn=135, customer_asn=12),
            CPLink(provider_asn=12, customer_asn=11),
            CPLink(provider_asn=34, customer_asn=33),
            CPLink(provider_asn=11, customer_asn=1),
            CPLink(provider_asn=33, customer_asn=1),
            CPLink(provider_asn=1, customer_asn=6),
            CPLink(provider_asn=6, customer_asn=7),
            CPLink(provider_asn=6, customer_asn=8),
        ]
    ),
)
