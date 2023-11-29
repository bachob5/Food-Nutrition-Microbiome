# Food-Nutrition-Microbiome
This project makes part of the first implementation study related to Food&Nutrition comunity (https://elixir-europe.org/communities/food-and-nutrition) in ELIXIR Europe infrastructure and the National Italian project ELIXIRxNextGenIT: Consolidation of the Italian Infrastructure for Omics and Bioinformatics (https://elixir-italy.org/elixir-x-nextgenerationit-consolidation-of-the-italian-infrastructure-for-omics-data-and-bioinformatics/).

The present repository aims at providing an automated retrieval routine to use public human microbiome datasets related to diet observation and intervention studies. 

The first data source used here to find human microbiome data is Mgnify (https://www.ebi.ac.uk/metagenomics). 
The availability of an Application Programming Interface (API) in Mgnify allows to set up a routine data retrieval to keep the repository up to date. 
The API of Magnify was exploited to create a general purpose python retrieval script able to fetch all human related data using specific libraries such as 'requests' and 'pandas'.
the retrieved data is available for further local parsing to flag only the diet-related studies using text and data mining techniques fed by ontology terms (e.g. ONS: https://www.ebi.ac.uk/ols4/ontologies/ons) 
and relational terms present in PhenotypeDB (https://dashin.eu/interventionstudies/).

According to the results obtained from the text mining routine, the repository will be regularly updated with the newly obtained results.

To make use of the scripts of this repository, it is required to install python 3 with the following libraries: requests, pandas, collections.

To obtain all the human microbiome studies present in mgnify resource simply run the following code:

	python Mgnify_Query.py

The script yield the following output file 'Mgnify_HumanAssociatedBiomes.csv' containing all the available human microbiome data summed to 859 studies (updated on November 15, 2023).

The abstracts of retrieved studies were then searched using pre-defined terms relevant to dietary related experiments as follows:

	python searchMgnifyAbstracts.py Mgnify_HumanAssociatedBiomes.csv 

Accordingly, the file 'Mgnify_HumanAssociatedBiomes_DietSelectedStudies.csv' was produced including 10 studies annotated as relevant for the searched terms.

Analyses results available for each Food and Nutrition study can be retrieved and explored using the following code, which provides the links to the results for each study. The output is named starting by the studyID (e.g. MGYS00000526_RelatedResults.csv). All outputs relevant to this project are provided in the RelatedResults branch.

	python getRelatedStudyResults.py Mgnify_HumanAssociatedBiomes_DietSelectedStudies.csv 
