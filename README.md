# Food-Nutrition-Microbiome
This project makes part of the first implementation study related to Food&Nutrition comunity (https://elixir-europe.org/communities/food-and-nutrition) in ELIXIR infrastructure. 
It aims at automating the retrieval and the use of public human microbiome datasets related to diet observation and intervention studies. 

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
