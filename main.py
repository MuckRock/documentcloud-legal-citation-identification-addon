""" Requires eyecite to find legal citations """
import csv
from documentcloud.addon import AddOn
from eyecite import get_citations


class LegalCitations(AddOn):
    """ DocumentCloud Add-On that uses eyecite to find legal citations in a document """
    def main(self):
        """ Loops through each page on each document """
        citations_found = []

        for document in self.get_documents():
            for page_number in range(1, document.page_count + 1):
                page_text = document.get_page_text(page_number)
                citation_list = get_citations(page_text)
                tagged_citation_list = [
                    (document.title, document.id, page_number, citation)
                    for citation in citation_list
                ]
                citations_found += tagged_citation_list

        # output the citations as a CSV.
        with open("citations_found.csv", "w+", encoding="utf-8") as file_:
            writer = csv.writer(file_)
            writer.writerow(("title", "id", "page number", "citation"))
            writer.writerows(citations_found)
            self.upload_file(file_)


if __name__ == "__main__":
    LegalCitations().main()
