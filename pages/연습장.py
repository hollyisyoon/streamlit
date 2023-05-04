from datetime import datetime, timedelta, date


min_date = date(2022, 7, 25)
max_date = date(2023, 4, 26)

# 시작 날짜와 끝 날짜를 동시에 입력받음
start_end_date = st.date_input("시작 날짜 - 끝 날짜",
                                value=(date(2023,4,5), date(2023,4,20)),
                                min_value=min_date + timedelta(days=7),
                                max_value=max_date - timedelta(days=90),
                                key="date_range")
start_date = start_end_date[0]
end_date = start_end_date[1]
