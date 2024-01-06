import os
import requests
from bs4 import BeautifulSoup

def parse_xml_webpages(ids, legislatura):
    """
    Parses XML webpages and extracts the text of the given IDs.

    Args:
        ids: A list of IDs of the people whose text to extract.
        legislatura: The legislature to extract data from.

    Returns:
        None
    """

    # Create folders for each ID.
    for id in ids:
        folder_name = str(id)
        os.makedirs(folder_name, exist_ok=True)

    # Iterate over the pages of XML data.
    for page_number in range(1, 2000):
        print('Sessione ' + str(page_number) + ', Legislatura ' + str(legislatura))
        # Get the URL for the current page.
        url = f'http://documenti.camera.it/apps/resoconto/getXmlStenografico.aspx?idNumero={str(page_number).zfill(4)}&idLegislatura={str(legislatura)}'

        # Get the contents of the current page.
        response = requests.get(url)

        # Check if the page contains the error message.
        if 'The remote server returned an error: (404) Not Found.' in response.text:
            break

        soup = BeautifulSoup(response.content, 'xml')

        # Find all of the testoXHTML elements on the current page.
        testoXHTML_elements = soup.find_all('testoXHTML')

        # Check each testoXHTML element with the id filter.
        for testo in testoXHTML_elements:
            # Find the 'nominativo' tag within the current testoXHTML element.
            nominativo = testo.find('nominativo')

            if nominativo and nominativo.get('cognomeNome') in ids:
                id = nominativo.get('cognomeNome')
                folder_name = str(id)
                filename = f'{folder_name}/{str(legislatura)}-{str(page_number).zfill(4)}.txt'

                '''
                # Alternative approach that can be used to remove nominativo
                
                for child in testo.find('nominativo').descendants:
                    if child.string:
                        child.string = ''
                '''

                with open(filename, 'a', encoding='utf-8') as file:

                    # Write the text of the testoXHTML element to the file.\

                    text_without_nominativo = ''.join(testo.find_all(text=True, recursive=False)).strip()
                    text_without_presidente = text_without_nominativo.replace('Presidente del Consiglio di ministri. ', '')
                    file.write(text_without_presidente)

                    # Find all subsequent interventoVirtuale elements until a non-matching testoXHTML element.
                    intervento_elements = testo.find_all_next('interventoVirtuale')
                    for intervento in intervento_elements:
                        testo_sibling = intervento.find_previous_sibling('testoXHTML')
                        if testo_sibling and testo_sibling.find('nominativo', {'cognomeNome': id}):
                            file.write(intervento.get_text())
                        else:
                            break
            else:
                # If the current testoXHTML element doesn't match the ID, continue to the next iteration.
                continue


# Example usage
legislatura = [17, 18, 19]
ids = ['MELONI Giorgia', 'DRAGHI Mario', 'CONTE Giuseppe', 'RENZI Matteo', 'LETTA Enrico', 'GENTILONI SILVERI Paolo']
for xx in legislatura:
    parse_xml_webpages(ids, xx)
