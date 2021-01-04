# import essential libraries
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import SessionState

# don't truncate long values
pd.set_option('display.max_colwidth', None)

# Use the full page instead of a narrow central column
st.set_page_config(layout='wide')

#
# LOAD DATAFRAMES
#

articles_df = pd.read_csv('files/df_articles.csv', index_col=0)
colors_df = pd.read_pickle('files/df_images-colours.pkl')
objects_df = pd.read_csv('files/images_objectsbasic.csv', index_col=0)

#
# CONVERT HEX TO RGB
#

def hex2rgb(color):
    h = color.lstrip('#')
    color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return color

#
# LIST OF CLASSES
#

classes = [
           'dog',
           'person',
           'bicycle',
           'car',
           'bench',
           'cat',
           'sports ball',
           'skateboard',
           'bottle',
           'wine glass',
           'cup',
           'fork',
           'knife',
           'spoon',
           'bowl',
           'chair',
           'sofa',
           'pottedplant',
           'bed',
           'diningtable',
           'toilet',
           'tvmonitor',
           'laptop',
           'keyboard',
           'microwave',
           'oven',
           'sink',
           'refrigerator',
           'book',
           'clock',
           'vase',
           ]

#
# SIDEBAR
#

st.sidebar.header('What are you looking for?')
search_type = st.sidebar.selectbox('',['Choose one...','colors', 'objects'])

# color recognition controls
if search_type == 'colors':
    st.sidebar.header('Which color are you looking for?')
    selected_color = st.sidebar.color_picker('', '#F9BB2A', key='selected')
    selected_color = hex2rgb(selected_color)

# object recognition controls
if search_type == 'objects':
    st.sidebar.header('Which object are you looking for?')
    selected_class = st.sidebar.selectbox('', classes)
    st.sidebar.header('What is relevant to you?')
    sort_type = st.sidebar.radio('', ['confidence', 'quantity'])

# search image grid control
st.sidebar.header('Customize the search results')
number_of_columns = st.sidebar.slider('Columns', min_value=1, max_value=5, value=3, step=1)
number_of_elements = st.sidebar.slider('Elements per page', min_value=1, max_value=24, value=12, step=1)

# implement per-session persistent state for pagination
ss = SessionState.get(page_number=0)

# pagination
st.sidebar.header('Looking for more?')
prev = st.sidebar.button('Previous page')
next = st.sidebar.button('Next page')

# increment pagination
if prev and ss.page_number > 0:
    ss.page_number -= 1
elif next:
    ss.page_number += 1

#
# HEADER AREA
#

st.title('DezeenAI - Color & object search engine')
st.header('''This app lets you search interior projects on Dezeen.com based on colors or objects in the pictures.''')
st.subheader('[DezeenAI GitHub repository](https://github.com/adamsiemaszkiewicz/dezeenAI)')

#
# COLOR RECOGNITION FUNCTIONS
#

def rgb2hsv(color):

  '''
  Takes a color in RGB format and converts it HSV format.

  Parameters:
  color (list): Color in the RGB format as a list of R, G, B values

  Returns:
  A converted color in HSV format.
  '''

  r, g, b = color[0]/255.0, color[1]/255.0, color[2]/255.0
  mx = max(r, g, b)
  mn = min(r, g, b)
  df = mx-mn
  if mx == mn:
    h = 0
  elif mx == r:
    h = (60 * ((g-b)/df) + 360) % 360
  elif mx == g:
    h = (60 * ((b-r)/df) + 120) % 360
  elif mx == b:
    h = (60 * ((r-g)/df) + 240) % 360
  if mx == 0:
    s = 0
  else:
    s = (df/mx)*100

  v = mx*100
  color = [h, s, v]
  return color

def closestColor(reference_color, list_of_colors):

  '''
  Takes a reference color and finds a closest color withing a given color list.

  Parameters:
  reference_color (list): Reference color in a RGB format
  list_of_colors (list): List of colors in a RGB format

  Returns:
  A color within a list the closest to the reference color and distance between them.
  '''

  # initiate the distance to be a really big number and closest_color as empty
  shortest_distance, closest_color = sys.maxsize, None

  # check if the color container is not NaN
  if isinstance(list_of_colors, np.ndarray):

    # iterate through all the colors
    for color in list_of_colors:
      # calculate the Euclidean distance to the reference color (sum of squared distances of each value)
      current_distance = pow(rgb2hsv(color)[0] - rgb2hsv(reference_color)[0], 2) + \
                         pow(rgb2hsv(color)[1] - rgb2hsv(reference_color)[1], 2) + \
                         pow(rgb2hsv(color)[2] - rgb2hsv(reference_color)[2], 2)


      # update the distance along with the corresponding color
      if current_distance < shortest_distance:
        shortest_distance = current_distance
        closest_color = color

  return closest_color, shortest_distance

@st.cache(show_spinner=False) # cache this function for better performance

def SortColors(color):
    '''
    Takes the colors_df DataFrame, finds the color distance between the selected
    color and the color palette of the picture and sorts the DataFrame accordingly.
    '''
    # find color distance for each image in the dataset and sort the DataFrame
    colors_df_search = colors_df.copy()
    colors_df_search['distance'] = colors_df.apply(lambda x: closestColor(color, x.loc['colours'])[1], axis=1)
    colors_df_search.sort_values(['distance'], inplace=True)

    return colors_df_search

def ColorGrid(ref_col, elements, columns, page_number=0):

  '''
  Takes the color, finds pictures containing it and outputs search results as a image grid.

  Parameters:
  ref_col (list): Color in RGB formatting
  output (tuple of integers): size of the image grid (rows, columns)

  Returns:
  An image grid with color search results
  '''

  st.write(f'''---
  ## Search results (page {page_number+1})''')

  # sort DataFrame
  df = SortColors(ref_col)

  # fetch lists of image paths and article ids for search results
  offset = page_number*elements
  urls = df['url'][offset:offset+elements]
  ids = df['id'][offset:offset+elements]

  # calculate number of rows to generate
  if elements % columns == 0:
	  rows = int(elements/columns)
  else:
	  rows = int(elements/columns) + 1

  # fill cells with search results
  cols = st.beta_columns(columns)

  for r in range(rows):
	  for c in range(columns):
		  ordinal = r*columns+c
		  if ordinal < elements:
			  img = urls.iloc[ordinal]
			  id = ids.iloc[ordinal]
			  title = articles_df[articles_df['id'] == id]['title'].to_string(index=False)
			  hyperlink = articles_df[articles_df['id'] == id]['url'].to_string(index=False)
			  cols[c].subheader(title)
			  cols[c].write(f'[Read article...]({hyperlink})')
			  cols[c].image(img, use_column_width=True)
			  cols[c].markdown('---')

def ObjectGrid(class_name, sort, elements, columns, page_number=0):

  '''
  Takes the class name to find together with search parameters and outputs
  search results as a images grid.

  Parameters:
  class_name (str): Name of the class to find
  sort (str): sorting method
    `quantity` sort according to quantity of objects found (default)
    `confidence` sort according to find confidence
  output (tuple of integers): size of the image grid (rows, columns)

  Returns:
  An image grid with object search results
  '''

  st.write(f'''---
  ## Search results (page {page_number+1})''')

  # sort according to specified method
  if sort == 'quantity':
    df_search = objects_df.sort_values([class_name, class_name+'_conf'], ascending=False)
  elif sort == 'confidence':
    df_search = objects_df.sort_values([class_name+'_conf'], ascending=False)

  # fetch lists of image paths and article ids for search results
  offset = page_number*elements
  urls = df_search['url'][offset:offset+elements]
  ids = df_search['id'][offset:offset+elements]

  if elements % columns == 0:
	  rows = int(elements/columns)
  else:
	  rows = int(elements/columns) + 1

  # fill cells with search results
  cols = st.beta_columns(columns)

  for r in range(rows):
	  for c in range(columns):
		  ordinal = r*columns+c
          # my_bar = st.progress(ordinal)
		  if ordinal < elements:
			  img = urls.iloc[ordinal]
			  id = ids.iloc[ordinal]
			  title = articles_df[articles_df['id'] == id]['title'].to_string(index=False)
			  hyperlink = articles_df[articles_df['id'] == id]['url'].to_string(index=False)
			  cols[c].subheader(title)
			  cols[c].write(f'[Read article...]({hyperlink})')
			  cols[c].image(img, use_column_width=True)
			  cols[c].markdown('---')

#
# DISPLAY SEARCH RESULTS
#

with st.spinner('Please wait. Loading search results...'):
    if search_type == 'colors':
        ColorGrid(selected_color, number_of_elements, number_of_columns, ss.page_number)
    elif search_type == 'objects':
        ObjectGrid(selected_class, sort_type, number_of_elements, number_of_columns, ss.page_number)
    elif search_type == 'Choose one...':
        st.info('Please specify your search criteria in the left sidebar.')
