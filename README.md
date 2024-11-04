# Food-Nutrition-Microbiome
This project makes part of the first implementation study related to Food&Nutrition comunity (https://elixir-europe.org/communities/food-and-nutrition) in ELIXIR Europe infrastructure and the National Italian project ELIXIRxNextGenIT: Consolidation of the Italian Infrastructure for Omics and Bioinformatics (https://elixir-italy.org/elixir-x-nextgenerationit-consolidation-of-the-italian-infrastructure-for-omics-data-and-bioinformatics/).

The present repository aims at providing an automated retrieval routine to use public human microbiome datasets related to diet observation and intervention studies. This makes part of data FAIRness characteristics verification for potential use in automated bioinformatics pipelines and data alignments efforts across different data sources.

The first data source used here to find human microbiome data is Mgnify (https://www.ebi.ac.uk/metagenomics). 
The availability of an Application Programming Interface (API) in Mgnify allows to set up a routine data retrieval to keep the repository up to date. 
The API of Magnify was exploited to create a general purpose python retrieval script able to fetch all human related data using specific libraries such as 'requests' and 'pandas'.
the retrieved data is available for further local parsing to flag only the diet-related studies using text and data mining techniques fed by ontology terms (e.g. ONS: https://www.ebi.ac.uk/ols4/ontologies/ons) 
and relational terms present in PhenotypeDB (https://dashin.eu/interventionstudies/).

Additional data sources were considered essential during the execution of this study, namely MG-RAST (Metagenomics Analysis Server: https://www.mg-rast.org/) and JGI (Joint Genome Institute: https://genome.jgi.doe.gov/portal/), as they offer an important and curated set of human microbiome data. As done with Mgnify these databases were explored for human-associated microbiome data using their specific APIs. The related data were retrieved and filtered for diet-related studies using ad-hoc python scripts documented below. 

According to the results obtained from the text mining routine, this repository will be regularly updated with the newly obtained results. Some terms used for text mining purposes were enriched also from manual mining of projects and studies descriptions and abstracts.

To make use of the scripts of this repository, it is required to install python 3 with the following libraries: requests, pandas, collections, pathlib, itertools, json, tqdm, urllib3.

To reduce the space usage, here we included only example files. However, all scripts are fully functional and they can be run locally to get the complete results.

In the following, a step by step guide to retrieve and parse the data from the above mentioned databases is provided:

# Mgnify: data retrieval and analysis

To obtain all the human microbiome studies present in mgnify resource simply run the following code:

	python Mgnify_Query.py

The script yield the following output file 'Mgnify_HumanAssociatedBiomes.csv' containing all the available human microbiome data summed to 882 studies (updated on November 04, 2024).

The abstracts of retrieved studies were then searched using pre-defined terms relevant to dietary related experiments as follows:

	python searchMgnifyAbstracts.py Mgnify_HumanAssociatedBiomes.csv

Accordingly, the file 'Mgnify_HumanAssociatedBiomes_DietSelectedStudies.csv' was produced including 148 studies annotated as relevant for the searched terms.

Analyses results available for each Food and Nutrition study can be retrieved and explored using the following code, which provides the links to the results for each study. The output is named starting by the studyID (e.g. MGYS00000526_RelatedResults.csv). All outputs relevant to this project are provided in the RelatedResults branch.

	python getRelatedStudyResults.py Mgnify_HumanAssociatedBiomes_DietSelectedStudies.csv 

# MG-RAST (Metagenomics Analysis Server): data retrieval and analysis

The following script includes aggregated functions of bulk download of selected biomes ("human-associated habitat", "organism-associated habitat", "gut" "feces", "food") as well as the retrieval of available related pubmed abstracts.

	python mg-rast.py 

The script returned 12404 entries corresponding to 299 studies of which 281 studies were tagged as Mixs compliant. Here we called the output "table-mgrast_tabDelimited.txt".

To search the studies' descriptions and abstracts for relevant diet related terms the following script can be executed taking the complete table retrieved in the previous step as input.

	python searchMGRAST_Abstracts.py table-mgrast_tabDelimited.txt

The above script yielded 124 studies relevant to human nutrition. However a careful manual curation of the results revealed that some entries with the same description and study title have different study ID. These entries were aggregated and considered as belonging to the same study. Consequently, the total number of diet-related microbiome studies was reduced to 70. 


# JGI (Joint Genome Institute): data exploration not fully open source

Although JGI Graphical User Interface is very informative on the database content its API has an important limiting factor falling out of FAIR principles. To perform queries and subsequent data retrieval from JGI using the API it is mandatory to have a valid registration with ORCID to obtain a TOKEN which is used to construct the API call. In this repository we provide an example of data retrieval from JGI as a bash script, which should be compiled with an "Offline TOKEN" and run subsequently.

After filling up the required information, it is possible to run the following script using a bash shell.

./jgi-request-example.sh 

According to our local analysis in October 2024, a total of 284 human-associated studies were retrieved from JGI of which only 10 were related to microbiome-diet.


# Disclaimer

The results obtained from the above three databases, their FAIRness level and the data characteristics will be drafted for scientific publication and made available here. 

