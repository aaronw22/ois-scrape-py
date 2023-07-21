from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Navigate to the URL
url = 'https://www.asx.com.au/markets/trade-our-derivatives-market/derivatives-market-prices/short-term-derivatives'
driver.get(url)

# Extract the page source
pg_source = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(pg_source, 'html.parser')

# Find the table containing the data
table = soup.find('table')

# Read the table data into a pandas DataFrame
cr_futures = pd.read_html(str(table))[0]

# Rename columns
cr_futures.columns = ['Expiry Date', 'Previous Settlement', 'Previous Settlement Time']
cr_futures.columns = ['date', 'cash_rate', 'scrape_date']

# Data cleaning and transformation
cr_futures['cash_rate'] = cr_futures['cash_rate'].str.replace('^(.*)As of \\d+/\\d+/\\d+', '\\1').str.strip()
cr_futures['scrape_date'] = cr_futures['scrape_date'].str.extract(r'As of (\d+/\d+/\d+)')[0]
cr_futures['date'] = pd.to_datetime('01 ' + cr_futures['date'], format='%d %b %y')
cr_futures['scrape_date'] = pd.to_datetime(cr_futures['scrape_date'], format='%d/%m/%y')
cr_futures['cash_rate'] = 100 - pd.to_numeric(cr_futures['cash_rate'])

print(cr_futures)
