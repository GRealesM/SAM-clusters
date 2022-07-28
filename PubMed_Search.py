#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Guillermo Reales
"""
# Import required libraries
from Bio import Entrez, Medline
import pandas as pd

def getpapers(kwd, countries, lang):
    #Increase query limit to 10/s & get warnings
    Entrez.email = 'XXXX' # We used our own email
    #Get one from https://www.ncbi.nlm.nih.gov/account/settings/ page
    Entrez.api_key='XXXX' # We used our own API key
    MPD = pd.DataFrame() # Empty data frame
    
    for country in countries:
        query = kwd + country 
        handle = Entrez.esearch(db="pubmed", term=str(query), retmax="20000", sort = 'pub+date')
        record = Entrez.read(handle)
        idlist = record["IdList"]
        handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text") # See medline format table
        records = Medline.parse(handle)
        records = list(records)
        df = pd.DataFrame(records)
        if len(df) > 1:
            cleaner = df['PT'].map(lambda x: 'Review' in x)
            df = df[~cleaner]
            columnames = {"AB":"Abstract","CI":"Copyright Information","AD":"Affiliation","IRAD":"Investigator Affiliation","AID":"Article Identifier","AU":"Author","FAU":"Full Author","CN":"Corporate Author","DCOM":"Date Completed","DA":"Date Created","LR":"Date Last Revised","DEP":"Date of Electronic Publication","DP":"Date of Publication","EDAT":"Entrez Date","GS":"Gene Symbol","GN":"General Note","GR":"Grant Number","IR":"Investigator Name","FIR":"Full Investigator Name","IS":"ISSN","IP":"Issue","TA":"Journal Title Abbreviation","JT":"Journal Title","LA":"Language","LID":"Location Identifier","MID":"Manuscript Identifier","MHDA":"MeSH Date","MH":"MeSH Terms","JID":"NLM Unique ID","RF":"Number of References","OAB":"Other Abstract","OCI":"Other Copyright Information","OID":"Other ID","OT":"Other Term","OTO":"Other Term Owner","OWN":"Owner","PG":"Pagination","PS":"Personal Name as Subject","FPS":"Full Personal Name as Subject","PL":"Place of Publication","PHST":"Publication History Status","PST":"Publication Status","PT":"Publication Type","PUBM":"Publishing Model","PMC":"PubMed Central Identifier","PMID":"PubMed Unique Identifier","RN":"Registry Number/EC Number","NM":"Substance Name","SI":"Secondary Source ID","SO":"Source","SFM":"Space Flight Mission","STAT":"Status","SB":"Subset","TI":"Title","TT":"Transliterated Title","VI":"Volume","CON":"Comment on","CIN":"Comment in","EIN":"Erratum in","EFR":"Erratum for","CRI":"Corrected and Republished in","CRF":"Corrected and Republished from","PRIN":"Partial retraction in","PROF":"Partial retraction of","RPI":"Republished in","RPF":"Republished from","RIN":"Retraction in","ROF":"Retraction of","UIN":"Update in","UOF":"Update of","SPI":"Summary for patients in","ORI":"Original report in"}
    
            df = df.rename(index=str,  columns = columnames)
            df['Country'] = country
            MPD = MPD.append(df)

        else:
            print("Search didn't throw any results for: " + country)
    
    name = "ALL_COUNTRIES_" + lang + "_CELAISO.tsv"
    MPD.to_csv(str(name), sep="\t", encoding="utf-8", index=False)

# Now let's find new papers for old countries

countries=['Argentina', 'Bolivia', 'Brazil', 'Chile','Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru','South America', 'Suriname', 'Uruguay', 'Venezuela']
countries = [x.upper() for x in countries]

kwd='founder effect OR consanguineous marriages OR isolated population genetic diseases OR consanguinity marriage OR geographical cluster genetic disease OR geographic cluster genetic disease OR cluster genetic disease OR rumor AND '

getpapers(kwd, countries, 'EN')

# Now we'll search for the terms in Spanish

kwd='(tw:(efecto fundador)) OR (tw:(matrimonios consanguineos)) OR (tw:(poblaciones aisladas)) OR (tw:(población aislada)) OR (tw:(matrimonio consanguineo)) OR (tw:(enfermedad genética cluster geográfico)) OR (tw:(cluster enfermedad genética)) OR (tw:(rumor)) AND '

countries=['Argentina', 'Bolivia', 'Chile','Colombia', 'Ecuador',  'Paraguay', 'Peru', 'Uruguay', 'Venezuela'] # Remove non-Spanish speaking countries
countries = [x.upper() for x in countries]
getpapers(kwd, countries,  'ES')
