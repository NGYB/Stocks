# Stock recommendation using AutoGen

To run the app, follow the instructions below. Make sure you are in the root directory of this repo.
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

To run group chat:
```
python stock_recommendation_group.py
```

To run nested chat:
```
python stock_recommendation_nested.py
```

To change the input data, change the filename in the code below:
```
# Function to read CSV file and prepare data for aggregation
def read_csv_file():
    print("Reading CSV file...")
    df = pd.read_csv("./data/Stocks-data - AT&T.csv") # change to your filename here
    return df.to_dict()
```

To exit the virtual environment:
```
deactivate
```

