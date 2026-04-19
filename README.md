## Chat With Your Data
A web application that allows users to upload a CSV file and ask natural language questions about their data. The system uses a Large Language Model (LLM) to generate Pandas code, executes it safely, and returns the result.

## Demo
Live Website: https://chat-with-your-data-2arw.onrender.com

GitHub Repo: https://github.com/awang182-ux/Chat-With-Your-Data

## Overview
The system uses a Large Language Model (LLM) to generate Pandas code, executes it safely, and returns the result.

Users can:
1. Upload a CSV file
2. Ask a question in plain English
3. Receive computed results powered by Pandas

## 📂 Sample Data

We provide example CSV files in the `sample_data/` folder for testing.

Example questions:

Sales Data
- What is the average Sales by Region?
- Which Region has the highest total Sales?
- Which Region has the highest average Profit?

Student Data
- What is the average GPA by major?
- What is the average GPA by major?
- Rank GPA from Highest to Lowest

Orders Data
- What is the total Amount?
- What is the total Amount by Customer?
- Which Customer spent the most?

## ⚙️ How It Works

1. CSV file is uploaded and loaded into a Pandas DataFrame  
2. A summary of the dataset (columns, types, preview) is generated  
3. A prompt is built using the dataset and user question  
4. The LLM generates Pandas code  
5. The code is executed in a restricted environment  
6. The result is returned and displayed in the UI

## 🛠️ Tech Stack

**Backend**
- Python
- Flask
- Pandas
- OpenRouter / OpenAI API

**Frontend**
- HTML, CSS, JavaScript


## ⚙️ Setup Instructions

Clone the repository:

```bash
git clone https://github.com/awang182-ux/Chat-With-Your-Data.git
cd Chat-With-Your-Data
