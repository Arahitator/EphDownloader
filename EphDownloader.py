import ftplib
import datetime
import os


def to_gps_date(ymd):
    y, m, d = ymd
    epoch = datetime.date(1980, 1, 6)
    our_date = datetime.date(int(y), int(m), int(d))
    delta = our_date - epoch
    return delta.days // 7, delta.days % 7


def ask_dates():
    while True:
        try:
            first_date = input("Введите дату первого дня интервала в формате 'ГГГГ (М)М (Д)Д'\n"
                                           "----->").split()
        except ValueError as er:
            print(f'Дата введена в неверном формате ({er}), попробуйте еще раз')
        else:
            break

    while True:
        try:
            last_date = input("Введите дату последнего дня интервала в формате 'ГГГГ (М)М (Д)Д'\n"
                                          "-----> ").split()
        except ValueError as er:
            print(f'Дата введена в неверном формате ({er}), попробуйте еще раз')
        else:
            break
    print("Временной интервал принят, устанавливаю подключение к серверу")
    return first_date, last_date


def get_eph():
    first_date, last_date = ask_dates()
    start, end = map(to_gps_date, [first_date, last_date])
    dir_name = "Эфемериды(" + "_".join(first_date) + "-" + "_".join(last_date) + ")"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    day = start[1]
    ftp = ftplib.FTP('lox.ucsd.edu')
    login = ftp.login()
    if login == '230 Login successful.':
        print("Подключение успешно установлено")
        ftp.cwd('archive/garner/products')
    else:
        print("Не удается подключиться к серверу :'(")
    for week in range(start[0], end[0] + 1):
        ftp.cwd(str(week))
        while True:
            gname = f'igs{week}{day}.sp3.Z'
            rname = f'igl{week}{day}.sp3.Z'
            with open(f"{dir_name}\\{gname}", "wb") as f1:
                try:
                    ftp.retrbinary('RETR ' + gname, f1.write)
                    print(f'Скачан файл {gname}')
                except ftplib.error_perm:
                    print(f'Файл {gname} отсутствует на сервере')
            with open(f"{dir_name}\\{rname}", "wb") as f2:
                try:
                    ftp.retrbinary('RETR ' + rname, f2.write)
                    print(f'Скачан файл {rname}')
                except ftplib.error_perm:
                    print(f'Файл {rname} отсутствует на сервере')
            if (week, day) == end:
                break
            elif day == 6:
                day = 0
                break
            else:
                day += 1
        ftp.cwd("..")


if __name__ == "__main__":
    get_eph()
    input("Программа выполнена, для завершения нажмите ENTER")
