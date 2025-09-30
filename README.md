## Project Overview
This project is a CLI tool for evaluating the trustworthiness of machine learning models from huggingface.  

Given a text file of URLs, the tool:
- Fetches metadata from Hugging Face,
- Extracts and cleans README files,
- Computes several metrics (ramp-up time, license availability, dataset quality, etc),
- Prints results directly to the console

## Prerequisites
- Python 3.12.10+  
- IDE or Linux

## Getting Started
Windows/IDE Terminal:
- Run 'python main.py install' or 'python3 main.py install'

Linux:
- Run './run install'
  
This will download all dependencies required for this program. Make sure to have Python install on your machine.

## How to use
Windows/IDE Terminal:
- Run 'python main.py test' or 'python3 main.py test' for test execution
- Run 'python main.py URL_FILE' or 'python3 main.py URL_FILE' where 'URL_FILE' is the absolute location of the text file that contains all the URLS.

Linux:
- Run './run test' for test execution
- Run './run URL_FILE' where 'URL_FILE' is the absolute location of the text file that contains all the URLS.

Example Output if './run URL_FILE' was done correctly:
'{"name": "bert-base-uncased", "category": "MODEL", "net_score": 0.66, "net_score_latency": 0, "ramp_up_time": 0.39, "ramp_up_time_latency": 1374, "bus_factor": 1.0, "bus_factor_latency": 870, "performance_claims": 1.0, "performance_claims_latency": 851, "license": 1.0, "license_latency": 0, "size_score": {"raspberry_pi": 0.0, "jetson_nano": 0.0, "desktop_pc": 0.78, "aws_server": 0.91}, "size_score_latency": 3506, "dataset_and_code_score": 1.0, "dataset_and_code_score_latency": 0, "dataset_quality": 0.2, "dataset_quality_latency": 0, "code_quality": 0.5, "code_quality_latency": 2250}'

## Project Structure
CSCI45000-Team-Project/
- ├── model.py        # Handles all data fetches (licenses, sizes, READMEs, datasets, etc)
- ├── metrics.py      # Computes and handle how metrics are calculated
- ├── main.py         # CLI entry point, parses input file and prints results
- ├── run             # Helper script for Linux execution
- ├── tests/          # Directory containing all test files
- │ └── test.py       # Unit tests for Model and Metrics
- └── README.md       # Project documentation

## Metric Weights
- **License**: 0.2 | 20%  
- **Dataset Quality**: 0.13 | 13%  
- **Code Quality**: 0.13 | 13%  
- **Ramp Up Time**: 0.12 | 12%  
- **Bus Factor**: 0.12 | 12%  
- **Size**: 0.1 | 10%  
- **Performance Claims**: 0.1 | 10%  
- **Dataset and Code**: 0.1 | 10% 
