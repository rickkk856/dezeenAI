# dezeenAI
**Search Dezeen.com interior library for specific objects and colours**

*by Adam Siemaszkiewicz*


# Summary

The idea behind this repo is to speed up an interior architect's workflow by allowing to search through the interior image dataset of [Dezeen.com] online architecture magazine. You can either search by a type of object or a colour. Currently, the Dezeen.com's dataset does not provide such feature, so I implemented a object detection and dominant colour recognition algorithms to properly tag the image dataset and allow for a proof-of-concept search engine.

![dezeenAI](https://github.com/adamsiemaszkiewicz/dezeenAI/blob/main/dezeenai.png)

# Scrape and download

Firstly, the notebook crawls all Dezeen.com articles under `Interior` category using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and fetches the information about articles' id, title, url and a list of images within each article. Secondly, it downloads all images and lastly saves a DataFrame of all information gathered.

# Object detection

This notebook builds a dataset of labeled images from [Open Images Dataset v6](https://storage.googleapis.com/openimages/web/index.html). Then, based on [YOLOv4](https://github.com/AlexeyAB/darknet) object detection system, it trains a custom object detection model to recognize 30 interior-architecture-related categories of objects such as: cupboard, drawer, shelf, etc.

# Dominant colours recognition

This notebook builds a KMeans-clustering-based colour recognition system to find a list of 10 dominant colours and their distribution for each picture in the dataset.

# Database building

This notebook runs both object and colour detection algorithms for our image dataset and builds a database containing all gathered data.
