# NC-MCM-Visualizer 

## A toolbox to visualize neuronal imaging data and apply the NC-MCM framework to it

This is a toolbox uses neuronal & behavioral data and visualizes it. The main functionalities include: 
* creating different diagnostic plots and fitting a models on the data
* clustering datapoints into cognitive clusters using behavioral probability trajectories 
* testing and plotting probability of the cognitive sequence being a markov process of 1st order
* creating 3D visualizations using different sklearn dimensionality reduction algorithms as mappings
* the possibility to create a neural manifold using custom BunDLeNet's or any other mapping added
* creating movies and plots of behavioral/neuronal trajectories using the 3D mapping

### These are some of the plots created from calcium imaging data of C. elegans
#### Interactive behavioral state diagram for worm 3 and 3 cognitive states (saved as a .html file)
<img src="ncmcm/data/plots/Demonstration/InteractivePlot.png" width="700" alt="Behavioral State Diagram for Worm 3 and 3 cognitive states - interactive">

#### Comparison of predicted and true label using BunDLeNet's tau model as mapping and its predictor on worm 3
<img src="ncmcm/data/plots/Demonstration/ComaprisonBunDLeNet.png" width="700" alt="Comparison between true and predicted label using BunDLeNet as mapping and predictor">

#### Movie using BunDLeNet's tau model as mapping on worm 1
<img src="ncmcm/data/plots/Demonstration/Worm_1_Interval_100.gif" width="700" alt="Movie using BunDLeNet's tau model as mapping and the true labels">

## Installation and usage information (for end-users)
- pip install ncmcm
-
## Installation and usage information (for contributors)