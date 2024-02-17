"""This module provides different text and image analysis functions for the AdDownloader."""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageStat
import pandas as pd
import os
#from sklearn.cluster import KMeans
#from skimage import color, data
#from skimage.feature import canny, corner_harris, corner_peaks
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

project_name = "test1"
data_path = f"output/{project_name}/ads_data"
data = pd.read_excel(os.path.join(data_path, "original_data.xlsx"))
text_data = data.filter(regex=r'^ad_creative')
text_data.to_excel(f'{data_path}\\text_data.xlsx', index=False)

# text analysis
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('vader_lexicon')

# tokenize and remove stopwords
eng_stop_words = set(stopwords.words('english'))
fr_stop_words = set(stopwords.words('french'))
nl_stop_words = set(stopwords.words('dutch'))

strp = text_data.loc[4, "ad_creative_bodies"].strip("[]")
tokens = [word.lower() for word in word_tokenize(strp) if word.isalnum() and word.lower() not in eng_stop_words]

# calculate word frequencies
fd = nltk.FreqDist(tokens)
#fd.tabulate()
#word_freq = Counter(tokens)
print(f"Most common keywords: {fd.most_common(3)}")

# sentiment
sia = SentimentIntensityAnalyzer()
sia.polarity_scores(strp)



# TOPIC MODELING
# Create a dictionary and a corpus
dictionary = corpora.Dictionary(tokens)
corpus = [dictionary.doc2bow(text) for text in texts]

# Build the LDA model
lda_model = models.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)

# Print the topics and associated words
print("Topics and associated words:")
topics = lda_model.print_topics(num_words=5)
for topic in topics:
    print(topic)









"""
# extract 3 dominant colors of the ad image
def extract_dominant_color(image, num_colors = 3):
    # Resize image to speed up processing
    resized_image = cv2.resize(image, (64, 64), interpolation=cv2.INTER_AREA)

    # Reshape the image to be a list of pixels
    reshaped_image = resized_image.reshape((resized_image.shape[0] * resized_image.shape[1], 3))

    # Find and display the most common colors
    clf = KMeans(n_clusters=num_colors, n_init=10)
    labels = clf.fit_predict(reshaped_image)
    counts = Counter(labels)

    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [f'#{int(c[0]):02x}{int(c[1]):02x}{int(c[2]):02x}' for c in ordered_colors]
    rgb_colors = [tuple(c) for c in ordered_colors]

    # Calculate percentages
    total_pixels = len(reshaped_image)
    color_percentages = [(counts[i] / total_pixels) * 100 for i in counts.keys()]

    #plt.figure(figsize=(8, 6))
    #plt.pie(counts.values(), labels=hex_colors, colors=hex_colors)
    #plt.show()

    return hex_colors, color_percentages

# assess image quality - resolution, brightness, sharpness and contrast
def assess_image_quality(image_path):
    with Image.open(image_path) as img:
        # resolution
        width, height = img.size
        resolution = width * height
        gray_img = img.convert('L')

        # brightness
        brightness = sum(img.getpixel((x, y))[0] for x in range(width) for y in range(height)) / (width * height)

        # sharpness and contrast
        opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY)
        # a higher variance indicates that the image is sharp, with clear edges and details
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

        # contrast indicates the spread of brightness levels across the image
        # a higher std suggests a higher contrast, the image has a wide range of tones from dark to light
        contrast = gray.std()

        return resolution, brightness, contrast, sharpness
    

# analyse an image including all features of interest
def analyse_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # extract dominant colors
    dominant_colors, percentages = extract_dominant_color(image, show_chart=True)
    for col, percentage in zip(dominant_colors, percentages):
        print(f"Color: {col}, Percentage: {percentage:.2f}%")

    resolution, brightness, contrast, sharpness = assess_image_quality(image_path)
    print(f"Resolution: {resolution} pixels, Brightness: {brightness}, Contrast: {contrast}, Sharpness: {sharpness}")

    img = Image.open(image_path)
    img = color.rgb2gray(img)

    # edge detection
    # higher the sigma smoother the image (focus on the outside shape)
    canny_edges = canny(img, sigma=1.8)

    # corners - meh
    measure_image = corner_harris(img)
    coords = corner_peaks(measure_image, min_distance=32, threshold_rel=0.02)
    ncorners = len(coords)
    print("With a min_distance set to 32, we detect a total", len(coords), "corners in the image.")

    numbers = pattern.findall(image_path)
    ad_id = '_'.join(numbers) # extract ad id

    dict = {'ad_id': ad_id, 'dom_colors': dominant_colors, 'dom_colors_prop': percentages, 'resolution': resolution,
            'brightness': brightness, 'contrast': contrast, 'sharpness': sharpness, 'ncorners': ncorners}
    return dict
    
"""
# TODO: add a for loop to analyse a set of images

images_path = f"output\\{project_name}\\ads_images"
images = os.listdir(images_path)
os.path.exists(data_path)
row_list2 = []
#row = analyse_image(image_path)
#row_list2.append(row)

img_results = pd.DataFrame(row_list2)
img_results.to_excel(f'data\\img_features.xlsx', index=False)
