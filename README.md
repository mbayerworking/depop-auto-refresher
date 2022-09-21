# depop-auto-refresher
A simple bot designed to auto-refresh depop items on store pages without getting the account banned.
Originally designed for *nix
Implemention available in Windows10/11 using WSL2
https://learn.microsoft.com/en-us/windows/wsl/install

# Setup
1. Clone github repo:
```
git clone https://github.com/mdberkey/depop-auto-refresher
```
2. setup python3 virtual environment.
```
cd depop-auto-refresher && python3 -m venv ./venv
```
3. install modules
```
source venv/bin/activate && python3 -m pip install -r requirements.txt
```

4. setup XServer
```
Navigate to https://sourceforge.net/projects/vcxsrv/ or https://github.com/ArcticaProject/vcxsrv and follow instructions to install. 
```

5. launch XServer
```
run vcxsrv and disable access control option
```

6. Install Chrome, update to newest version
```
https://www.google.com/chrome/
```

7. Install corresponding Chrome Driver
```
https://chromedriver.chromium.org/downloads
```

# Use
1. Start up program
```
export DISPLAY=192.168.0.222:0.0 && cd depop-auto-refresher && . venv/bin/activate && python auto_refresher_UI_V1.py
```
2. Leave fields blank and select "Start Bot."
```
Recent updates to Depop backup causes problems with automated login. User must login themselves.
```
3. Chromedriver will launch Chrome via chrome driver. On depop login page, enter credentials and the application will autonomously refresh listings once per hour.