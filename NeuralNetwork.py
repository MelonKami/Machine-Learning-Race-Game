import math, random, json
from matrix import Matrix

class ActivationFunction:
    sigmoid = None
    tanh = None
    def __init__(self, func, dFunc):
        self.func = func
        self.dFunc = dFunc
ActivationFunction.sigmoid = ActivationFunction((lambda x : 1/math.exp(-x)), (lambda y : y * (1-y)))
ActivationFunction.tanh = ActivationFunction((lambda x : math.tanh(x)), (lambda y : 1 - (y*y)))    



class NeuralNetwork:
    def __init__(self, in_nodes_or_nn=1, hid_nodes=1, out_nodes=1):
        self.hash = "%032x" % random.getrandbits(128)
        if type(in_nodes_or_nn) is NeuralNetwork:
            a = in_nodes_or_nn
            self.input_nodes = a.input_nodes
            self.hidden_nodes = a.hidden_nodes
            self.output_nodes = a.output_nodes

            self.weights_ih = a.weights_ih.copy()
            self.weights_ho = a.weights_ho.copy()

            self.bias_h = a.bias_h.copy()
            self.bias_o = a.bias_o.copy()
            

            self.activation_function = in_nodes_or_nn.activation_function
            self.learning_rate = in_nodes_or_nn.learning_rate

        elif type(in_nodes_or_nn) is int and type(hid_nodes) is int and type(out_nodes) is int:
            self.input_nodes = in_nodes_or_nn
            self.hidden_nodes = hid_nodes
            self.output_nodes = out_nodes

            self.weights_ih = Matrix(self.hidden_nodes, self.input_nodes)
            self.weights_ho = Matrix(self.output_nodes, self.hidden_nodes)
            self.weights_ih.randomize()
            self.weights_ho.randomize()

            self.bias_h = Matrix(self.hidden_nodes, 1)
            self.bias_o = Matrix(self.output_nodes, 1)
            self.bias_h.randomize()
            self.bias_o.randomize()
            
            self.set_learning_rate()
            self.set_activation_function()
        else:
            raise Exception('Failed to create Neural Network constructor arguments must be type <int> or type <NeuralNetwork>')

        
        return self

    def set_learning_rate(self,rate = 0.1):
        if type(rate) != float or type(rate) != int:
            raise Exception('Rate must be a number not: ' + str(type(rate)))
        self.learning_rate = rate
        return self

    def set_activation_function(self, func = ActivationFunction.sigmoid):
        if type(func) != ActivationFunction:
            raise Exception('Func must be a type of ActivationFunction not: ' + str(type(func)))
        self.activation_function = func
        return self

    def predict(self, input_data = []):
        if type(input_data) != list or type(input_data) != tuple:
            raise Exception('Input Data must be an array/list/tuple of input values not: ' + str(type(input_data)))
        inputs = Matrix.from_array(input_data)
        hidden = Matrix.multiply(self.weights_ih, inputs)
        hidden.add(self.bias_h)

        hidden.map(self.activation_function.func)

        output = Matrix.multiply(self.weights_ho, hidden)
        output.add(self.bias_o)
        output.map(self.activation_function.func)

        return output.to_array()


    def train(self, input_array, target_array, debug = False):
        inputs = Matrix.fromArray(input_array)
        hidden = Matrix.multiply(self.weights_ih, inputs)
        hidden.add(self.bias_h)

        hidden.map(self.activation_function.func)

        outputs = Matrix.multiply(self.weights_ho, hidden)
        outputs.add(self.bias_o)
        outputs.map(self.activation_function.func)

        targets = Matrix.fromArray(target_array)

        output_errors = Matrix.subtract(targets, outputs)

        gradients = Matrix.map(outputs, self.activation_function.dfunc)
        gradients.multiply(output_errors)
        gradients.multiply(self.learning_rate)


        hidden_T = Matrix.transpose(hidden)
        weight_ho_deltas = Matrix.multiply(gradients, hidden_T)

        self.weights_ho.add(weight_ho_deltas)
        self.bias_o.add(gradients)

        who_t = Matrix.transpose(self.weights_ho)
        hidden_errors = Matrix.multiply(who_t, output_errors)

        hidden_gradient = Matrix.map(hidden, self.activation_function.dfunc)
        hidden_gradient.multiply(hidden_errors)
        hidden_gradient.multiply(self.learning_rate)

        inputs_T = Matrix.transpose(inputs)
        weight_ih_deltas = Matrix.multiply(hidden_gradient, inputs_T)

        self.weights_ih.add(weight_ih_deltas)
        self.bias_h.add(hidden_gradient)

        if debug:
            print('Output:')
            outputs.print()
            print('')
            print('')
            print('Error (difference from target):')
            output_errors.print()
            print('')
            print('')
        return self

    def serialize(self):
        oObj = {
            "input_nodes":self.input_nodes,
            "hidden_nodes":self.hidden_nodes,
            "output_nodes":self.output_nodes,
            "weights_ih":self.weights_ih,
            "weights_ho":self.weights_ho,
            "bias_h":self.bias_h,
            "bias_o":self.bias_o,
            "learning_rate":self.learning_rate
        }
        return json.dumps(oObj)

    @staticmethod
    def deserialize(data):
        if type(data) != str:
            raise Exception('You can only deserialize with a json-string')
        _data = json.loads(data)
        nn = NeuralNetwork(_data['input_nodes'], _data['hidden_nodes'], _data['output_nodes'])
        nn.weights_ih = Matrix.deserialize(_data['weights_ih'])
        nn.weights_ho = Matrix.deserialize(_data['weights_ho'])
        nn.bias_h = Matrix.deserialize(_data['bias_h'])
        nn.bias_o = Matrix.deserialize(_data['bias_o'])
        nn.learning_rate = _data['learning_rate']
        return nn

    def copy(self):
        return NeuralNetwork(self)

    def mutate(self, func):
        self.weights_ih.map(func)
        self.weights_ho.map(func)
        self.bias_h.map(func)
        self.bias_o.map(func)
    
    


