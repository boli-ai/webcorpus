## Corpora

Corpora is language-agnostic web crawler and a corpora processor tool specifically designed for Indian languages.


#### Setup

Clone the repository and run the following command:
```bash
pip3 install .
```



#### Usage

* Re-compile the list of news sources:

  ```
  corpora fetch-sources
  ```

* Scrape news sources and build raw dataset:

  ```bash
  corpora fetch-news --lang <langcode> [--srange a,b]
  ```

* Process a raw dataset:

  ```bash
  corpora process-news --corpuspath <path> --lang <langcode>
  ```


#### Performance

* Crawls around 0.5 GB of raw data / day for 10 sources.
* To achieve better efficiency, run multiple instances of crawlers on different machines, each operating on a different set of sources.
* Need around 5GB of raw data for 100M tokens



#### Datasets

| Language | # News Articles | # Lines | # Tokens  | # Unique Tokens | Link |
| -------- | --------------- | ------- | --------- | --------------- | ---- |
| Kannada  |  |  | 94M |          |      |

