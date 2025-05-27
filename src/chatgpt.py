import time, json
import undetected_chromedriver as uc
from pathlib import Path

USER_DATA = Path.cwd() / "EnvironmentDirectory" / "environment_1"
PROFILE   = "myprofile"
LOCAL     = USER_DATA / "Local State"

# 1. Make absolutely sure we point Chrome at the right folder:
opts = uc.ChromeOptions()
opts.add_argument(f"--user-data-dir={USER_DATA}")
opts.add_argument(f"--profile-directory={PROFILE}")

# 2. Force the metrics service to run (but not upload):
opts.add_argument("--metrics-recording-only")

# 3. Run headful (or classic headless) so metrics + crypto are not suppressed:
#    Uncomment one of the next two lines:
# opts.add_argument("--headless=new")    # newer headless
# opts.add_argument("--headless")        # classic headless
# (You can omit headless entirely to see the window.)

# launch
driver = uc.Chrome(options=opts)

# 4. Navigate somewhere that sets or reads cookies:
driver.get("https://www.google.com")
# small delay for cookie service to spin up:
time.sleep(2)
# optionally set a dummy cookie to guarantee key creation:
driver.add_cookie({"name": "clorm_test", "value": "1", "domain": ".google.com"})

# 5. Quit cleanly so Chrome flushes Local State to disk:
driver.quit()

# 6. Now inspect Local State:
data = json.loads(LOCAL.read_text(encoding="utf-8"))
print("client_id:       ", data["user_experience_metrics"]["client_id"])
print("client_id2:      ", data["user_experience_metrics"]["client_id2"])
print("client_id_time:  ", data["user_experience_metrics"]["client_id_timestamp"])
print("encrypted_key:   ", data["os_crypt"]["encrypted_key"][:16], "…")
