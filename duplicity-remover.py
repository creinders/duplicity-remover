#!/usr/bin/env python2
import os, argparse, datetime
import dateutil.parser

def parse_args():
    global args

    parser = argparse.ArgumentParser(
        description="Removes old duplicity backup files"
    )

    parser.add_argument(
        "--version", action="version",
        version="%(prog)s 1.0"
    )

    parser.add_argument(
        "--force", action="store_true", default=False,
        help="delete files. If False only print files that can be removed (default: %(default)s)"
    )

    parser.add_argument(
        "--remove-all-but-n-full", dest="N", type=int, required=True,
        help="keeps n full backups and removes all older backups"
    )

    parser.add_argument(
        "path",
        help="path to backup folder"
    )
    args = parser.parse_args()

    args.remove_all_but_n_full = args.N
    args.path = os.path.realpath(args.path)

parse_args()

FLAG_PREFIX = "FLAG_"
FLAG_FULL = "FLAG_FULL"
FLAG_INC = "FLAG_INC"

now = datetime.datetime.now()

print("------ start duplicity-remover ------")
print("Time: " + str(now))
print("Path: " + args.path)

deletions_available = False

files = os.listdir(args.path)

grouped = {}

for file in files:
    if file.startswith("."):
        continue
    if not file.startswith("duplicity"):
        continue

    parts = file.split(".")
    if len(parts) < 2:
        print("Error: Wrong file format " + file)
        exit()

    type = parts[0]

    timestamp = None
    flag = None

    if type == "duplicity-full":
        timestamp = parts[1]
        flag = FLAG_FULL

    elif type == "duplicity-full-signatures":
        timestamp = parts[1]
        flag = FLAG_FULL

    elif type == "duplicity-new-signatures":
        if len(parts) < 4:
            print("Error: Wrong file format " + file)
            exit()

        timestamp = parts[3]
        flag = FLAG_INC

    elif type == "duplicity-inc":
        if len(parts) < 4:
            print("Error: Wrong file format " + file)
            exit()

        timestamp = parts[3]
        flag = FLAG_INC
    else:
        print("Unknown file " + file)
        exit()

    date = dateutil.parser.parse(timestamp) #throws exception if not a timestamp
    if date is None:
        print("Error: Wrong file format " + file)
        exit()

    if date in grouped:
        grouped_files = grouped[date]
        grouped_files.append(file)
    else:
        grouped_files = [flag, file]
        grouped[date] = grouped_files

count_full = 0

for key in sorted(grouped.iterkeys(), reverse=True):
    value = grouped[key]
    #print key

    if count_full >= args.remove_all_but_n_full:
        for file in value:
            if file.startswith(FLAG_PREFIX):
                continue

            print("remove " + file)
            deletions_available = True

            if args.force:
                file_path = os.path.join(args.path, file)
                os.remove(file_path)

    if FLAG_FULL in value:
        count_full += 1
        #print "FULL"

if not deletions_available:
    print("Nothing to do")