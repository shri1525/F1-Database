from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.oauth2.id_token
from google.auth.transport import requests
from google.cloud import firestore
from urllib.parse import unquote  
from google.cloud.firestore_v1.base_query import FieldFilter

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

firestore_db = firestore.Client()

firebase_request_adapter = requests.Request()

def validateFirebaseToken(id_token):
    if not id_token:
        return None
    try:
        user_token = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        return user_token
    except ValueError as err:
        print(str(err))
        return None

# Function to add a driver 
def add_driver(driver_data):
    driver_ref = firestore_db.collection('drivers').document(driver_data["name"])
    if driver_ref.get().exists:
        return False  
    driver_ref.set(driver_data)
    return True

# Function to add a team 
def add_team(team_data):
    team_ref = firestore_db.collection('teams').document(team_data["name"])
    if team_ref.get().exists:
        return False  
    team_ref.set(team_data)
    return True

# Root route to display the main page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)

    # Fetch all drivers and teams
    drivers = firestore_db.collection('drivers').stream()
    teams = firestore_db.collection('teams').stream()

    driver_list = [driver.to_dict() for driver in drivers]
    team_list = [team.to_dict() for team in teams]

    return templates.TemplateResponse("main.html", {
        "request": request,
        "user_token": user_token,
        "drivers": driver_list,
        "teams": team_list
    })

# Route to display the "Add Driver" page
@app.get("/add-driver", response_class=HTMLResponse)
async def add_driver_page(request: Request):
    return templates.TemplateResponse("drivers.html", {"request": request})

# Route to handle driver addition
@app.post("/add-driver", response_class=RedirectResponse)
async def add_driver_handler(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    pole_positions: int = Form(...),
    race_wins: int = Form(...),
    points_scored: int = Form(...),
    world_titles: int = Form(...),
    fastest_laps: int = Form(...),
    team: str = Form(...),
):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")

    driver_data = {
        "name": name,
        "age": age,
        "pole_positions": pole_positions,
        "race_wins": race_wins,
        "points_scored": points_scored,
        "world_titles": world_titles,
        "fastest_laps": fastest_laps,
        "team": team
    }

    if not add_driver(driver_data):
        return RedirectResponse("/add-driver?error=duplicate", status_code=303)

    return RedirectResponse("/", status_code=303)

# Route to display the "Add Team" page
@app.get("/add-team", response_class=HTMLResponse)
async def add_team_page(request: Request):
    return templates.TemplateResponse("teams.html", {"request": request})

# Route to handle team addition
@app.post("/add-team", response_class=RedirectResponse)
async def add_team_handler(
    request: Request,
    name: str = Form(...),
    year_founded: int = Form(...),
    pole_positions: int = Form(...),
    race_wins: int = Form(...),
    constructor_titles: int = Form(...),
    previous_season_finish: int = Form(...),
):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")

    team_data = {
        "name": name,
        "year_founded": year_founded,
        "pole_positions": pole_positions,
        "race_wins": race_wins,
        "constructor_titles": constructor_titles,
        "previous_season_finish": previous_season_finish
    }

    if not add_team(team_data):
        return RedirectResponse("/add-team?error=duplicate", status_code=303)

    return RedirectResponse("/", status_code=303)

# Route to display driver details
@app.get("/driver/{driver_name}", response_class=HTMLResponse)
async def driver_details(request: Request, driver_name: str):
    driver_name = unquote(driver_name)  

    driver_ref = firestore_db.collection('drivers').document(driver_name)
    driver_doc = driver_ref.get()

    if not driver_doc.exists:
        return RedirectResponse("/")  

    driver = driver_doc.to_dict()
    return templates.TemplateResponse("driver_details.html", {"request": request, "driver": driver})

# Route to display team details
@app.get("/team/{team_name}", response_class=HTMLResponse)
async def team_details(request: Request, team_name: str):
    team_name = unquote(team_name)  

    team_ref = firestore_db.collection('teams').document(team_name)
    team_doc = team_ref.get()

    if not team_doc.exists:
        return RedirectResponse("/")  

    team = team_doc.to_dict()
    return templates.TemplateResponse("team_details.html", {"request": request, "team": team})

# Route to query drivers
@app.post("/query-drivers", response_class=HTMLResponse)
async def query_drivers(
    request: Request,
    attribute: str = Form(...),
    comparison: str = Form(...),
    value: int = Form(...)
):
    drivers_ref = firestore_db.collection('drivers')

    # Use FieldFilter for the query
    if comparison == "<":
        query = drivers_ref.where(filter=FieldFilter(attribute, "<", value))
    elif comparison == ">":
        query = drivers_ref.where(filter=FieldFilter(attribute, ">", value))
    else:
        query = drivers_ref.where(filter=FieldFilter(attribute, "==", value))

    drivers = query.stream()
    driver_list = [driver.to_dict() for driver in drivers]

    return templates.TemplateResponse("drivers_results.html", {
        "request": request,
        "user_token": None,  
        "drivers": driver_list,
        "teams": []  
    })

# Route to query teams
@app.post("/query-teams", response_class=HTMLResponse)
async def query_teams(
    request: Request,
    attribute: str = Form(...),
    comparison: str = Form(...),
    value: int = Form(...)
):
    teams_ref = firestore_db.collection('teams')

    # Use FieldFilter for the query
    if comparison == "<":
        query = teams_ref.where(filter=FieldFilter(attribute, "<", value))
    elif comparison == ">":
        query = teams_ref.where(filter=FieldFilter(attribute, ">", value))
    else:
        query = teams_ref.where(filter=FieldFilter(attribute, "==", value))

    teams = query.stream()
    team_list = [team.to_dict() for team in teams]

    return templates.TemplateResponse("teams_results.html", {
        "request": request,
        "user_token": None,  
        "drivers": [],  
        "teams": team_list
    })

# Route to display the edit driver page
@app.get("/edit-driver/{driver_name}", response_class=HTMLResponse)
async def edit_driver_page(request: Request, driver_name: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")  

    driver_name = unquote(driver_name)  
    print(f"Attempting to edit driver: {driver_name}")  

    driver_ref = firestore_db.collection('drivers').document(driver_name)
    driver_doc = driver_ref.get()

    if not driver_doc.exists:
        print(f"Driver '{driver_name}' does not exist.")  
        return RedirectResponse("/")  

    driver = driver_doc.to_dict()
    print(f"Driver data: {driver}")  

    return templates.TemplateResponse("edit_drivers.html", {"request": request, "driver": driver})

# Route to handle driver updates
@app.post("/edit-driver/{driver_name}", response_class=RedirectResponse)
async def edit_driver_handler(
    request: Request,
    driver_name: str,
    age: int = Form(...),
    pole_positions: int = Form(...),
    race_wins: int = Form(...),
    points_scored: int = Form(...),
    world_titles: int = Form(...),
    fastest_laps: int = Form(...),
    team: str = Form(...),
):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")  

    driver_ref = firestore_db.collection('drivers').document(driver_name)
    if not driver_ref.get().exists:
        return RedirectResponse("/")  

    driver_data = {
        "age": age,
        "pole_positions": pole_positions,
        "race_wins": race_wins,
        "points_scored": points_scored,
        "world_titles": world_titles,
        "fastest_laps": fastest_laps,
        "team": team
    }

    driver_ref.update(driver_data)  
    return RedirectResponse("/", status_code=303)

# Route to display the edit team page
@app.get("/edit-team/{team_name}", response_class=HTMLResponse)
async def edit_team_page(request: Request, team_name: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")  

    team_ref = firestore_db.collection('teams').document(team_name)
    team_doc = team_ref.get()

    if not team_doc.exists:
        return RedirectResponse("/")  

    team = team_doc.to_dict()
    return templates.TemplateResponse("edit_teams.html", {"request": request, "team": team})

# Route to handle team updates
@app.post("/edit-team/{team_name}", response_class=RedirectResponse)
async def edit_team_handler(
    request: Request,
    team_name: str,
    year_founded: int = Form(...),
    pole_positions: int = Form(...),
    race_wins: int = Form(...),
    constructor_titles: int = Form(...),
    previous_season_finish: int = Form(...),
):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")  

    team_ref = firestore_db.collection('teams').document(team_name)
    if not team_ref.get().exists:
        return RedirectResponse("/")  

    team_data = {
        "year_founded": year_founded,
        "pole_positions": pole_positions,
        "race_wins": race_wins,
        "constructor_titles": constructor_titles,
        "previous_season_finish": previous_season_finish
    }

    team_ref.update(team_data)  
    return RedirectResponse("/", status_code=303)

# Route to delete a driver
@app.post("/delete-driver/{driver_name}", response_class=RedirectResponse)
async def delete_driver(request: Request, driver_name: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")  

    driver_ref = firestore_db.collection('drivers').document(driver_name)
    if not driver_ref.get().exists:
        return RedirectResponse("/")  

    driver_ref.delete()  
    return RedirectResponse("/", status_code=303)

# Route to delete a team
@app.post("/delete-team/{team_name}", response_class=RedirectResponse)
async def delete_team(request: Request, team_name: str):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")  

    team_ref = firestore_db.collection('teams').document(team_name)
    if not team_ref.get().exists:
        return RedirectResponse("/")  

    team_ref.delete()  
    return RedirectResponse("/", status_code=303)

# Route to display the compare drivers page
@app.get("/compare-drivers", response_class=HTMLResponse)
async def compare_drivers_page(request: Request):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")  

    drivers = firestore_db.collection('drivers').stream()
    driver_list = [driver.to_dict() for driver in drivers]

    return templates.TemplateResponse("compare.html", {
        "request": request,
        "drivers": driver_list
    })

# Route to handle driver comparison
@app.post("/compare-drivers", response_class=HTMLResponse)
async def compare_drivers(
    request: Request,
    driver1: str = Form(...),
    driver2: str = Form(...),
):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")  

    driver1_ref = firestore_db.collection('drivers').document(driver1)
    driver2_ref = firestore_db.collection('drivers').document(driver2)

    driver1_doc = driver1_ref.get()
    driver2_doc = driver2_ref.get()

    if not driver1_doc.exists or not driver2_doc.exists:
        return RedirectResponse("/")  

    driver1_data = driver1_doc.to_dict()
    driver2_data = driver2_doc.to_dict()

    return templates.TemplateResponse("compare-results.html", {
        "request": request,
        "driver1": driver1_data,
        "driver2": driver2_data
    })

# Route to display the compare teams page
@app.get("/compare-teams", response_class=HTMLResponse)
async def compare_teams_page(request: Request):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")

    teams = firestore_db.collection('teams').stream()
    team_list = [team.to_dict() for team in teams]

    return templates.TemplateResponse("compare_teams.html", {  
        "request": request,
        "teams": team_list
    })

# Route to handle team comparison
@app.post("/compare-teams", response_class=HTMLResponse)
async def compare_teams(
    request: Request,
    team1: str = Form(...),
    team2: str = Form(...),
):
    id_token = request.cookies.get("token")
    user_token = validateFirebaseToken(id_token)
    if not user_token:
        return RedirectResponse("/")

    team1_ref = firestore_db.collection('teams').document(team1)
    team2_ref = firestore_db.collection('teams').document(team2)

    team1_doc = team1_ref.get()
    team2_doc = team2_ref.get()

    if not team1_doc.exists or not team2_doc.exists:
        return RedirectResponse("/")

    team1_data = team1_doc.to_dict()
    team2_data = team2_doc.to_dict()

    return templates.TemplateResponse("compare_teams_results.html", {  
        "request": request,
        "team1": team1_data,
        "team2": team2_data
    })