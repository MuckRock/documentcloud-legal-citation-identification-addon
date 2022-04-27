"""
This is a hello world add-on for DocumentCloud.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from documentcloud.addon import AddOn
from eyecite import get_citations
import csv


class LegalCitations(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""

        citations_found = []

        # add a hello note to the first page of each selected document
        if self.documents:
            for document in self.client.documents.list(id__in=self.documents):
                citation_list = get_citations(document.full_text)
                tagged_citation_list = [(document.title, document.id, citation) for citation in citation_list]
                citations_found += tagged_citation_list
        elif self.query:
            documents = self.client.documents.search(self.query)[:3]
            for document in documents:
                citation_list = get_citations(document.full_text)
                tagged_citation_list = [(document.title, document.id, citation) for citation in citation_list]
                citations_found += tagged_citation_list

        with open("citations_found.csv", "w+") as file_:
            writer = csv.writer(file_)
            writer.writerow(("title", "id", "citation"))
            writer.writerows(citations_found)
            self.upload_file(file_)

        # just for testing
        print(citations_found)

if __name__ == "__main__":
    LegalCitations().main()
