import datetime

# 2 - 28 days
# 1, 3, 5, 7, 8, 10, 12 - 31 days
# 4, 6, 9, 11 - 30 days


class DateFormating:
    def __init__(self):
        self.days31 = [1, 3, 5, 7, 8, 10, 12]
        self.days30 = [4, 6, 9, 11]

    def date_formting(self, days):
        datetime_now = datetime.datetime.now()
        str_datetime = datetime_now.strftime("%Y-%m-%d-%H-%M")
        datetime_list = str_datetime.split("-")
        int_datetime_list = [int(i) for i in datetime_list]

        int_datetime_list[2] += days
        try:
            FinalDate = datetime.datetime(
                int(int_datetime_list[0]),
                int(int_datetime_list[1]),
                int(int_datetime_list[2]),
                int(int_datetime_list[3]),
                int(int_datetime_list[4]),
                0
            )
            formatted_date = datetime.datetime.fromtimestamp(FinalDate.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
            return formatted_date

        except:

            if int_datetime_list[1] in self.days31:
                temp = int_datetime_list[2] - 31
                FinalDate = datetime.datetime(
                    int(int_datetime_list[0]),
                    int(int_datetime_list[1]) + 1,
                    temp,
                    int(int_datetime_list[3]),
                    int(int_datetime_list[4]),
                    0
                )
                formatted_date = datetime.datetime.fromtimestamp(FinalDate.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
                return formatted_date

            elif int_datetime_list[1] in self.days30:
                temp = int_datetime_list[2] - 30
                FinalDate = datetime.datetime(
                    int(int_datetime_list[0]),
                    int(int_datetime_list[1]) + 1,
                    temp,
                    int(int_datetime_list[3]),
                    int(int_datetime_list[4]),
                    0
                )
                formatted_date = datetime.datetime.fromtimestamp(FinalDate.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
                return formatted_date

            elif int_datetime_list[1] == 2:
                temp = int_datetime_list[2] - 28
                FinalDate = datetime.datetime(
                    int(int_datetime_list[0]),
                    int(int_datetime_list[1]) + 1,
                    temp,
                    int(int_datetime_list[3]),
                    int(int_datetime_list[4]),
                    0
                )
                formatted_date = datetime.datetime.fromtimestamp(FinalDate.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
                return formatted_date
