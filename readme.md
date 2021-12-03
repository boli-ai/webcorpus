# webcorpus

![pypi badge](https://badge.fury.io/py/webcorpus.svg)

Generate large-scale NLP corpora from web crawls. This project has been used to generate [IndicCorp](https://indicnlp.ai4bharat.org/corpora/), a large-scale corpora for Indic languages.


### Installation

Make sure you have **java** installed on your system. Next, go to the project root directory and install it using pip:

```bash
sudo pip3 install .
```

### Usage

##### Running Crawls
* Before starting the crawls, recheck the config options in scrapyd_config (`scrapyd.conf`) file. Documentation to better understand these options can be found [here](https://scrapyd.readthedocs.io/en/stable/config.html).
The default configration we have set will use the number of cpus available in the system multiplied by the value in `max_proc_per_cpu`.

* First, create a log directory where all the logs will be dumped. Next, start the scrapyd server from project directory and deploy the spiders:

  ```bash
  # current directory is webcorpus
  mkdir logs
  # We need to start the scrapyd service, that listens to requests for spiders to run and spawns a process for each one.
  # since this needs to run in the backgroud, start the next command in a screen or tmux session
  sudo scrapyd
  ```
  After starting the scrapyd service, run this command to [deploy your project](https://github.com/scrapy/scrapyd-client#scrapyd-deploy) to a Scrapyd server:
  ```bash
  scrapyd-deploy
  ```

* Start a crawl

  ```bash
  # all paths must be absolute paths
  curl http://localhost/schedule.json -d project=webcorpus -d spider=recursive-spider -d html_path=<html_path> -d source_name=<source_name> -d home_url=<home_url> -d lang=<iso code> -d log_path=<path_to_webcorpus>/logs
  
  ```
For example, if you want to crawl tamil bbc news website:
```
curl http://localhost/schedule.json \
-d project=webcorpus \
-d spider=recursive-spider \
-d html_path=/home/username/ta/bbc \
-d source_name=bbc \
-d home_url=https://www.bbc.com/tamil \
-d lang=ta \
-d log_path=/home/username/webcorpus/logs
```
In the above command, `https://www.bbc.com/tamil` will be the base url that we use to start crawling and crawler fetches all the urls inside this base url to continue crawling. To avoid advertisements, redirects to other websites, etc, **We only crawl websites of the form `<base url>/route`. Hence this base url is very important**

The crawls (html files) will be saved in the folder `html_path` and will be used for further processing later.

To generate all the crawl commands from a csv or text file containing all the sources:
```
python get_crawl_commands.py -f <sources txt/csv file> -lp <webcorpus logs folder> -of <output folder>

Args:
 -quiet, --q           Quiet mode
  -f FILE, --file FILE  Text/CSV file containing the urls to crawl
  -lp LOG_PATH, --log_path LOG_PATH
                        Path to webcorpus logs folder
  -of OUTPUT_FOLDER, --output_folder OUTPUT_FOLDER
                        Output folder for saving crawls. The crawls would be
                        saved in {output_folder}/{lang_code} (lang_code is inferred from the text/csv file name)
```

example command:
```bash
python get_crawl_commands.py -f "sources/as.csv" -lp "webcorpus/logs" -of "crawling_outputs"
```


* Monitor crawls: You can monitor the jobs at the dashboard available at `http://<ip address>`. If using GCP, make sure to enable HTTP traffic on your VM. 


![image](https://user-images.githubusercontent.com/9641196/142577587-a92a1426-5d87-499d-8618-a1f47c0dbcfd.png)

^This is the screenshot of the landing page. Clicking on `jobs` button will show you the status of all the pending (in queue), running and finished crawls:


![image](https://user-images.githubusercontent.com/9641196/142577798-d4c02dd7-1931-45a4-beeb-db29572a9979.png)

^ Clicking on the logs button will show more statitics like crawling speed, the route that is currently being crawled, any error that caused the crawling to stop, etc.



##### Processing corpus

Once crawling is complete, We can process the html pages to extract articles, sentences or genres (uses the url route to infer genre, for instance sentences from `https://www.bbc.com/sport` are grouped in sports genre) of each website.


  ```bash
  # all paths must be absolute paths
  python3 scripts/process.py --operation <operation code> --lang <lang code> --input <input path> --output <output path>
  ```
* Processing operations supported: `extract_arts`, `extract_sents`, `extract_genres`

For example, to extract articles for all the html sources inside `/home/username/ta` folder (assuming ta folder contains all the tamil html crawls), you should run the following command to save the processed articles in `/home/username/ta_arts`:
```bash
python3 scripts/process.py --operation extract_arts --lang ta --input /home/username/ta --output /home/username/ta_arts
```
The `lang` tag is used to filter articles that are in different scripts (lang="hi" will ignore articles that have non-devnagiri characters beyond a certain threshold).
After running the above command, `/home/username/ta_arts/<source>/<articleid>` would a json file with following information:
```
{
    "title": <article title>,
    "body":<artcile body>,
    "source": <name of the source>,
    "url": <base url/route>,
    "timestamp": <timestamp>
}
```
This json metadata format is similar to popular monoligual datasets like `C4` (see some samples [here](https://huggingface.co/datasets/allenai/c4/tree/main/realnewslike) ).

To convert the above processed tamil articles to sentences, use the following command:
```bash
python3 scripts/process.py --operation extract_sents --lang ta --input /home/username/ta_arts --output /home/username/sents/ta.txt
```
This will create `/home/username/sents/ta.txt` that has tamil sentences (one per line) from all the processed articles.

**Based on your tasks, users may add language-identification, removing offensive text or any other forms of cleaning before using the final corpus**

### Features

* supports crawling and processing of 17 Indian languages
* designed to run in distributed fashion




### Similar Projects

* [news-please](https://github.com/fhamborg/news-please)
* [newspaper3k](https://github.com/codelucas/newspaper)
* [lazynlp](https://github.com/chiphuyen/lazynlp)



