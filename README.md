# dezeenAI
**Search Dezeen.com interior library for specific objects and colours**

*by Adam Siemaszkiewicz*

# [Try the app online!](https://dezeenai.herokuapp.com/)
The proof-of-work version of the search engine is now available on Heroku. Feel free to play with it!

# Summary

The idea behind this repo is to speed up an interior architect's workflow by allowing to search through the interior image dataset of [Dezeen.com](http://dezeen.com/) online architecture magazine. You can either search by a type of object or a colour. Currently, the Dezeen.com's dataset does not provide such feature, so I implemented an object detection and dominant colour recognition algorithms to synthetically tag the image dataset and allow for a proof-of-concept search engine.

![dezeenAI](https://github.com/adamsiemaszkiewicz/dezeenAI/blob/main/dezeenai.png)

# Scrape and download

[Github](https://github.com/adamsiemaszkiewicz/dezeenAI/blob/main/1_ScrapeAndDownload.ipynb) | [Google Colab](https://drive.google.com/file/d/1Q0BQBP0lDJZbMNl7gf-A1YHVS-_BYEp6/view?usp=sharing)

Firstly, the notebook crawls all Dezeen.com articles under `Interior` category using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and fetches the information about articles' id, title, url and a list of images within each article. Secondly, it downloads all images and saves a DataFrame of all information gathered.

# Dominant colours recognition

[Github](https://github.com/adamsiemaszkiewicz/dezeenAI/blob/main/2_DominantColours.ipynb) | [Google Colab](https://drive.google.com/file/d/1RnL1UTHYOc3-l2DUK4YKVSGv3VJaeSVq/view?usp=sharing)

This notebook builds a OpenCV & KMeans-clustering-based colour recognition system to find a list of 10 dominant colours and their distribution for each picture in the dataset.

# Object detection (basic)

[Github](https://github.com/adamsiemaszkiewicz/dezeenAI/blob/main/3_ObjectDetectionBasic.ipynb) | [Google Colab](https://drive.google.com/file/d/1lV6TZ8UKSQDZvJbkYIudHRTG9wx9zyse/view?usp=sharing)

This notebook runs an object recognition system through our image dataset and tags each picture with names of object detected along with a confidence of a detection.

# Object detection (custom)

[Github](https://github.com/adamsiemaszkiewicz/dezeenAI/blob/main/4_ObjectDetectionCustom.ipynb) | [Google Colab](https://drive.google.com/file/d/1um65Ym8zZec4vvusZMWjwG_h77cRtiPm/view?usp=sharing)

This notebook builds a dataset of labeled images from [Open Images Dataset v6](https://storage.googleapis.com/openimages/web/index.html). Then, based on [YOLOv4](https://github.com/AlexeyAB/darknet) object detection system, it trains a custom object detection model to recognize additional 30 interior-architecture-related categories of objects such as: cupboard, drawer, shelf, etc.

# Search engine

[Github](https://github.com/adamsiemaszkiewicz/dezeenAI/blob/main/5_SearchEngine.ipynb) | [Google Colab](https://drive.google.com/file/d/18mZCKfh71fjTZvPkxyP0tedw3YZ--yTX/view?usp=sharing)

This final notebook builds a two-module search engine to check the functionality of the system. After that, the app is deployed using a [Streamlit](https://www.streamlit.io/) library and [Heroku](https://heroku.com/) cloud platform.
