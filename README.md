# Discord-Bot
A Discord bot for AWS Cloud Community's Internal Discord Server.

## :zap: Installation
**1. Clone this repo by running the below command.**

```
git clone https://github.com/AWS-Cloud-Community-LPU/Discord-Bot.git
```

**2. Now, run the following commands:**

```bash
cd Discord-Bot
pip install -r requirements.txt
```
This will install all the project dependencies.

*Note*: Recommended way is to first create a virtual environment and then install the dependencies.

**3. Configure Missing Files:**

**File: secrets.ini**
```bash
touch secrets.ini
```
A file ```secrets.ini``` is missing as it contains a token to access the HTTP API of *Odin*. The file is structured in this way: 
```
[KEYS]
API_KEY = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

**File: credentials.json**
```bash
touch credentials.json
```
A file ```credentials.json``` contains OAuth 2.0 Client IDs of Google Calendar API. Learn more about it [here](https://developers.google.com/workspace/guides/create-credentials).

**File: token.json**

The file ```token.json``` stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.

**4. :tada: Run the bot:**
```bash
python3 main.py
```

## :page_facing_up: License
[MIT](./LICENSE) © AWS Cloud Community LPU
