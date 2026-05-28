import urllib.request
import os

def download_and_format():
    os.makedirs('data', exist_ok=True)
    
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    csv_path = "data/adult.csv"
    
    headers = "age,workclass,fnlwgt,education,education-num,marital-status,occupation,relationship,race,sex,capital-gain,capital-loss,hours-per-week,native-country,income\n"
    
    print("Downloading adult.data...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        print("Saving to data/adult.csv with headers...")
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(headers)
            # Ensure we remove any empty trailing lines
            lines = [line for line in content.split('\n') if line.strip()]
            f.write('\n'.join(lines) + '\n')
            
        print("Dataset successfully downloaded and prepared!")
    except Exception as e:
        print(f"Error downloading data: {e}")

if __name__ == '__main__':
    download_and_format()
