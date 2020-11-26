"""
uniprot python interface
to access the uniprot database

available services:
    map
    retrieve
"""

import requests
import sys, argparse

def pfam_from_uniprot(uniprot):
r = requests.get(f"https://www.uniprot.org/uniprot/{uniprot}.xml")
if r.ok:
record = bpio.read(StringIO(r.text),"uniprot-xml")
return [x.split(":")[1] for x in record.dbxrefs if x.startswith("Pfam:") ]
raise Exception(f"error retrieving {uniprot}")

url = 'https://www.uniprot.org/'

def _retrieve(query, format='fasta'):
    """_retrieve is not meant for use with the python interface, use `retrieve`
    instead"""
      
    return _map(query, 'ACC+ID', 'ACC', format=format) 

def retrieve(ids, format='fasta'):
    """ request entries by uniprot acc using batch retrieval

    Args:
        query: list of ids to retrieve
        format: fasta by default

    Help:
        possible formats:
        txt, xml, rdf, gff"""
    if type(ids) is not list:
        ids = [ids]
    return _retrieve(' '.join(ids), format)

def _map(query, f, t, format='tab'):
    """ _map is not meant for use with the python interface, use `map` instead
    """
    tool = 'uploadlists/'

    data = {
            'from':f,
            'to':t,
            'format':format,
            'query':query
            }
    response = requests.post(url + tool, data=data)
    page = response.text
    return page

def map(ids, f, t, format='tab'):
    """ map a list of ids from one format onto another using uniprots mapping api
    
    Args:
        query: id or list of ids to be mapped
        f: from ACC | P_ENTREZGENEID | ...
        t: to ...
        format: tab by default

    Help:
        for a list of all possible mappings visit
        'https://www.uniprot.org/help/api_idmapping'
    """
    if type(ids) is not list:
        ids = [ids]
    page = _map(' '.join(ids), f, t, format)
    result = dict()
    for row in page.splitlines()[1:]:
        key, value = row.split('\t')
        if key in result:
            result[key].add(value)
        else:
            result[key] = set([value])
    return result
