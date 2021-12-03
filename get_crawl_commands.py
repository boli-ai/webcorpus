import argparse
import os
from urllib.parse import urlparse, parse_qsl, unquote_plus
import pandas as pd


def normalize_url(url):
    if not url.startswith("http") and not url.startswith("https"):
        url = "http://{0}".format(url)
    parts = urlparse(url)
    _query = frozenset(parse_qsl(parts.query))
    _path = unquote_plus(parts.path)
    parts = parts._replace(query=_query, path=_path)
    # strip www. from netloc
    domain = parts.netloc.strip("www.")
    # path is not important as we are doing a deep crawl
    # path = parts[2].strip("/")
    return domain


def read_lines(path):
    # if path doesnt exist, return empty list
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        lines = f.readlines()
    lines = [line.strip("\n") for line in lines]
    return lines


def read_csv_sources(path):
    df = pd.read_csv(path)
    return df["home_url"].tolist()


def create_txt(outFile, lines):
    add_newline = not "\n" in lines[0]
    outfile = open("{0}".format(outFile), "w")
    for line in lines:
        if add_newline:
            outfile.write(line + "\n")
        else:
            outfile.write(line)

    outfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get crawl commands for a given text file"
    )
    parser.add_argument(
        "-quiet", "--q", help="Quiet mode", action="store_true", default=False
    )
    parser.add_argument("-f", "--file", help="Text/CSV file to crawl", required=True)
    parser.add_argument(
        "-lp", "--log_path", help="Path to webcorpus logs folder", required=True
    )
    parser.add_argument(
        "-of",
        "--output_folder",
        help="Output folder for saving crawls. The crawls would be saved in {output_folder}/lang_code",
        required=True,
    )

    args = parser.parse_args()
    file = args.file
    if file.endswith(".csv"):
        lines = read_csv_sources(file)
    elif file.endswith(".txt"):
        lines = read_lines(file)
    else:
        raise NotImplementedError("Only .txt and .csv files are supported")

    if args.q:
        print("Found {0} sources".format(len(lines)))
        print("samples sources: ", lines[:5])

    # convert log_path and output folder to absolute paths
    args.log_path = os.path.abspath(args.log_path)
    args.output_folder = os.path.abspath(args.output_folder)
    # convert windows path to unix path
    args.log_path = args.log_path.replace("\\", "/")
    args.output_folder = args.output_folder.replace("\\", "/")
    # folder = file.split("/")[0]
    if "/" in file:
        lang_code = file.split("/")[1].split(".")[0]
    else:
        lang_code = file.split(".")[0]

    commands = []

    for line in lines:
        line = line.strip("\n")
        if not line.startswith("http") and not line.startswith("https"):
            line = "http://{0}".format(line)
        # remove last .com, .org, .net, .edu etc
        domain_name = ".".join(normalize_url(line).split(".")[:-1])
        if domain_name == "":
            print("==============================================")
            print(f"recheck this source {line} -> {normalize_url(line)}")
            print("==============================================")
            exit(1)
        # replace . and / in source name to _
        domain_name = domain_name.replace(".", "_")
        domain_name = domain_name.replace("/", "_")
        domain_name = domain_name.replace("\\", "_")

        # html_path = f"/home/gowtham_ramesh1/{lang_code}/{domain_name}"
        html_path = f"{args.output_folder}/{lang_code}/{domain_name}"
        source_name = domain_name
        home_url = line
        # log_path = "/home/gowtham_ramesh1/webcorpus/logs"
        command = f"curl http://localhost/schedule.json -d project=webcorpus -d spider=recursive-spider -d html_path={html_path} -d source_name={source_name} -d home_url={home_url} -d lang={lang_code} -d log_path={args.log_path}"

        commands.append(command)
        if args.q is False:
            print(command)

    create_txt(
        f"{lang_code}_commands.txt",
        commands,
    )
    if args.q is False:
        print()
        print("Commands written to {0}_commands.txt".format(lang_code))
