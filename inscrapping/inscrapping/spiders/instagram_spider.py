import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.http import HtmlResponse
import time

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    start_urls = ['https://www.instagram.com/']

    def __init__(self, *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def parse(self, response):
        self.driver.get('https://www.instagram.com/accounts/login/')

        # Dê tempo para a página carregar
        time.sleep(5)

        # Localizar campos de login e senha
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        # Inserir suas credenciais aqui (não faça isso em código de produção!)
        username_input.send_keys('seu_usuario')
        password_input.send_keys('sua_senha')

        # Submeter o formulário
        password_input.send_keys(Keys.RETURN)

        # Dê tempo para o login acontecer
        time.sleep(5)

        # Navegar para a página inicial
        self.driver.get('https://www.instagram.com/')

        # Dê tempo para a página carregar
        time.sleep(5)

        # Extraia o conteúdo da página
        response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
        self.parse_posts(response)

    def parse_posts(self, response):
        # Exemplo simples de extração de dados de posts
        for post in response.css('article div div div div a::attr(href)').getall():
            yield {'post_url': response.urljoin(post)}

    def closed(self, reason):
        self.driver.quit()
