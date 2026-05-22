# Machine Learning

For machine learning the main files are:

- `machine_learning/roboflow_model/PokemonGenOneModel.ipynb` — The Jupyter notebook that we used to train our roboflow yolo model
- `machine_learning/plotting.ipynb` — We used a jupyter notebook file at first to see clustering and easily change variables
- `python/streamlit/functions/ClusterFunctions.py` - 
This file contains the functions we use to show the clusters and other graphs we show on our streamlit frontend
- `python/streamlit/functions/model_predict.py` - 
The function our frontend uses when we upload a picture. It uses our trained model to return what pokemon picture has been uploaded.


### Our model, training params and training data
The params we used to train our model
![alt text](readme_images/image-2.png)

Our top1 and top5 accuracy
![alt text](readme_images/image-5.png)


We can see that our model got increasingly more accurate the more epochs it ran
![alt text](readme_images/image-4.png)


### clustering

We test k-means to see how many clusters are optimal for our dataset
![alt text](readme_images/image-6.png)
- In our dataset around 3 clusters is ideal

our clustering with 3 clusters. In our webapp it's possible to change how many clusters there are
![alt text](readme_images/image-7.png)

We have included a boxplot using a specific stat which showcases the upper and lower fences and the means of each cluster
![alt text](readme_images/image-8.png)

### Pokemon recogniser 
Our trained model takes a picture and can tell what pokemon is in the picure
Since our model is a classification model it can not tell us all the pokemon in the picture, but tells us what pokemon is has the highest confidence in
![alt text](readme_images/image-9.png)