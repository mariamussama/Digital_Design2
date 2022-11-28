# importing the required module
import matplotlib.animation as plt
 
# x axis values
x = [1,2,3]
# corresponding y axis values
y = [2,4,1]
 
# plotting the points
plt.plot(x, y)
 
# naming the x axis
plt.xlabel('Wire Length')
# naming the y axis
plt.ylabel('Temperature')
 
# giving a title to my graph
plt.title('Wire Length vs Temperature')
 
# function to show the plot
plt.show()