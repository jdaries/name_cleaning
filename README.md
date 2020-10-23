# name_cleaning
A very simple process for cleaning up employer and university names

## What's in this repo?
1. Jupyter notebooks
    1. Employer name cleaning application.ipynb
    1. employer db lookup.ipynb
1. Python scripts
    1. Employer name cleaning application.py (export from Jupyter of the equivalent notebook)
    1. employer db lookup.py (export from Jupyter of the equivalent notebook)
1. Employer name database, employer_names.db (sqlite format)

## How do I use it?

You'll need to have a list of employer or university names that you want to clean. This should be saved as an Excel, in a single column with the column heading of "Employer"

You will also need a sqlite database that has existing pairs of raw names and clean names. You are free to use the one included in this repo, it has been filled using nearly a decade of survey data from MIT exit surveys for graduating students. Some of the choices of standardized names that I have made may not match the choices you would make, so you might want to browse the database first before deciding. If you want to make your own, then here is the table creation script for the single table in the database:

`CREATE TABLE employer_pairs ('RAW_NAME','CLEAN_NAME', count);`

If you open the Employer name cleaning Jupyter notebook (or run the equivalent .py script) then you just run the whole thing after you update the name of the database and the input and output file names. Then you will have a simple interactive text session where you process your file row by row. Rows that have exact matches in the database are processed automatically and you are prompted to choose matches for any that have a close match. If no close match is found, you'll be asked to enter a name. 

This was not developed to be a robust application, it's just something simple that I've used for my own purposes for a few years, and so I make no guarantees! Please feel free to submit a PR if you have ideas of how to improve it.