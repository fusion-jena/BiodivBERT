# Open Access is required for full publication crawl. check Legal aspects by the publishers.
OPENACCESS = False

Year_Range = "1990-2020"
keywords = ["biodivers*", "genetic diversity","*omic diversity", "phylogenetic diversity", "soil diversity",
            "population diversity",  "species diversity", "ecosystem diversity", "functional diversity",
            "microbial diversity"]

years = [] # [1990 - 2020]
for i in range(2020-1990+1):
    years.append(i+1990)

API = 'Springer'
# API = 'Elsevier'

Metric = True # for abstracts and dois only
Full = False # for full text crawl

