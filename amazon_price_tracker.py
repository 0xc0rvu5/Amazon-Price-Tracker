import requests, os, smtplib, lxml
from bs4 import BeautifulSoup


#initialize global variables
EMAIL = os.getenv('SMTP_USER')
PW = os.getenv('SMTP_PASS')
URL = 'https://www.amazon.com/dp/B08T9H18TJ?tag=camelproducts-20&linkCode=ogi&th=1&psc=1&language=en_US'
AMOUNT = 600
SEND_TO = 'corvus@0xc0rvu5.com'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/84.0.4147.105 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.5",
}


def price_is_right():
    '''Query user to use pre-configured variables or to input their own, initialize relevant request, create bs4 class and obtain relevant data. If conditions met send email to specified email address.'''
    os.system('clear')
    choice = input(f'~ SMTP Credentials ~\nEmail: {EMAIL}\nPassword: {PW}\n~ Product Details ~\nProduct: {URL}\nAmount: ${AMOUNT}\nSend to: {SEND_TO}\nUse the pre-configured variables? "y"\n ~ ').lower()
    if choice == 'y':
        email = EMAIL
        pw = PW
        url = URL
        amount = AMOUNT
        send_to = SEND_TO
    else:
        email = input('Email:\n ~ ')
        pw = input('Password:\n ~ ')
        url = input('URL:\n ~ ')
        amount = input('Amount:\n $ ')
        send_to = input('Send to:\n ~ ')

    #intial request and BeautifulSoup class created to access the relevant data.
    response = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "lxml")

    #scrape relevant data from site.
    text = soup.find(name='span', class_='a-price-whole')
    decimal = soup.find(name='span', class_='a-price-fraction')
    text2 = soup.find(name='span', id='productTitle')
    #convert price to float and convert the product name to a binary string to send in email. it will not send otherwise.
    total = f'{text.text}{decimal.text}'
    price = float(total)
    product = text2.text.strip()
    encoded = product.encode('ascii', 'ignore')

    #if below specified price then send email
    if price < float(amount):
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
                        connection.starttls()
                        connection.login(user=email, password=pw)
                        connection.sendmail(
                            from_addr=email,
                            to_addrs=send_to,
                            msg=f'Subject: Price alert!\n\n{encoded}\nis now ${price}!')


#initialize price_is_right() function and inform when complete.
try:
    price_is_right()
    print('Done')

except KeyboardInterrupt:
    print('\nSee you later.')