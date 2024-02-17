from bgpy.as_graphs import PeerLink, CustomerProviderLink as CPLink

from bgpy.as_graphs import ASGraphInfo
from bgpy.enums import ASNs


r"""
Test relationship preference in gao_rexford.py.

  1---2
 /|  /|
4 | | |
 \| | |
  777-3

This tests all three possible relationship preference scenarios.
  1 prefers customer 777 over peer 2
  3 prefers peer 777 over provider 2
  4 prefers customer 777 over provider 1
"""

as_graph_info_017 = ASGraphInfo(
    peer_links=frozenset([PeerLink(1, 2), PeerLink(ASNs.VICTIM.value, 3)]),
    customer_provider_links=frozenset(
        [
            CPLink(provider_asn=1, customer_asn=4),
            CPLink(provider_asn=1, customer_asn=ASNs.VICTIM.value),
            CPLink(provider_asn=2, customer_asn=ASNs.VICTIM.value),
            CPLink(provider_asn=2, customer_asn=3),
            CPLink(provider_asn=4, customer_asn=ASNs.VICTIM.value),
        ]
    ),
)
