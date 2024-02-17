from FlyBaseDownloads.downloads.Downloads import Downloads 
from FlyBaseDownloads.utilities.internet import Check_internet
        
class AnnSeq():
    
    def __init__(self, main_url, cred):
        
        self.cred = cred
        self.main_url = main_url
        
    def get(self, data_type, release = "r6.55"):
        annSeq_url = str(f"{self.main_url}/dmel-all-{data_type}-{release}.fasta.gz")
        if not self.cred:
            connection_ = False
        else:
            connection_ =  Check_internet.check_internet_connection(msg=False)
        downloads = Downloads(annSeq_url, self.cred, connection_)
        
        file = downloads.get()
        
        return file
    
    def get_types(self):
        list_types = ["aligned", "CDS", "chromosome",
                      "clones", "exon", "five_prime_UTR",
                      "gene", "gene_extended2000", "intergenic", 
                      "intron", "miRNA", "miscRNA", 
                      "ncRNA", "predicted", "pseudogene",
                      "sequence_features", "synteny", 
                      "three_prime_UTR", "transcript", 
                      "translation", "transposon", "tRNA"]
        
        return list_types
