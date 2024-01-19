# S&P 500 Stock Screener and Portfolio Recommender
This repository will scrape Yahoo Finance for SP 500 member company performance metrics and rank them within the categories of 1-year return, trading volume, recommendation rating, market capitalization, and price to earnings ration. The analysis file will also allow the user to follow prompts and select a custom-made investment portfolio allocation recommendation. 

## Instructions to create a conda environment
For ease of operation, all .py files should be placed in the same folder and the cd set to that folder for quick utilization. The steps are sequential and linked through the code. This project was created in pycharm for windows. The associated workflow diagram is posted as 'project_workflow.pdf'.

## Instructions on how to install the required libraries
After ensuring that you have set your cd to the folder containing the requirements.txt, here the src folder, run: pip install -r requirements.txt 

## Instructions on how to download the data
First open datacollection.py and run. Ensure that line 264 "sp500merged.to_csv('dataforcleaning.csv', index=False)" is not commented out! This will produce a file called 'dataforcleaning.csv' in your working directory. Line 265 will create the second file: 'indexdata.csv'. These files, as generated for the report, are included in the data/raw folder.

## Instructions on how to clean the data
Open datacleaning.py from the same folder/cd as your previous output files and click Run. This should output two cleaned files: 'dataforanalysis.csv' and 'indexdataforanalysis.csv'. These files, as generated for the report, are included in the data/processed folder.

## Instructions on how to run analysis code
Open dataanalysis.py from the same folder/cd as your previous output files and click Run. This will generate an in-step analysis of the code in the terminal as well as prompt the user for answers to a series of questions that will build a personalized portfolio and investment amounts. If instructions are not followed precisely, an exception will be raised with clarifying guidance and the user must restart the program. It will also output four files for visualization: 'dataforvisualization.csv', 'dataforvisualization1.csv', 'portfolio_options_performance.csv', and 'myportfolio.csv, the last being the custom-tailored portfolio. In its current form, the program will generate one of 11 different portfolio recommendations that are all subsets of the S&P 500. These files, as generated for the report, are included in the data/processed folder.

## Instructions on how to create visualizations
Open datavisualization.py from the same folder/cd as your previous output files and click Run. The visuals generated are the raw images contained in the final report. These files, as generated for the report, are included in the /results folder.

*******For legal reasons, author is not a licensed financial advisor and recommendations are made for entertainment purposes only******
