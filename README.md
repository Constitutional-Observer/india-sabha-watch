# India Sabha Watch

This repository is meant to track discussions at the many levels of parliaments in India. 

Namely: The LokSabha, RajyaSabha and the State Legislative Assemblies.

Current Status: The repository currently hosts Lok Sabha records

## Lok Sabha

The Lok Sabha has many forms of discussions. 

### Notes

1. Largely 3 categories of documentation are published by the Lok Sabha:
    1. Question Hour Q&A
    2. Debates
    3. Full day's proceedings
2. Full Day proceedings are published in 3 different language forms:
    1. Original (Hindi, English and regional language translated to English as used by the MPs)
    2. Translated to Hindi
    3. Translated to English
3. These are available with varying levels of completeness:
    1. Debates are available till the 17th LS. 18th (current) LS is available through the sansad.in API 
    2. Q&A are available till the ?


# short notes

## old api
was downloading meta tables and created a list of fall meta pages to get the main file list. 

## new api

### full day proceedings, session dates
https://sansad.in/api_ls/business/AllLoksabhaAndSessionDates

https://sansad.in/api_ls/debate/text-of-debate?loksabha=17&sessionNo=XV&debateDate=1/31/2024&locale=en

### Debates 
list: https://sansad.in/api_ls/debate/debate-search?loksabha=17&sessionNumber=&mpCode=&debateTypeId=&searchKeyword=&fromDate=&toDate=&debateKeyword=&page=1&size=10\
note:
    1. Appears to only list from LS 17
note: 
    1. Appears to only contain from LS 13, text seems to be available as text and not as pdf
contents: https://sansad.in/api_ls/debate/debate-details?loksabha=14&sessionNumber=15&dbSlNo=11213