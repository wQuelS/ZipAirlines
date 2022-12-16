# ZipAirlines

DRF Api service for managing airplanes

## Installing using Github

Python 3.10+ is a must


1. Clone the repository:
`git clone https://github.com/wQuelS/ZipAirlines.git`
2. Setup virtual env:
    * On Windows: `venv\Scripts\activate`
    * On Linux or MacOS: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`  

**Step 4 is needed, because there must be one and only one predefined Airline**:  
4. Load data from fixture db: `python manage.py loaddata fixture_db.json`  
5. Migrate after Airline is loaded: `python manage.py migrate`  
6. Now you can run it: `python manage.py runserver`  
