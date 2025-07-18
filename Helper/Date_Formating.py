import datetime

# 2 - 28 days
# 1, 3, 5, 7, 8, 10, 12 - 31 days
# 4, 6, 9, 11 - 30 days


class DateFormating:
    def __init__(self):
        self.days31 = [1, 3, 5, 7, 8, 10, 12]
        self.days30 = [4, 6, 9, 11]

    def date_formting(self, days):
        date_now = datetime.datetime.now()
        str_date_format = date_now.strftime("%Y-%m-%d-%H-%M-%S")
        datetime_list = str_date_format.split("-")
        int_datetime_list = [int(i) for i in datetime_list]

        int_datetime_list[2] += days
        try:
            return datetime.date(
                int_datetime_list[0], int_datetime_list[1], int_datetime_list[2]
            )

        except:

            if int_datetime_list[1] in self.days31:
                temp = int_datetime_list[2] - 31
                return datetime.date(
                    int_datetime_list[0], int_datetime_list[1] + 1, temp
                )

            elif int_datetime_list[1] in self.days30:
                temp = int_datetime_list[2] - 30
                return datetime.date(
                    int_datetime_list[0], int_datetime_list[1] + 1, temp
                )

            elif int_datetime_list[1] == 2:
                temp = int_datetime_list[2] - 28
                return datetime.date(
                    int_datetime_list[0], int_datetime_list[1] + 1, temp
                )
