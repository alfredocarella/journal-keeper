#!/usr/bin/env python3

"""The ugliest daily journal script in the world... but it works for me
"""

import os
import os.path
from datetime import date, datetime
import locale
import sys
import platform

def create_main_index(base_path: str, file_name: str):

    # Insert header at the beginning
    with open(os.path.join(base_path, "header.adoc"), "r") as header_file:
        journal_header = header_file.read()

    # Add daily entries, grouped by year and month
    with open(os.path.join(base_path, file_name), "w") as f:
        f.write(journal_header)

        years = sorted(rec.name for rec in os.scandir(base_path) if rec.name.isdigit() and rec.is_dir())
        for year in years:
            year_dir = os.path.join(base_path, year)
            yearly_entries = sum([len(files) for r, d, files in os.walk(year_dir)])
            f.write("\n== {0} ({1})\n".format(year, yearly_entries))

            months = sorted(rec.name for rec in os.scandir(year_dir) if rec.name.isdigit() and rec.is_dir())
            for month in months:
                month_dir = os.path.join(year_dir, month)
                monthly_entries = sum([len(files) for r, d, files in os.walk(month_dir)])
                f.write("\n=== {0} ({1})\n".format(date(int(year), int(month), 1).strftime('%B').capitalize(), monthly_entries))

                days = sorted(rec.name for rec in os.scandir(month_dir) if rec.name.endswith('.txt') and rec.is_file())
                for day in days:
                    day_path = os.path.join(month_dir, day)
                    with open(day_path) as day_file:
                        day_entry = day_file.read()
                    if day_entry == "":
                        os.remove(day_path)
                    else:
                        day_date = date(int(year), int(month), int(day[:-4]))
                        f.write("\n==== {0} ({1})\n".format(day_date.strftime("%x"), day_date.strftime("%A")))
                        f.write("\n" + day_entry + "\n")

    # Run Asciidoctor on .adoc file
    if platform.system() != "Windows":
        os.system('asciidoctor "{0}/{1}"'.format(base_path, file_name))


def open_journal(base_path: str, editing_app: "editing app exec"="vim"):
    now = datetime.now()
    this_month = os.path.join(base_path, str(now.year), str(now.month).zfill(2))
    today_file = os.path.join(this_month, str(now.day).zfill(2) + ".txt")

    if not os.path.isdir(this_month):
        os.makedirs(this_month)

    if not os.path.isfile(today_file):
        with open(today_file, 'w') as f:
            with open(os.path.join(base_path, "day_template.adoc")) as template:
                f.write(template.read())
    if platform.system() == "Windows":
        os.system(r'"{0} "{1}""'.format(editing_app, today_file))
    else:
        os.system('{0} {1}'.format(editing_app, today_file))

if __name__ == "__main__":
    if platform.system() == "Windows":
        editor = '"C:\\Program Files\\Sublime Text 3\\sublime_text.exe"'
    else:
        editor = sys.argv[1] if len(sys.argv) > 1 else "vim"

    locale.setlocale(locale.LC_ALL, '')
    journal_path = os.path.dirname(os.path.realpath(__file__))

    open_journal(journal_path, editor)
    create_main_index(journal_path, "journal.adoc")
