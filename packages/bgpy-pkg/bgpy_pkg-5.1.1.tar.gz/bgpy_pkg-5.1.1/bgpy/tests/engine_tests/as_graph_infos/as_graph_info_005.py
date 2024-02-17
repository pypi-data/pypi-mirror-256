from bgpy.as_graphs.base.links import CustomerProviderLink as CPLink
from bgpy.as_graphs.base.links import PeerLink

from bgpy.as_graphs import ASGraphInfo
from bgpy.enums import ASNs


r"""v3 example with ROV++v2

      /1\\
    2 |  \attacker_asn
   /   |   \
  /    | 3 \
 4    |/  \ \
  \    5   victim_asn
   \  /
    6
"""

as_graph_info_005 = ASGraphInfo(
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=1, customer_asn=2),
            CPLink(provider_asn=1, customer_asn=5),
            CPLink(provider_asn=1, customer_asn=ASNs.VICTIM.value),
            CPLink(provider_asn=1, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=2, customer_asn=4),
            CPLink(provider_asn=4, customer_asn=9),
            CPLink(provider_asn=4, customer_asn=8),
            CPLink(provider_asn=4, customer_asn=10),
            CPLink(provider_asn=10, customer_asn=11),
            CPLink(provider_asn=11, customer_asn=6),
            CPLink(provider_asn=9, customer_asn=13),
            CPLink(provider_asn=13, customer_asn=6),
            CPLink(provider_asn=3, customer_asn=5),
            CPLink(provider_asn=3, customer_asn=ASNs.VICTIM.value),
            CPLink(provider_asn=5, customer_asn=8),
            CPLink(provider_asn=8, customer_asn=12),
            CPLink(provider_asn=13, customer_asn=15),
            CPLink(provider_asn=14, customer_asn=15),
            CPLink(provider_asn=11, customer_asn=15),
            CPLink(provider_asn=12, customer_asn=14),
            CPLink(provider_asn=14, customer_asn=6),
            CPLink(provider_asn=16, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=17, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=18, customer_asn=16),
            CPLink(provider_asn=18, customer_asn=17),
        ]
    ),
    peer_links=frozenset([PeerLink(18, 3)]),
)
