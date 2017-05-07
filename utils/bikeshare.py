import os, requests, zipfile

def get_year_quarter_tuples(years):
    for year in years:
        for quarter in [1,2,3,4]:

            if year == 2010 and quarter < 4: continue # First: 2010 Q4
            if year == 2016 and quarter > 1: continue #  Last: 2016 Q1

            yield (year, quarter)

def get_bikeshare_filename(year, quarter, ext):
    filename = "{year}-Q{quarter}-cabi-trip-history-data".format(year=year, quarter=quarter)
    return filename + ext

def download_bikeshare_years(years, data_folder):
    for year, quarter in get_year_quarter_tuples(years):
        download_bikeshare_data(year, quarter, data_folder)

def download_bikeshare_data(year, quarter, data_folder):
    """
    Downloads data for a given year and quarter from Capital Bikeshare's Amazon S3 into
    the given data folder.
    
    The data can be found at: https://s3.amazonaws.com/capitalbikeshare-data/index.html
    """
    
    zip_filename = get_bikeshare_filename(year, quarter, ".zip")
    csv_filename = get_bikeshare_filename(year, quarter, ".csv")

    zip_filepath = data_folder + zip_filename
    csv_filepath = data_folder + csv_filename

    if not os.path.exists(csv_filepath):
        
        # Download data from Amazon S3 using requests library
        print("Downloading:", year, "Q%d" % quarter, end=" | ")
        response = requests.get("https://s3.amazonaws.com/capitalbikeshare-data/%s" % zip_filename)

        # Write downloaded zip file to disk within the data folder
        with open(zip_filepath, "wb") as f:
            f.write(response.content)
        
        # Extract zip using the zipfile library and normalize the csv filenames to be consistent
        print("Extracting...", end=" | ")
        with open(zip_filepath, "rb") as f:
            z = zipfile.ZipFile(f)
            original_csv_filename = z.namelist()[0] # get name of first csv in zip file
            unzipped_csv_filepath = z.extract(original_csv_filename, data_folder) # extract csv file
            os.rename(unzipped_csv_filepath, csv_filepath) # normalize csv name

        print("Created:", csv_filepath)
    else:
        print("Data Exists:", year, "Q%d" % quarter, "|", data_folder + csv_filename)