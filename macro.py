import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from dataclasses import dataclass
st.title('Macro Calculator')

st.write('This calculator will help you determine your daily calorie intake based on your activity level and goal.')

def get_user_info():
        age = st.text_input("Enter your age: ", 0)
        weight = st.text_input("Enter your weight: ", 0 )
        height = st.text_input("Enter your height: ",0)
        activity_level = st.selectbox('Enter your activity level: ', ('Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extra Active'))
        sex = st.selectbox('Enter your sex: ', ('Male', 'Female'))
        goal = st.selectbox('Enter your goal: ', ('Lose Weight', 'Maintain Weight', 'Gain Weight'))
        return age, weight, height, activity_level, sex, goal

age, weight, height, activity_level, sex, goal = get_user_info()

@dataclass
class ActivityLevel:
    sedentary: float = 1.2
    lightly_active: float = 1.375
    moderately_active: float = 1.55
    very_active: float = 1.725
    extra_active: float = 1.9

@dataclass
class WeightGoal:
    lose_weight: float = 0.8
    maintain_weight: float = 1
    gain_weight: float = 1.2



class MacroCalculator:

    def __init__(self, age, weight, height, activity_level, sex, goal):
        self.age = age
        self.weight = weight
        self.height = height
        self.activity_level = activity_level
        self.sex = sex
        self.goal = goal
        self.bmr = None
        self.adjusted_bmr = None
        self.calories = None
        self.protein = None
        self.carbs = None
        self.fat = None

    def force_types(self):
        self.age = int(self.age)
        self.weight = int(self.weight)
        self.height = int(self.height)
    
    def set_activity_level(self):
        activity_levels = ActivityLevel()
        if self.activity_level == 'Sedentary':
            self.activity_level = activity_levels.sedentary
        elif self.activity_level == 'Lightly Active':
            self.activity_level = activity_levels.lightly_active
        elif self.activity_level == 'Moderately Active':
            self.activity_level = activity_levels.moderately_active
        elif self.activity_level == 'Very Active':
            self.activity_level = activity_levels.very_active
        elif self.activity_level == 'Extra Active':
            self.activity_level = activity_levels.extra_active

    def set_weight_goal(self):
        weight_goals = WeightGoal()
        if self.goal == 'Lose Weight':
            self.goal = weight_goals.lose_weight
        elif self.goal == 'Maintain Weight':
            self.goal = weight_goals.maintain_weight
        elif self.goal == 'Gain Weight':
            self.goal = weight_goals.gain_weight

    def set_sex(self):
        if self.sex == "Male":
            self.sex = 1
        else:
            self.sex = 0


    def calculate_bmr(self):
        self.bmr = 9.99 * self.weight + 6.25 * self.height - 4.92 * self.age + 166 * self.sex - 161
        self.adjusted_bmr = self.bmr * self.activity_level
        self.calories = self.adjusted_bmr * self.goal

    def calculate_macros(self):
        self.protein = 0.3 * self.calories / 4
        self.carbs = 0.5 * self.calories / 4
        self.fat = 0.2 * self.calories / 9
    
macro = MacroCalculator(age, weight, height, activity_level, sex, goal)
macro.force_types()
macro.set_weight_goal()
macro.set_activity_level()
macro.set_sex()
macro.calculate_bmr()
macro.calculate_macros()











st.write(f"Target calories: ", macro.calories)
st.write(f"Target protein: ", macro.protein)
st.write(f"Target carbs: ", macro.carbs)
st.write(f"Target fat: ", macro.fat)

st.write("This calculator is based on the Mifflin-St Jeor Equation.")
st.write("https://www.sciencedirect.com/science/article/abs/pii/S0002916523166986")



class BMRComparisonPlot:
    def __init__(self, weight_range, height, age):
        self.weight_range = weight_range
        self.height = height
        self.age = age
    
    def calculate_bmr(self, method):
        if method == 'new':
            return 9.99 * self.weight_range + 6.25 * self.height - 4.92 * self.age + 166 * 1 - 161
        elif method == 'harris':
            return 66.473 + (13.7516 * self.weight_range) + (5.0033 * self.height) - (6.755 * self.age)
        else:
            raise ValueError("Invalid BMR calculation method. Choose 'new' or 'harris'.")
    
    def plot(self):
        # Create a new figure object
        fig, ax = plt.subplots()

        new_bmr = self.calculate_bmr('new')
        harris = self.calculate_bmr('harris')

        # Compute the difference between the two lines
        diff = new_bmr - harris

        # Create line plot of weight vs. new_bmr and harris
        sns.lineplot(x=self.weight_range, y=new_bmr, label='Mifflin-St Jeor Equation')
        sns.lineplot(x=self.weight_range, y=harris, label='Harris-Benedict Equation')

        # Add a shaded region to emphasize the distance between the two lines
        ax.fill_between(self.weight_range, new_bmr, harris, where=new_bmr>harris, interpolate=True, alpha=0.2, color='green')
        ax.fill_between(self.weight_range, new_bmr, harris, where=new_bmr<harris, interpolate=True, alpha=0.2, color='red')

        # Set labels and title
        ax.set_xlabel("Weight (kg)")
        ax.set_ylabel("BMR (kcal)")
        ax.set_title("Comparison of BMR Calculation Methods")

    # Display the plot in Streamlit using st.pyplot()
        st.pyplot(fig)

bmrplot = BMRComparisonPlot(np.arange(40, 100), 184, 27)
bmrplot.calculate_bmr('new')
bmrplot.plot()
