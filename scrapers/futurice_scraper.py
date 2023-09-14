import requests
import pandas as pd
from bs4 import BeautifulSoup

class FuturiceScraper():        
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
            'headings': self.__extract_headings(),
            'content paragraph': self.__extract_content_paragraph(),
            'bullets': self.__extract_bullet_points()
        }

        object = object_grid_item | object_blog_content

        return object


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

    def __extract_headings(self):
        big_headings = [x.get_text() for x in self.soup.find_all("h2", {"class":"typography_heading__lg__WBfN2 primaryContent_content__title__w19Zq"})]
        small_headings = [x.get_text() for x in self.soup.find_all("h3", {"class": "typography_heading__md__fDSFm"})]
        even_smaller_headings = [x.get_text() for x in self.soup.find_all("h4", {"class": "typography_heading__sm__YtNGG"})]
        headings = big_headings + small_headings + even_smaller_headings
        return headings

    def __extract_content_paragraph(self):
        paragraphs =  self.soup.find_all('p')
        not_paragraphs = self.soup.find_all('p', {"class":"typography_body__4D3BM linkGridItem_item__teaser__FDVWQ"})
        paragraphs = [x.get_text() for x in paragraphs if x not in not_paragraphs]
        return paragraphs

    def __extract_grid_item_paragraph(self):
        paragraphs = self.soup.find('p', {"class":"typography_body__4D3BM linkGridItem_item__teaser__FDVWQ"}).get_text()
        return paragraphs

    def __extract_bullet_points(self):
        bullets = [x.get_text() for x in self.soup.find_all('li')]
        not_bullet1 = [x.get_text() for x in self.soup.find_all('li', {"class":"menu_menu__item__RBocN"})]
        not_bullet2 = [x.get_text() for x in  self.soup.find_all('li', {"class":"footer_footer__menu_link__EKNZs"})]
        not_bullet3 = [x.get_text() for x in self.soup.find_all('span', {"class":"menu_submenu__link_label__uFi7u"})]
        not_bullet4 = [x.get_text() for x in self.soup.find_all('li', {"class":"contactList_contact_list__list_item__6DWnj"})]
        not_bullet5 = [x.get_text() for x in self.soup.find_all('li', {"class":"linkGridItem_item__wrapper__1LczZ"})]

        bullets = [
            x for x in bullets if (x not in not_bullet1) and 
            (x not in not_bullet2) and (x not in not_bullet3) 
            and (x not in not_bullet4) and (x not in not_bullet5)
        ]

        return bullets


if __name__ == "__main__":
    scraper = FuturiceScraper()

    objects = []

    for i in range(1, 16, 1):
        base_url = f"https://futurice.com/blog?page={i}"
        page = requests.get(base_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        for a in soup.find_all('a', {"class": "linkGridItem_item__link__YZtcF"}):
            object = scraper.scrape(a)
            objects.append(object)

    df = pd.DataFrame(data=objects)
    df.to_csv('data/raw/futurice/blogs.csv', index=False)
    



    

    