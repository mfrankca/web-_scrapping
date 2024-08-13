# importing libraries
from bs4 import BeautifulSoup
import requests

def main(URL):
    # opening our output file in append mode
    File = open("out.csv", "a")

    # specifying user agent, You can use other user agents
    # available on the internet

    # Making the HTTP Request
    webpage = requests.get(URL)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # retrieving product title
    try:
        # Outer Tag Object
        title = soup.find("span", 
                          attrs={"id": 'productTitle'})

        # Inner NavigableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip().replace(',', '')

    except AttributeError:
        title_string = "NA"
    print("product Title = ", title_string)

    # saving the title in the file
    File.write(f"{title_string},")

    # retrieving price
    try:
        price = soup.find(
            "span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')
        # we are omitting unnecessary spaces
        # and commas form our string
    except AttributeError:
        price = "NA"
    print("Products price = ", price)

    # saving
    File.write(f"{price},")

    # retrieving product rating
    try:
        rating = soup.find("i", attrs={
                           'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')

    except AttributeError:

        try:
            rating = soup.find(
                "span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
        except:
            rating = "NA"
    print("Overall rating = ", rating)

    File.write(f"{rating},")

    try:
        review_count = soup.find(
            "span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '')

    except AttributeError:
        review_count = "NA"
    print("Total reviews = ", review_count)
    File.write(f"{review_count},")

    # print availablility status
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip().replace(',', '')

    except AttributeError:
        available = "NA"
    print("Availability = ", available)

    # saving the availability and closing the line
    File.write(f"{available},\n")

    # closing the file
    File.close()


if __name__ == '__main__':
  # opening our url file to access URLs
    ###file = open("url.txt", "r")

    # iterating over the urls
    ###for links in file.readlines():
    links=    url='https://www.amazon.ca/Stylish-Non-prescription-Eyeglasses-Eyeglass-Gradient/dp/B07PY8MQ5M/ref=sr_1_1?crid=3U06ACJEVNQL8&dib=eyJ2IjoiMSJ9.0DPMaxiy5RHMOAe3jYgiNjx2U_l2vejKryfnIhJP_Oe42X7-Ap5be7C2T_71pY-smlLrwMiMkaYU4Ar_4U-1pFMpnwohhSYc44lJCOEjtkPk4zs0eruAY0F65uuVuX_wB6wXFuJwj1Uu0lgjbnmsbxqDCsV94Mpsak6y6j6FL9qPTZ-jO9nlkaqOvZNnvxI16nZcrWAwVyGGq0Vv4jG2sxLA8J6sH2dEAxOPJrky_qxKMjz-wsNpJUo1oN-7ifGgdPD9SeHwfrcwXQA6XpUf1ZsTv5BF1l3rbkzzJr8Ict4.lmcMBgfroCnMyvnQA1bMm6vmzd3t_PEzmPYOxZFUNOk&dib_tag=se&keywords=Fendi+Eyeglasses&qid=1723517219&sprefix=fendi+eyeglasses%2Caps%2C64&sr=8-1'  # Replace with the product URL
    main(links)