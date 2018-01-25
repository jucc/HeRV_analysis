# HeRV_analysis

Exploratory analysis that aims to identify what information can be extracted from HRV, starting with an individual's current activity. Data is originally collected by an android app (https://github.com/jucc/HeRV_app.git).

## HeRV_Pipeline.ipynb 
reads the activity and RR interval files and consolidates them into one large excel file for analysis. Allows configuration of parameters such as fragment length and slice to be cropped from the beginning of each session for stabilization.

## HeRV_Analysis_xxx.ipynb 
some analysis I actuallly ran through the course of this project. Mostly uses classifiers, such as SVM and random forests.
