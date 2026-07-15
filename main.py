import requests
import keys

response = requests.get(
    f"{keys.BASE_URL}/team/frc1619",
    headers=keys.headers
)

if response.ok:
    team_data = response.json()
    print(f"Team Name: {team_data['nickname']}")
    print(f"City: {team_data['city']}")
    print(f"Rookie Year: {team_data['rookie_year']}")
else:
    print(f"Error {response.status_code}: {response.text}")