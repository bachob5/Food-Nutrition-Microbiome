#!/usr/bin/bash

# API Information and examples available at
# https://gold-ws.jgi.doe.gov/

# Requirements, summary:
# 1. ORCID is necessary to access the API at the above link
# 2. Once logged in, you need to request an *offline token*
# 3. Open a session using the *offline token* which gives a *access token*

# Copy the string given as *offline token* in this variable, instead of *XXXXX*
# to avoid problem I suggest to use single or double quotes around the token
# It expires if unused in 365 days
OFFLINE_TOKEN=XXXXX

# This is used to access data, valid for 12 hours. Technically it's a *bearer token* that
# is commonly used for authentication in similar APIs
ACCESS_TOKEN=$(curl https://gold-ws.jgi.doe.gov/exchange?offlineToken=$OFFLINE_TOKEN)

# Subsequent calls use a similar system, in general there are multiple types of requests
# that is possible to see at the following url:
# https://gold-ws.jgi.doe.gov/swagger-ui/index.html
# The following call request in JSON format the organisms present in project Gp0451293
curl https://gold-ws.jgi.doe.gov/api/v1/organisms?projectGoldId=Gp0451293 -H "Accept: application/json" -H "Authorization: Bearer $ACCESS_TOKEN"

# I it possible to get more information, including PUBMED IDs if present with the following
curl -X 'GET' \                                                                                                      
        'https://gold-ws.jgi.doe.gov/api/v1/analysis_projects?projectGoldId=Gp0451293' \
        -H 'accept: */*' -H "Authorization: Bearer $ACCESS_TOKEN"
