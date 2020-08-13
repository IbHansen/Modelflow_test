#!/usr/bin/env python
# coding: utf-8

# # Modelling spreading of infectious diseases
# This is an experimental model made in a few hours. Inspirered by https://triplebyte.com/blog/modeling-infectious-diseases. 
# 
# The model is purely for testing the capabilities of ModelFlow, the parameters selected are for ilustration of the dynamic and are not actual estimates. 
# 
# This is a Jupyter Notebook running Python. 
# 
# The notebook is located on github here: https://github.com/IbHansen/Modelflow_test
# 
# Feel free to use this notebook. 
# 
# THE Notebook IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# **To run the model** select **cell>run all** in the menu
# 
# Then press the run button in the user interaction section in the end of the notebook 
# 
# Use the sliders to change the input parameters
# 

# ## Import some stuff

# In[14]:


import pandas as pd
#from ipywidgets import interact,Dropdown,Checkbox,Layout,FloatSlider

from modelsandbox      import create_new_model
from modelmanipulation import explode
from modeljupyter      import inputwidget


# ##  Specify Model
# The model is specified as equations. The equations defines the daily transition between the states:
# 
#  - susciptible
#  - exposed
#  - infectious
#  - recovered
#  - dead 
#  
# Some conventions:
#  - (-1) after a variable means the value the day before.
#  - diff means the change in variable from the day before

# In[15]:


rcorona = '''             infection_rate        = min(rate_contact * probability_transmision * infectious(-1) / population(-1),1.0) 
             new_exposed           = infection_rate * susceptible
             diff(exposed)         = new_exposed - new_infectious + exo_exposed

             new_infectious        = incubation_rate * exposed 
             diff(infectious)      = new_infectious - new_recovered  - new_dead

             diff(susceptible)     = -new_exposed  

             new_recovered         = recovery_rate * infectious(-1)
             diff(recovered)       = new_recovered 
             
             new_dead              = dead_rate * infectious(-1)
             diff(dead)            = new_dead 
             diff(population)      = -diff(dead)             
'''
mcorona = create_new_model(rcorona) # create a model instance which can solve the model 


# ## Define an initial scenario 
# Now a tabel for the data is created.
# The tabel is implemented as a Pandas Dataframe. 
# 
# You don't have to understand the python code below. 

# In[16]:


DAYS = 500
basedf = pd.DataFrame(index=range(DAYS))       # make an empty dataframe with DAYS rows
basedf.index.name = 'Day'


# ## Make eksperiments 
# Now you can make your own experiment. Use the sliders to define an experiment. Then press the run button. The model will solve, and the results can be inspected.
# 
# Press the Run button to run an experiment. Inspect the results in the tabs. 
# 
# Adjust the parameters, try to increase *Daily rate of contact* to 6.
# 
# Then press run and watch how the values changes.
# 
# Again, you don't have to understand the Python code just press run. 

# In[17]:


cow = inputwidget(mcorona,basedf,modelopt={'silent':0,'antal':1000,'first_test':10},
                  slidedef = {
                     'Population            '     :{'var' : 'POPULATION SUSCEPTIBLE', 'min' : 0.0, 'max' : 10_000_000, 'value' : 1_000_000,'step':100_000,'op':'=start-','dec':0},
                     'Number of infected t=1'     :{'var' : 'EXO_EXPOSED',            'min' : 0.0, 'max' : 1000,       'value' : 300,      'step':10,'op':'=impulse','dec':0},
                     'Daily incubation rate'      :{'var' : 'INCUBATION_RATE',        'min' : 0.0, 'max' : 1.0,        'value' : 0.1,                'op':'='},
                     'Daily death rate'           :{'var' : 'DEAD_RATE',              'min' : 0.0, 'max' : 1.0,        'value' : 0.01,               'op':'=' },
                     'Daily recovery rate'        :{'var' : 'RECOVERY_RATE',          'min' : 0.0, 'max' : 1.0,        'value' : 0.1,                'op':'='},
                     'Daily rate of contact'      :{'var' : 'RATE_CONTACT',           'min' : 0.0, 'max' : 30,         'value' : 4,'step':1,         'op':'='},
                     'Probability of transmission':{'var' : 'PROBABILITY_TRANSMISION','min' : 0.0, 'max' : 1.0,        'value' : 0.05,'step':0.005,  'op':'=','dec':3},
                             },
                 varpat='infectious recovered dead new_infectious new_recovered new_dead')

