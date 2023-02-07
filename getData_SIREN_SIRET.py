####################################################################### 
# Collect Data - SIREN/SIRET of the Companies and their Establishment #
####################################################################### 


# - Import Libraries -
import sys
import os
import wget
import zipfile


# - FUNCTIONS -
def barProgress(current, total):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()
    


# - CORE -
if __name__ == '__main__':
    
    # -- Set Paths (data and tmp) --
    pathData = 'data'
    pathTMP = os.path.join(pathData, 'tmp')
    os.makedirs(pathTMP, exist_ok=True)
    
    
    # -- Define a dictionnary containing information about the Stocks (SIREN/SIRET) Data URLs --
    dictStocks = dict({
    'CORE_URL': 'https://www.data.gouv.fr/fr/datasets/r/',
    'Stock Etablissement Historique': {'URL': '88fbb6b4-0320-443e-b739-b4376a012c32', 'UPDATE': '2023_02_01'},
    'Stock Etablissement': {'URL': '0651fb76-bcf3-4f6a-a38d-bc04fa708576', 'UPDATE': '2023_02_01'},
    'Stock Unite Legale Historique': {'URL': '0835cd60-2c2a-497b-bc64-404de704ce89', 'UPDATE': '2023_02_01'},
    'Stock Etablissement Liens Succession': {'URL': '9c4d5d9c-4bbb-4b9c-837a-6155cb589e26', 'UPDATE': '2023_02_01'},
    'Stock Unite Legale': {'URL': '825f4199-cadd-486c-ac46-a65a8ea1a047', 'UPDATE': '2023_02_01'}
    })
    
    
    # -- Download and Extract each of these Data URLs --
    for stockKey in list(filter(lambda cKey : 'stock' in cKey.lower(), dictStocks.keys())):
        print(f'Current File -> {stockKey}')
        stockURL = dictStocks["CORE_URL"] + dictStocks[stockKey]["URL"]
        stockFilename = wget.download(stockURL, out=pathTMP, bar=barProgress)
        z = zipfile.ZipFile(stockFilename)
        z.extractall(pathData)
        z.close()
        os.remove(stockFilename)
        print(f'\nFile Downloaded and Extracted Successfully!\n')
    
    