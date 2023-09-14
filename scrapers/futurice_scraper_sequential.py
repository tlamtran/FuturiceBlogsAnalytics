import requests
import pandas as pd
from bs4 import BeautifulSoup

class ModifiedFuturiceScraper():        
    def scrape(self, a):
        self.soup = a
        
        object_grid_item = {
            'link': self.__extract_link(),
            'title': self.__extract_title(),
            'date': self.__extract_date(),
            'category': self.__extract_category(),
            'grid paragraph': self.__extract_grid_item_paragraph()
        }

        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.text, 'html.parser')


        object_blog_content = {
            'content': self.__extract_content_sequentially()
        }


        object = object_grid_item | object_blog_content

        return object

    def __extract_content_sequentially(self):
        content = []
        for element in self.soup.find_all(['h2', 'h3', 'h4', 'p', 'li']):
            elClass = element.get('class', [])
            
            if element.name == 'h2' and "typography_heading__lg__WBfN2 primaryContent_content__title__w19Zq" not in elClass:
                continue

            elif element.name == 'h3' and "typography_heading__md__fDSFm" not in elClass:
                continue

            elif element.name == 'h4' and "typography_heading__sm__YtNGG" not in elClass:
                continue
            
            elif element.name == 'p' and any(c in elClass for c in ["typography_body__4D3BM", "linkGridItem_item__teaser__FDVWQ"]):
                continue

            elif element.name == 'li':

                if any(not_bullet in elClass
                    for not_bullet in ["menu_menu__item__RBocN", "footer_footer__menu_link__EKNZs",
                                          "contactList_contact_list__list_item__6DWnj", "linkGridItem_item__wrapper__1LczZ"]):
                    continue

                elif element.find('span', {"class": "menu_submenu__link_label__uFi7u"}):
                    continue


            text = element.get_text()
            text = text.replace('\n', ' ')
            text = text.strip()
            content.append(text)
        continuous_text = ' '.join(content)
        return continuous_text

    def __extract_link(self):
        self.url = "https://futurice.com" + self.soup.get('href')
        return self.url

    def __extract_title(self):
        title = self.soup.find("h3", {"class":"typography_heading__sm__YtNGG linkGridItem_link_item__title__rqhTZ"}).get_text()
        return title

    def __extract_date(self):
        date = self.soup.find('time', {"class":"metadata_meta__date__XQoMb"}).get_text()
        return date

    def __extract_category(self):
        category = self.soup.find('span', {"class":"metadata_meta__category__dXABR"}).get_text()
        return category


    def __extract_grid_item_paragraph(self):
        paragraphs = self.soup.find('p', {"class":"typography_body__4D3BM linkGridItem_item__teaser__FDVWQ"}).get_text()
        return paragraphs




if __name__ == "__main__":
    scraper = ModifiedFuturiceScraper()

    objects = []

    for i in range(1, 16, 1):
        print("page: " + str(i))
        base_url = f"https://futurice.com/blog?page={i}"
        page = requests.get(base_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for a in soup.find_all('a', {"class": "linkGridItem_item__link__YZtcF"}):
            object = scraper.scrape(a)
            objects.append(object)

    df = pd.DataFrame(data=objects)
    df.to_csv('data/raw/futurice/blogs_seq.csv', index=False)
    



    

    