##################################################### 
# Collect Data - BODACC from SIREN of the Companies #
##################################################### 


# - Import Libraries -
import requests
import json
import pandas as pd


# - FUNCTIONS -
def getDataBODAAC(SIREN):
    SIREN = str(SIREN)
    if len(SIREN) != 9:
        print('INPUT does not correspond to a SIREN')
        return False
    
    bodacc_URL = 'https://bodacc-datadila.opendatasoft.com/api/records/1.0/search/?dataset=annonces-commerciales'
    bodacc_PARAMETERS = 'q=&rows=1000&sort=dateparution&facet=publicationavis&facet=publicationavis_facette&facet=typeavis&facet=typeavis_lib&facet=familleavis&facet=familleavis_lib&facet=numerodepartement&facet=departement_nom_officiel'
    api_URL = f'{bodacc_URL}&{bodacc_PARAMETERS}&refine.registre={SIREN}'

    try:
        r =  requests.get(api_URL)
        if r.status_code != 200:
            print(f'Request Failed -> {r.status_code}')
            return False
        
        rContent = json.loads(r.content)
        if rContent['nhits'] == 0: 
            print(f'No information regarding the SIREN -> {SIREN}')
            return False
        
        lsRecords = []
        lsFieldsInfo = ['id', 'publicationavis', 'publicationavis_facette', 'parution', 'dateparution', 'numeroannonce', 'typeavis', 'typeavis_lib', 'familleavis', 'familleavis_lib', 'numerodepartement', 'departement_nom_officiel', 'region_code', 'region_nom_officiel', 'tribunal', 'commercant', 'ville', 'registre', 'cp', 'pdf_parution_subfolder', 'ispdf_unitaire', 'listepersonnes', 'listeetablissements', 'jugement', 'acte', 'modificationsgenerales', 'radiationaurcs', 'depot', 'listeprecedentexploitant', 'listeprecedentproprietaire', 'divers', 'parutionavisprecedent']

        for record in rContent['records']:
            dictRecord = dict({'SIREN': SIREN, 'INTERNAL_RECRD_ID': record['recordid']})
            lsCurFieldKeys = list(filter(lambda cKey : cKey in lsFieldsInfo, record['fields'].keys()))
            dictRecord.update({fKey : record['fields'][fKey] for fKey in lsCurFieldKeys})
            lsRecords.append(dictRecord)  
            
        return pd.DataFrame.from_records(lsRecords)

    except Exception as e:
        print(f'Exception Raise -> {e}')
        return False
    

# - CORE -
if __name__ == '__main__':
    df_BODAAC = getDataBODAAC(382629442)