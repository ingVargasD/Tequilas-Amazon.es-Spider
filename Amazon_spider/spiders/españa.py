import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import AmazonesItem
from scrapy.loader import ItemLoader


class EspañaSpider(CrawlSpider):
    name = 'españa'
    allowed_domains = ['www.amazon.es']
    start_urls = ['https://www.amazon.es/s?k=tequilas&i=grocery&rh=n%3A6198072031%2Cn%3A6347711031%2Cn%3A6347720031%2Cn%3A6347786031&dc&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1608298128&rnid=6198072031&ref=sr_nr_n_1']



    rules = (
        Rule(LinkExtractor(restrict_xpaths="//li[@class='a-last']"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-4']//a[@class='a-link-normal a-text-normal']"), callback='parse_item', follow=True),
    )




    def vol(self, lista):

        a=" ".join(lista)
        d=a.replace("\n", "")
        b= d.split(" ")
        try:
            c= b.index("ml")
            cantidad=b[c-1]
        except:
            cantidad="no se pudo definir con el programa"

        return cantidad
    def vol2(self,texto):
        #a=" ".join(lista)
        a=texto.split(" ")
        b=a[-2]+a[-1]
        try:
            b=b.replace("|","")
        except:
            b=b
        if len(b)>6:
            b="no se pudo definir con el programa"
        else:
            b=b
        return b


    def estado(self, texto):

        b = texto.split(" ")

        for i in b:
            if i == "Añejo" or i == "AÑEJO" or i == "añejo":
                clase = "Añejo"
                break
            elif i == "Blanco" or i == "blanco" or i == "BlANCO":
                clase = "Blanco"
                break

            elif i == "Plata" or i == "PLATA" or i == "plata":
                clase = "Plata"
                break

            elif i == "Reposado" or i == "REPOSADO" or i == "reposado":
                clase = "Reposado"
                break
            elif i == "Joven" or i == "JOVEN" or i == "joven":
                clase = "joven"
                break
            elif i == "Oro" or i == "ORO" or i == "oro":
                clase = "Oro"
                break
            elif i == "Cristalino" or i == "cristalino" or i == "CRISTALINO":
                clase = "Cristalino"
                break
            elif i == "Extra Añejo":
                clase = "Extra Añejo"
                break
            else:
                clase = "El titulo no indica la clase del tequila"
        return clase


    def parse_item(self, response):

        
        loader = ItemLoader(AmazonesItem(), response)

        link = response.xpath(
            "//div[@id='imgTagWrapperId']/img/@data-old-hires").get()

        loader.add_value("image_urls", link)

        nombre = (response.xpath("//span[@id='productTitle']/text()").get()).strip()
        price = response.xpath(
            "//span[@id='priceblock_ourprice']/text()").get()
        clase = response.xpath(
            "//span[text()='Ingredientes']/../../td[2]/span/text()").get()
        volumen=response.xpath("//table[@id='productDetails_techSpec_section_1']//td[@class='a-size-base']/text()").getall()

        links=response.request.url 

     

        loader.add_value("name", nombre)
        loader.add_value("price", price)
        loader.add_value("clase", self.estado(nombre))
        loader.add_value("volumen_mL",self.vol2(nombre))
        loader.add_value("links",links)
        



        yield loader.load_item()
