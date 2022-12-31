import pickle
import matplotlib.pyplot as plt

####################################################
############# Variable to change ###################
####################################################
# enter the file you want to open with pickle. You may need the file path
file_to_open = 'Pickle_Graphs_2022/sep_dm_seeing full(lim 2)_2022.pickle'
# file_to_open = 'sep one to one resres_one.pickle'

####################################################
############# End of variables #####################
####################################################

# code to open .pickle file
file = open(file_to_open, 'rb')  # opens the .pickle files
figx = pickle.load(file)  # makes a figure
file.close()
plt.show()  # shows the figure
figx.show()
