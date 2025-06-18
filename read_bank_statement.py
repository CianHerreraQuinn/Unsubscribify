import sys
import subprocess

def install_and_import(package, import_name=None):
    import importlib
    try:
        return importlib.import_module(import_name or package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return importlib.import_module(import_name or package)

# Automatically install/import required libraries
pdfplumber = install_and_import('pdfplumber')
pandas = install_and_import('pandas')
re = install_and_import('re')
dateutil = install_and_import('python-dateutil', 'dateutil')
parser = dateutil.parser

# 2. Extract transaction data (date, description, amount)
def extract_transactions(pdf_path):
    transactions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                import re
                match = re.match(r"(\\d{2}/\\d{2}/\\d{4})\\s+(.+?)\\s+(-?\\d+\\.\\d{2})", line)
                if match:
                    date, desc, amount = match.groups()
                    transactions.append({
                        'date': parser.parse(date),
                        'description': desc.strip(),
                        'amount': float(amount)
                    })
    return pandas.DataFrame(transactions)

def identify_subscriptions(df):
    df['month'] = df['date'].dt.to_period('M')
    recurring = df.groupby('description').filter(lambda x: x['month'].nunique() > 1)
    return recurring

# Usage Example:
# df = extract_transactions('statement.pdf')
# subscriptions = identify_subscriptions(df)
# print(subscriptions)
