#!/usr/bin/python3.5
import os
from datetime import date, datetime
# import locale
import sys


def create_main_index(base_path: str, file_name: str):

    # Insert header at the beginning
    with open(os.path.join(base_path, "header.adoc"), "r") as header_file:
        journal_header = header_file.read()

    # Add journal content
    with open(os.path.join(base_path, file_name), "w") as f:
        f.write(journal_header)

        # TODO: Encapsulate this repetitive stub in a function (use it at month-level as well)
        years = sorted(rec.name for rec in os.scandir(base_path) if not rec.name.startswith('.') and rec.is_dir())
        for year in years:
            year_dir = os.path.join(base_path, year)
            year_entries = sum([len(files) for r, d, files in os.walk(year_dir)])
            f.write("\n== {0} ({1})\n".format(year, year_entries))

            months = sorted(rec.name for rec in os.scandir(year_dir) if not rec.name.startswith('.') and rec.is_dir())
            for month in months:
                month_dir = os.path.join(year_dir, month)
                month_entries = sum([len(files) for r, d, files in os.walk(month_dir)])
                f.write("\n=== {0} ({1})\n".format(date(int(year), int(month), 1).strftime('%B'), month_entries))

                days = sorted(rec.name for rec in os.scandir(month_dir) if rec.name.endswith('.txt') and rec.is_file())
                for day in days:
                    day_path = os.path.join(month_dir, day)
                    with open(day_path) as day_file:
                        day_entry = day_file.read()
                    if day_entry == "":
                        os.remove(day_path)
                    else:
                        day_date = date(int(year), int(month), int(day[:-4]))
                        f.write("\n==== {0} {1}\n".format(day_date.strftime("%A").capitalize(), day_date.strftime("%x")))
                        f.write("\n" + day_entry + "\n")
                        # f.write("\ninclude::" + day_path_rel + "[]\n")

    # Run Asciidoctor on .adoc file
    os.system("asciidoctor {0}/{1}".format(base_path, file_name))


# def create_main_index(base_path: str, file_name: str, start_date: datetime):
#
#     # Insert header at the beginning
#     with open(os.path.join(base_path, "header.adoc"), "r") as header_file:
#         journal_header = header_file.read()
#
#     # Add journal content
#     now = datetime.now()
#     date = start_date
#     with open(os.path.join(base_path, file_name), "w") as f:
#         f.write(journal_header)
#         while date < now:
#             year_dir = os.path.join(base_path, str(date.year))
#             if date.day == date.month == 1 and os.path.isdir(year_dir) and os.listdir(year_dir):
#                 f.write("\n== {0}\n".format(date.year))
#
#             month_dir = os.path.join(base_path, str(date.year), str(date.month).zfill(2))
#             if date.day == 1 and os.path.isdir(month_dir) and os.listdir(month_dir):
#                 f.write("\n=== {0}\n".format(date.strftime("%B").capitalize()))
#
#             day_path_rel = os.path.join(str(date.year), str(date.month).zfill(2), str(date.day).zfill(2) + ".txt")
#             day_path_abs = os.path.join(base_path, day_path_rel)
#             if os.path.isfile(day_path_abs):
#                 with open(day_path_abs) as day_file:
#                     day_entry = day_file.read()
#                     if day_entry == "":
#                         os.remove(day_path_abs)
#                     else:
#                         f.write("\n==== {0} {1}\n".format(date.strftime("%A").capitalize(), date.strftime("%x")))
#                         f.write("\n" + day_entry + "\n")
#                         # f.write("\ninclude::" + day_path_rel + "[]\n")
#             date += timedelta(1)
#
#     # Run Asciidoctor on .adoc file
#     os.system("asciidoctor {0}/{1}".format(base_path, file_name))
#
#
def open_journal(base_path: str, editing_app: "editing app exec"="vim"):
    now = datetime.now()
    today_path = os.path.join(base_path, str(now.year), str(now.month).zfill(2))
    today_file = os.path.join(today_path, str(now.day).zfill(2) + ".txt")
    day_template_text = ""  # Add some text template if desired

    if not os.path.isdir(today_path):
        os.makedirs(today_path)

    if not os.path.isfile(today_file):
        with open(today_file, 'w') as f:
            f.write(day_template_text)
    os.system("{0} {1}".format(editing_app, today_file))


if __name__ == "__main__":
    editor = sys.argv[1] if len(sys.argv) > 1 else "vim"
    # locale.setlocale(locale.LC_ALL, 'es_ES')
    journal_path = os.path.dirname(os.path.realpath(__file__))
    index_name = "journal.adoc"

    create_main_index(journal_path, index_name)
    open_journal(journal_path, editor)
