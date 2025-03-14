from Bio import Entrez

def fetch_pubmed_articles(query, max_results=10):
    Entrez.email = "chimutaspandana@gmail.com"  # Replace with your email
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    article_ids = record["IdList"]
    return article_ids

# Example usage
if __name__ == "__main__":
    query = "cancer treatment"
    articles = fetch_pubmed_articles(query)
    print("PubMed Article IDs:", articles)
 
