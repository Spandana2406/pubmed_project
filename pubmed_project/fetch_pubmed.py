import requests
import xml.etree.ElementTree as ET

# Define search query
query = input("Enter PubMed search query: ")

# Fetch papers from PubMed API
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    "db": "pubmed",
    "term": query,
    "retmode": "xml",
    "retmax": "10"  # Fetching only 10 papers for testing
}

response = requests.get(base_url, params=params)
root = ET.fromstring(response.content)

# Extract PubMed IDs
pmids = [id_elem.text for id_elem in root.findall(".//Id")]
print(f"Total papers retrieved: {len(pmids)}")

if not pmids:
    print("No papers found.")
    exit()

# Fetch details for each paper
details_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
details_params = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "retmode": "xml"
}

details_response = requests.get(details_url, params=details_params)
details_root = ET.fromstring(details_response.content)

# Define keywords to identify non-academic authors
pharma_keywords = ["Inc", "Ltd", "Biotech", "Pharmaceutical", "Corporation", "GmbH", "LLC"]

# Process and filter papers
filtered_papers = []

for doc in details_root.findall(".//DocSum"):
    title = doc.find(".//Item[@Name='Title']").text if doc.find(".//Item[@Name='Title']") is not None else "Unknown"
    authors = [author.text for author in doc.findall(".//Item[@Name='AuthorList']/Item") if author.text]
    affiliations = [aff.text for aff in doc.findall(".//Item[@Name='Affiliation']") if aff.text]

    print(f"\nTitle: {title}")
    print(f"Authors: {authors}")
    print(f"Affiliations: {affiliations}")

    # Check for non-academic authors
    if any(any(keyword in aff for keyword in pharma_keywords) for aff in affiliations):
        print("✔ Non-academic author found!")
        filtered_papers.append((title, authors, affiliations))
    else:
        print("✘ No non-academic author.")

# Output results
if filtered_papers:
    print("\nFiltered Papers with Non-Academic Authors:")
    for paper in filtered_papers:
        print(f"Title: {paper[0]}")
else:
    print("\nNo papers found with non-academic authors.")
