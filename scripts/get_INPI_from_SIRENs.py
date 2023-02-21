##################################################### 
# Collect Data - INIP from SIREN of the Companies #
##################################################### 

# - Import Libraries -
import requests
import pandas as pd


# - FUNCTIONS -
def setupLogin(baseURL="https://registre-national-entreprises.inpi.fr/api"): 
    username_INPI, password_INPI = "loicesnault95@gmail.com", "#Groupama2000#"
    loginURL = f"{baseURL}/sso/login"
    loginResponse = requests.post(loginURL, json={'username': username_INPI, 'password': password_INPI})
    if not loginResponse.status_code == 200:
        return None
    return loginResponse.json()['token']


# -- --
def construct_INPI_Dictionnary(response):
    
    dictContent = dict({})
    dictPath = dict({
        'SIREN': 'formality/siren',
        'TYPE_PERSONNE': 'formality/typePersonne',
        'NatureCreation': 'formality/content/natureCreation', 
        'PP-IDENTITE': 'formality/content/personnePhysique/identite', 
        'PP-DESCRIPTION': 'formality/content/personnePhysique/identite/description/datePremiereCloture', 
        'PP-CARACTERISTIQUE': 'formality/content/personnePhysique/adresseEntreprise/caracteristiques',
        'PP-ADRESSE': 'formality/content/personnePhysique/adresseEntreprise/adresse',
        'PP-ETABLISSEMENTS_PRINCIPAL': 'formality/content/personnePhysique/etablissementPrincipal',
        'PP-AUTRES_ETABLISSEMENTS': 'formality/content/personnePhysique/autresEtablissements',
        'PP-DEFAIL_CESSATION_ENTREPRISE': 'formality/content/personnePhysique/detailCessationEntreprise',
        'PP-BENEFICIARES_EFFECTIFS': 'formality/content/personnePhysique/beneficiairesEffectifs',
        'PP-OBSERVATIONS': 'formality/content/personnePhysique/observations',
        'PM-IDENTITE': 'formality/content/personneMorale/identite', 
        'PM-DESCRIPTION': 'formality/content/personneMorale/identite/description/datePremiereCloture', 
        'PM-CARACTERISTIQUE': 'formality/content/personneMorale/adresseEntreprise/caracteristiques',
        'PM-ADRESSE': 'formality/content/personneMorale/adresseEntreprise/adresse',
        'PM-ETABLISSEMENTS_PRINCIPAL': 'formality/content/personneMorale/etablissementPrincipal',
        'PM-AUTRES_ETABLISSEMENTS': 'formality/content/personneMorale/autresEtablissements',
        'PM-DEFAIL_CESSATION_ENTREPRISE': 'formality/content/personneMorale/detailCessationEntreprise',
        'PM-BENEFICIARES_EFFECTIFS': 'formality/content/personneMorale/beneficiairesEffectifs',
        'PM-OBSERVATIONS': 'formality/content/personneMorale/observations',
    })

    for pathKey in dictPath.keys():
        res = response
        subkeys = dictPath[pathKey].split('/')
        
        keyExists = True
        for sKey_ in subkeys:
            if sKey_ not in res.keys():
                keyExists = False
                break
            res = res[sKey_]
            
        if not keyExists:
            continue
        
        dictContent.update({pathKey: res})
        
    return dictContent

# -- --
def getDataINPI(baseURL="https://registre-national-entreprises.inpi.fr/api", SIRENs=[]):
    TOKEN_BEARER = setupLogin(baseURL)
    if not TOKEN_BEARER:
        print('Authentication Issue')
        return False
    
    if not isinstance(SIRENs, list):
        SIRENs = [SIRENs]

    SIRENs = "&".join(list(map(lambda vSIREN : f'siren[]={vSIREN}', SIRENs)))
    contentURL = f'{baseURL}/companies?{SIRENs}'
    headers =  {"Content-Type":"application/json", "Authorization": f"Bearer {TOKEN_BEARER}"}
    contentRequest = requests.get(contentURL, headers=headers)
    if not contentRequest.status_code == 200:
        return 
    
    lsContent = []
    for content in contentRequest.json():
        lsContent.append(construct_INPI_Dictionnary(content))
    return pd.DataFrame.from_records(lsContent)    



# - CORE -
if __name__ == '__main__':
    df_INIP = getDataINPI(SIRENs=382629442)
    print(df_INIP)