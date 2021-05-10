from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # ## Scrape Mars News Site


    # target URL
    url = "https://redplanetscience.com/"
    browser.visit(url)



    html = browser.html
    soup = bs(html,'html.parser')



    print(soup.body.prettify())
    # results = soup.find_all('div', class_='content_title')
    # results



    # Latest news title
    data = soup.find_all('div', class_='list_text')
    title = data[0].find('div', class_="content_title").get_text()
    title



    # Paragraph from latest news title
    para = data[0].find('div', class_="article_teaser_body").get_text()
    para


    # ## Mars pictures


    url2 = "https://spaceimages-mars.com"
    browser.visit(url2)



    # html2 = browser.html
    # soup2 = bs(html2,'html.parser')
    # print(soup2.body.prettify())



    # button = soup2.find_all('button', class_="btn btn-outline-light")[0]
    button = browser.find_by_tag('button')[1]
    button.click()



    # Get image url
    html2 = browser.html
    soup2 = bs(html2,'html.parser')
    # print(soup2.body.prettify())
    featured_image_url = soup2.find('img', class_='fancybox-image').get('src')
    featured_image_url



    full_url = url2 + '/' + featured_image_url
    full_url


    # ## Pandas scraping


    # create table
    url3 = "https://galaxyfacts-mars.com"
    df = pd.read_html(url3)[0]
    df.columns = ['Description','Mars',"Earth"]



    # Set index
    df.set_index('Description', inplace=True)
    df



    df = df.to_html()
    print(df)


    # ## Mars Hemispheres


    url4 = "https://marshemispheres.com/"
    browser.visit(url4)
    html = browser.html
    soup = bs(html,'html.parser')
    print(soup)



    # Find image URL
    image_url = soup.find_all('a', class_="itemLink product-item")
    image_url



    #spearate url
    page_url = []

    for x in image_url:
        if (x["href"] != "#"):
            current_url = url4 + x["href"]
            if current_url not in page_url:
                page_url.append(current_url)
                
    page_url



    title_and_img_url = []

    for x in page_url:
        browser.visit(x)
        html = browser.html
        soup = bs(html, 'html.parser')
        title_hemis = soup.find_all("h2", class_="title")[0].text.split()
        title_hemis.pop()
        title_hemis = " ".join(title_hemis)
        image_url = url4 + soup.find_all('img', class_="wide-image")[0]["src"]
        loop_dict = {"title": title_hemis, "img_url": image_url}
        title_and_img_url.append(loop_dict)
        
    title_and_img_url


    # Store scraped info in a dictionary
    all_info = {
        "title": title,
        "para": para,
        "full_url": full_url,
        "df": df,
        "mars_title_and_img_url": title_and_img_url
    }


    browser.quit()
    print (f"{all_info}")



