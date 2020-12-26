from NeuralNetwork import ActivationFunction, NeuralNetwork
import math

#
# Basic Usage
#

# NeuralNetwork( input_nodes = 1 (default), hidden_nodes = 1 (default), output_nodes = 1 (default)  )
my_nn = NeuralNetwork(2, 4, 2)

# train( values, expected_output, [debug(optional)] = False (default) )
# Types: arrays, tuples, lists
my_nn.train([1,2,3], [2,3,4]) # -> returns the Neural Network (able to chain methods (train().train().train() .....))

# predict( input )
# Types: arrays, tuples, lists
my_nn.predict([1,2,3]) # -> returns list of outputs




#
# Extra Control
#

# set_learning_rate( rate = 0.1 (default) )
# Changes the learning rate (do not use high values, this will make training very hard) Lower is better but it's slower
my_nn.set_learning_rate(0.01)

# ActivationFunction( Equation, Derivative )
# Creating your own activation function
ArcTan = ActivationFunction( lambda x: math.tan(x)**-1, lambda x: 1 / (x**2 + 1) )

# Built-In:
#     ActivationFunction.sigmoid    - most used
#     ActivationFunction.tanh       - can also be used


# set_activation_function ( ActivationFunction = sigmoid (default) )
my_nn.set_activation_function(ArcTan)





#
# Serialize & Deserialize
#


# Serialize (convert Neural Network to JSON and write to file)
with open('my_nn.json', 'w') as File:
    File.write(my_nn.serialize())

# Deserialize (read from file and convert from JSON to class)
with open('my_nn.json', 'r') as File:
    my_nn = NeuralNetwork.deserialize(File.read())

