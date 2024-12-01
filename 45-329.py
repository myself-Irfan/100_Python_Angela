import logging
from bs4 import BeautifulSoup


def read_html(file_name: str) -> str:
    with open(file_name) as html_f:
        content = html_f.read()

    return content

def main():
    content = read_html('43-319/index.html')

    soup = BeautifulSoup(content, 'html.parser')

    # logging.info(soup.title)
    # logging.info(soup.title.string)
    #
    # logging.info(soup.find('h2'))
    #
    # # logging.info(soup.prettify())
    #
    # all_p = soup.find_all(name='p')
    # p_txt = [p.getText() for p in all_p]
    #
    # logging.info(p_txt)

    logging.info(soup.find(class_='external'))

    al_ext = soup.find_all(class_='external')

    ext_txt = [ext.getText() for ext in al_ext]
    logging.info(ext_txt)

    logging.info(soup.select_one(selector="p[draggable='False']"))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s -> %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    main()