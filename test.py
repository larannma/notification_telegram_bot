from datetime import datetime, timezone

current_utc_time = datetime.now(timezone.utc)
print(current_utc_time)