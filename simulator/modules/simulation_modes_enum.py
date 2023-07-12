# © 2023 Coalfire
#
# Author: Rodney Beede

from enum import Enum

class SimulationMode(Enum):
    ALLOW_ALL_SAME_ACCOUNT = "cazt_scen0_Setup-Any"
    QA_SPECIFIC_API_RESOURCES = "cazt_scen1_QA_specific"
    QA_API_WILDCARD_REQUIRED = "cazt_scen1_QA_wildcard"
    CROSS_TENANT_ATTACK = "cazt_scen2_cross-tenant"
    SAME_ACCOUNT_ATTACK = "cazt_scen3_same-acct_specific"
    DENY_EXPLICIT = "cazt_scen4_explicit-deny"
    DENY_IMPLICIT = "cazt_scen4_implicit-deny"
    CLIENT_IP_ENFORCED = "cazt_scen5_ipaddress"
    CLIENT_IP_SPOOFED = "x-forwarded-for_header_seen"  # dynamically detected
    IMPERSONATION = "cazt_scen7_impersonation"
    HIERARCHICAL = "cazt_scen8_hierarchical"
    HTTP_101 = "upgrade-header"  # dynamically detected