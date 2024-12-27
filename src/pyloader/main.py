from datetime import date, timedelta

if __name__ == "__main__":
    today = date(2024, 1, 1)
    nextd = today + timedelta(days=1)
    print(nextd.strftime("%Y%m%d"))