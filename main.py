from documentcloud.addon import AddOn
from eyecite import get_citations
import csv


class LegalCitations(AddOn):

    def main(self):

        citations_found = []

        # if the input parameter is specifying documents.
        if self.documents:
            # iterate through those documents.
            for document in self.client.documents.list(id__in=self.documents):
                # identify the citations in the document.
                citation_list = get_citations(document.full_text)
                tagged_citation_list = [(document.title, document.id, citation) for citation in citation_list]
                citations_found += tagged_citation_list

        # otherwise, use the query to get the documents of interest.
        elif self.query:
            # iterate through the documents in the query.
            documents = self.client.documents.search(self.query)[:3]
            for document in documents:
                # identify the citations in the document.
                citation_list = get_citations(document.full_text)
                tagged_citation_list = [(document.title, document.id, citation) for citation in citation_list]
                citations_found += tagged_citation_list

        # output the citations as a CSV.
        with open("citations_found.csv", "w+") as file_:
            writer = csv.writer(file_)
            writer.writerow(("title", "id", "citation"))
            writer.writerows(citations_found)
            self.upload_file(file_)

if __name__ == "__main__":
    LegalCitations().main()
