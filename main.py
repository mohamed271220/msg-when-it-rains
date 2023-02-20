import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# use twillo.com for numbers message

OWN_POINT = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "YOUR ACCOUNT SID"
auth_token = os.environ.get("AUTH_TOKEN")

api_key = "d034dbce78c2c78947c3a893426deb21"
weather_prams = {
    "lat": 31.085135,
    "lon": 32.373963,
    "exclude": "current,minutely,daily",
    "appid": api_key,

}

response = requests.get(OWN_POINT, params=weather_prams)
print(response.status_code)
response.raise_for_status()
weather_data = response.json()

weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL NUMBER"
    )
    print(message.status)
# print(weather_data["hourly"][0]["weather"][0]["id"])
