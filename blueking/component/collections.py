# -*- coding: utf-8 -*-
"""Collections for component client"""
from .apis.bk_login import CollectionsBkLogin
from .apis.bk_paas import CollectionsBkPaas
from .apis.cc import CollectionsCC
from .apis.cmsi import CollectionsCMSI
from .apis.gse import CollectionsGSE
from .apis.job import CollectionsJOB
from .apis.sops import CollectionsSOPS
from .apis.get_capacity_api import CollectionsGetCapacity

# Available components
AVAILABLE_COLLECTIONS = {
    'bk_login': CollectionsBkLogin,
    'bk_paas': CollectionsBkPaas,
    'cc': CollectionsCC,
    'cmsi': CollectionsCMSI,
    'gse': CollectionsGSE,
    'job': CollectionsJOB,
    'sops': CollectionsSOPS,
    'get_capacity_api': CollectionsGetCapacity,
}
