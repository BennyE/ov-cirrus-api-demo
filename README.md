## OmniVista Cirrus 10.3 API Demo

- Create AppId/AppSecret from your OmniVista Cirrus 10.3 User Profile
- Adapt/Create ovc_application_settings.json from (-example)
- Adapt/Create ovc_url.json from (-example)
- Ensure you have python-requests installed in your .venv (python3 -m pip install requests)

```
% python3 ov-cirrus-api-demo.py
### /api/ov/v1/applications/authenticate - Access Token ###
REDACTED
### /api/ov/v1/user/profile - User Profile ###
REDACTED
### /api/ov/v1/organizations/permissions - Organisation Permissions ###
{
    "status": 200,
    "message": "All permissions has been successfully fetched.",
    "data": [
        {
            "id": "649da69789609a0d13xxxxxx",
            "role": "ORGANIZATION_VIEWER",
            "organization": "6412db72ae6ff46588xxxxxx"
        }
    ]
}
### /api/ov/v1/sites/permissions - Sites Permissions ###
{
    "status": 200,
    "message": "All permissions has been successfully fetched.",
    "data": [
        {
            "id": "649da69789609a7cd9xxxxxx",
            "role": "SITE_VIEWER",
            "site": "6412db72ae6ff4c78cxxxxxx"
        },
        {
            "id": "649da69789609a2b7dxxxxxx",
            "role": "SITE_VIEWER",
            "site": "64142c54ae6ff4bd1cxxxxxx"
        }
    ]
}
### /api/ov/v1/organizations/<ORGANISATION>/sites/<SITE> - Site: Details ###
{
    "status": 200,
    "message": "The site has been successfully fetched.",
    "data": {
        "createdAt": "2023-03-16T09:03:46.351Z",
        "updatedAt": "2023-06-28T12:13:58.419Z",
        "id": "6412db72ae6ff4c78xxxxxx",
        "name": "Unnamed site",
        "countryCode": "DE",
        "timezone": "Europe/Berlin",
        "address": "",
        "location": {},
        "imageUrl": "",
        "isDefault": false,
        "zoom": 4,
        "organization": "6412db72ae6ff46588xxxxxx"
    }
}
### Getting Devices for Unnamed site ###
No devices on this site!
### /api/ov/v1/organizations/<ORGANISATION>/sites/<SITE> - Site: Details ###
{
    "status": 200,
    "message": "The site has been successfully fetched.",
    "data": {
        "createdAt": "2023-03-17T09:01:08.487Z",
        "updatedAt": "2023-06-28T12:13:58.422Z",
        "id": "64142c54ae6ff4bd1cxxxxxx",
        "name": "Hamburg",
        "countryCode": "DE",
        "timezone": "Europe/Berlin",
        "address": "Elbe\u00a0Philharmonic\u00a0Hall,\u00a01,\u00a0Platz\u00a0der\u00a0Deutschen\u00a0Einheit,\u00a0Quartier\u00a0Am\u00a0Sandtorkai/Dalmannkai,\u00a0HafenCity,\u00a0Hamburg-Mitte,\u00a0Hamburg,\u00a020457,\u00a0Germany",
        "location": {
            "type": "Point",
            "coordinates": [
                "9.984206",
                "53.541292"
            ]
        },
        "imageUrl": "cdcda0eb-03ba-460b-a524-e2760aad9dca.png",
        "isDefault": true,
        "zoom": 18,
        "organization": "6412db72ae6ff46588xxxxxx"
    }
}
### Getting Devices for Hamburg ###
### /api/ov/v1/organizations/<ORGANISATION>/sites/<SITE>/devices - Site: Devices ###
{
    "status": 200,
    "message": "Devices have been successfully fetched.",
    "data": [
        {
            "pingTime": 1680267120,
            "createdAt": "2023-03-17T09:05:24.145Z",
            "updatedAt": "2023-06-29T20:24:32.776Z",
...
```
