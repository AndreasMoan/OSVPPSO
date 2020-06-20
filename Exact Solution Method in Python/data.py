# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:01:49 2019

@author: andrebmo
"""
import math

# =============================== DATA ===============================

# ---------------------------- SingleParameters ----------------------------

fuel_price = 0.2755 #Dollars per kg

max_speed = 14

min_speed = 7

fuel_consumption_DP = 170 #kg

fuel_consumption_idling = 120 #kg

spotHourRate = 608

time_spent_per_demand_unit = 0.1

# ---------------------------- Precision ----------------------------

number_of_time_periods_per_hour = 4


# ---------------------------- Installations ----------------------------

class Installation:
    def __init__(self, name, opening_hour, closing_hour, number):
        self.name = name
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
        self.number = number

installations = []

installations.append(Installation("DEP", 0,24, 0))
installations.append(Installation("TRO", 7,19, 1))
installations.append(Installation("TRB", 7,19, 2))
installations.append(Installation("TRC", 7,19, 3))
installations.append(Installation("CPR", 0,24, 4))
installations.append(Installation("SEN", 0,24, 5))
installations.append(Installation("SDO", 0,24, 6))
installations.append(Installation("SEQ", 0,24, 7))
installations.append(Installation("OSE", 0,24, 8))
installations.append(Installation("OSB", 0,24, 9))
installations.append(Installation("OSC", 0,24, 10))
installations.append(Installation("OSO", 0,24, 11))
installations.append(Installation("SSC", 0,24, 12))
installations.append(Installation("OSS", 0,24, 13))
installations.append(Installation("DSD", 0,24, 14))
installations.append(Installation("KVB", 0,24, 15))
installations.append(Installation("VMO", 0,24, 16))
installations.append(Installation("WEL", 0,24, 17))
installations.append(Installation("VFB", 0,24, 18))
installations.append(Installation("WEP", 0,24, 19))
installations.append(Installation("HUL", 0,24, 20))
installations.append(Installation("STA", 7,19, 21))
installations.append(Installation("STB", 0,24, 22))
installations.append(Installation("STC", 0,24, 23))
installations.append(Installation("GFA", 0,24, 24))
installations.append(Installation("GFB", 0,24, 25))
installations.append(Installation("GFC", 0,24, 26))
installations.append(Installation("SOD", 0,24, 27))

installation_numbers = []

for installation in installations:
    installation_numbers.append(installation.number)


#InstNames = ['TRO', 'TRB', 'TRC', 'CPR', 'SEN', 'SDO', 'SEQ', 'OSE', 'OSB', 'OSC', 'OSO', 'SSC', 'OSS', 'DSD', 'KVB', 'VMO', 'WEL', 'VFB', 'WEP', 'HUL', 'STA', 'STB', 'STC', 'GFA', 'GFB', 'GFC', 'SOD']

#         ____________________________________
#        | Installations settings:            |
#        |------------------------------------|
#        | 0 - Clustering of installations    |
#        | 1 - Evenly spread of installations |
#        | 2 - Random enumeration             |
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#Insts_sequence_0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
#Insts_sequence_1 = [0, 1, 24, 8, 18, 3, 21, 14, 27, 20, 4, 15, 2, 13, 25, 22, 10, 6, 23, 11, 5, 26, 7, 9, 12, 16, 17, 19]
#Insts_sequence_2 = [0, 9, 16, 18, 3, 5, 23, 13, 11, 15, 25, 12, 21, 8, 24, 26, 6, 27, 4, 22, 20, 2, 10, 17, 1, 14, 7, 19]


Distance =  [[0.00, 43.47, 47.25, 43.76, 44.47, 44.65, 43.21, 41.73, 71.65, 71.65, 70.54, 64.49, 64.49, 75.08, 89.05, 76.84, 81.18, 81.18, 64.88, 71.58, 71.58, 97.52, 97.69, 96.75, 87.12, 86.97, 85.01, 37.67],
              [43.47, 0.00, 10.14, 14.85, 6.83, 19.08, 12.96, 15.09, 28.27, 28.27, 28.11, 23.53, 23.53, 31.64, 46.71, 44.07, 47.01, 47.01, 25.81, 33.86, 33.86, 65.74, 64.90, 65.90, 55.13, 55.70, 54.09, 15.85],
              [47.25, 10.14, 0.00, 7.23, 3.70, 11.07, 5.96, 8.76, 26.56, 26.56, 23.78, 17.26, 17.26, 31.44, 48.84, 34.32, 37.58, 37.58, 17.91, 25.37, 25.37, 56.04, 55.36, 56.08, 45.38, 45.86, 44.19, 11.98],
              [43.76, 14.85, 7.23, 0.00, 8.42, 4.25, 1.90, 2.13, 33.24, 33.24, 29.62, 22.43, 22.43, 38.37, 56.00, 34.04, 37.99, 37.99, 21.65, 27.85, 27.85, 55.52, 55.24, 55.20, 44.86, 45.04, 43.21, 6.26],
              [44.47, 6.83, 3.70, 8.42, 0.00, 12.65, 6.62, 9.18, 28.05, 28.05, 26.12, 20.13, 20.13, 32.47, 49.18, 38.02, 41.27, 41.27, 21.27, 28.91, 28.91, 59.74, 59.06, 59.76, 49.07, 49.54, 47.86, 11.26],
              [44.65, 19.08, 11.07, 4.25, 12.65, 0.00, 6.12, 4.46, 36.01, 36.01, 31.73, 24.25, 24.25, 41.40, 59.35, 32.27, 36.53, 36.53, 22.62, 27.84, 27.84, 53.38, 53.31, 52.86, 42.80, 42.83, 40.93, 7.36],
              [43.21, 12.96, 5.96, 1.90, 6.62, 6.12, 0.00, 2.81, 32.39, 32.39, 29.15, 22.16, 22.16, 37.37, 54.78, 35.24, 39.06, 39.06, 21.80, 28.39, 28.39, 56.82, 56.46, 56.56, 46.14, 46.38, 44.57, 6.32],
              [41.73, 15.09, 8.76, 2.13, 9.18, 4.46, 2.81, 0.00, 35.11, 35.11, 31.66, 24.52, 24.52, 40.15, 57.59, 35.78, 39.82, 39.82, 23.78, 29.93, 29.93, 57.16, 56.95, 56.76, 46.52, 46.65, 44.79, 4.14],
              [71.65, 28.27, 26.56, 33.24, 28.05, 36.01, 32.39, 35.11, 0.00, 0.00, 7.36, 13.61, 13.61, 6.07, 24.69, 36.68, 36.48, 36.48, 18.15, 22.79, 22.79, 54.28, 52.24, 55.61, 45.50, 46.92, 46.17, 38.54],
              [71.65, 28.27, 26.56, 33.24, 28.05, 36.01, 32.39, 35.11, 0.00, 0.00, 7.36, 13.61, 13.61, 6.07, 24.69, 36.68, 36.48, 36.48, 18.15, 22.79, 22.79, 54.28, 52.24, 55.61, 45.50, 46.92, 46.17, 38.54],
              [70.54, 28.11, 23.78, 29.62, 26.12, 31.73, 29.15, 31.66, 7.36, 7.36, 0.00, 7.64, 7.64, 13.23, 31.52, 29.33, 29.29, 29.29, 11.38, 15.43, 15.43, 47.41, 45.51, 48.62, 38.35, 39.72, 38.90, 35.46],
              [64.49, 23.53, 17.26, 22.43, 20.13, 24.25, 22.16, 24.52, 13.61, 13.61, 7.64, 0.00, 0.00, 19.67, 38.31, 25.54, 26.75, 26.75, 4.95, 12.20, 12.20, 45.65, 44.18, 46.45, 35.74, 36.83, 35.69, 28.46],
              [64.49, 23.53, 17.26, 22.43, 20.13, 24.25, 22.16, 24.52, 13.61, 13.61, 7.64, 0.00, 0.00, 19.67, 38.31, 25.54, 26.75, 26.75, 4.95, 12.20, 12.20, 45.65, 44.18, 46.45, 35.74, 36.83, 35.69, 28.46],
              [75.08, 31.64, 31.44, 38.37, 32.47, 41.40, 37.37, 40.15, 6.07, 6.07, 13.23, 19.67, 19.67, 0.00, 18.65, 42.33, 41.81, 41.81, 24.22, 28.54, 28.54, 59.09, 56.90, 60.58, 50.73, 52.22, 51.58, 43.35],
              [89.05, 46.71, 48.84, 56.00, 49.18, 59.35, 54.78, 57.59, 24.69, 24.69, 31.52, 38.31, 38.31, 18.65, 0.00, 59.62, 58.32, 58.32, 42.77, 46.27, 46.27, 73.96, 71.41, 75.82, 66.83, 68.48, 68.13, 60.40],
              [76.84, 44.07, 34.32, 34.04, 38.02, 32.27, 35.24, 35.78, 36.68, 36.68, 29.33, 25.54, 25.54, 42.33, 59.62, 0.00, 4.99, 4.99, 20.82, 13.93, 13.93, 21.73, 21.22, 21.84, 11.06, 11.69, 10.27, 39.52],
              [81.18, 47.01, 37.58, 37.99, 41.27, 36.53, 39.06, 39.82, 36.48, 36.48, 29.29, 26.75, 26.75, 41.81, 58.32, 4.99, 0.00, 0.00, 22.41, 14.57, 14.57, 19.00, 17.89, 19.71, 9.09, 10.44, 9.83, 43.68],
              [81.18, 47.01, 37.58, 37.99, 41.27, 36.53, 39.06, 39.82, 36.48, 36.48, 29.29, 26.75, 26.75, 41.81, 58.32, 4.99, 0.00, 0.00, 22.41, 14.57, 14.57, 19.00, 17.89, 19.71, 9.09, 10.44, 9.83, 43.68],
              [64.88, 25.81, 17.91, 21.65, 21.27, 22.62, 21.80, 23.78, 18.15, 18.15, 11.38, 4.95, 4.95, 24.22, 42.77, 20.82, 22.41, 22.41, 0.00, 8.19, 8.19, 41.41, 40.12, 42.06, 31.27, 32.27, 31.04, 27.89],
              [71.58, 33.86, 25.37, 27.85, 28.91, 27.84, 28.39, 29.93, 22.79, 22.79, 15.43, 12.20, 12.20, 28.54, 46.27, 13.93, 14.57, 14.57, 8.19, 0.00, 0.00, 33.45, 32.03, 34.27, 23.60, 24.78, 23.76, 34.06],
              [71.58, 33.86, 25.37, 27.85, 28.91, 27.84, 28.39, 29.93, 22.79, 22.79, 15.43, 12.20, 12.20, 28.54, 46.27, 13.93, 14.57, 14.57, 8.19, 0.00, 0.00, 33.45, 32.03, 34.27, 23.60, 24.78, 23.76, 34.06],
              [97.52, 65.74, 56.04, 55.52, 59.74, 53.38, 56.82, 57.16, 54.28, 54.28, 47.41, 45.65, 45.65, 59.09, 73.96, 21.73, 19.00, 19.00, 41.41, 33.45, 33.45, 0.00, 3.13, 2.80, 10.69, 10.56, 12.52, 60.72],
              [97.69, 64.90, 55.36, 55.24, 59.06, 53.31, 56.46, 56.95, 52.24, 52.24, 45.51, 44.18, 44.18, 56.90, 71.41, 21.22, 17.89, 17.89, 40.12, 32.03, 32.03, 3.13, 0.00, 5.88, 10.58, 11.00, 13.03, 60.62],
              [96.75, 65.90, 56.08, 55.20, 59.76, 52.86, 56.56, 56.76, 55.61, 55.61, 48.62, 46.45, 46.45, 60.58, 75.82, 21.84, 19.71, 19.71, 42.06, 34.27, 34.27, 2.80, 5.88, 0.00, 10.84, 10.22, 11.99, 60.22],
              [87.12, 55.13, 45.38, 44.86, 49.07, 42.80, 46.14, 46.52, 45.50, 45.50, 38.35, 35.74, 35.74, 50.73, 66.83, 11.06, 9.09, 9.09, 31.27, 23.60, 23.60, 10.69, 10.58, 10.84, 0.00, 1.89, 3.17, 50.13],
              [86.97, 55.70, 45.86, 45.04, 49.54, 42.83, 46.38, 46.65, 46.92, 46.92, 39.72, 36.83, 36.83, 52.22, 68.48, 11.69, 10.44, 10.44, 32.27, 24.78, 24.78, 10.56, 11.00, 10.22, 1.89, 0.00, 2.03, 50.18],
              [85.01, 54.09, 44.19, 43.21, 47.86, 40.93, 44.57, 44.79, 46.17, 46.17, 38.90, 35.69, 35.69, 51.58, 68.13, 10.27, 9.83, 9.83, 31.04, 23.76, 23.76, 12.52, 13.03, 11.99, 3.17, 2.03, 0.00, 48.28],
              [37.67, 15.85, 11.98, 6.26, 11.26, 7.36, 6.32, 4.14, 38.54, 38.54, 35.46, 28.46, 28.46, 43.35, 60.40, 39.52, 43.68, 43.68, 27.89, 34.06, 34.06, 60.72, 60.62, 60.22, 50.13, 50.18, 48.28, 0.00]]

def get_distance_between_installation_number(first_order_number, second_order_number):
    return Distance[first_order_number][second_order_number]

class Order:
    def __init__(self, demand, departure_day, installation, order_number, deadline):
        self.demand = demand
        self.departure_day = departure_day
        self.installation = installation
        self.number = order_number
        self.deadline = deadline

order_sizes = []
order_deadlines = []
standard_order_size = {}
order_size_variations = {}


order_sizes.append([0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
order_sizes.append([3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 3, 0])
order_sizes.append([0, 3, 3, 0, 0, 0, 0, 0, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
order_sizes.append([0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 2, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0])
order_sizes.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 0, 0, 0, 3, 4, 0, 0, 0, 4, 5, 0, 0, 0, 0])
order_sizes.append([0, 0, 0, 0, 2, 4, 0, 3, 4, 0, 0, 5, 2, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
order_sizes.append([0, 0, 0, 0, 0, 2, 4, 3, 2, 0, 0, 0, 0, 2, 4, 4, 5, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0])
order_sizes.append([0, 0, 4, 0, 2, 4, 0, 0, 0, 2, 3, 0, 0, 0, 3, 0, 0, 4, 0, 2, 0, 0, 0, 3, 3, 0, 1])
order_sizes.append([2, 3, 2, 4, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 3, 4, 5, 0, 0, 0, 0])
order_sizes.append([2, 0, 0, 4, 0, 0, 3, 0, 0, 3, 3, 0, 2, 2, 0, 4, 1, 0, 4, 5, 0, 0, 4, 0, 0, 0, 4])
order_sizes.append([0, 2, 3, 0, 0, 3, 3, 2, 1, 0, 0, 0, 0, 4, 3, 2, 5, 0, 0, 0, 0, 0, 4, 3, 3, 0, 0])
order_sizes.append([2, 2, 0, 3, 0, 1, 0, 5, 0, 2, 0, 4, 3, 4, 0, 0, 0, 3, 4, 2, 1, 0, 0, 2, 0, 4, 0])
order_sizes.append([0, 2, 3, 2, 3, 4, 5, 0, 0, 0, 3, 4, 5, 3, 0, 0, 0, 2, 2, 1, 0, 0, 2, 3, 0, 0, 0])
order_sizes.append([0, 0, 3, 0, 0, 2, 0, 2, 3, 1, 3, 0, 0, 4, 2, 0, 4, 3, 4, 2, 3, 2, 3, 0, 3, 2, 0])
order_sizes.append([3, 3, 2, 4, 5, 1, 0, 0, 0, 3, 3, 5, 5, 2, 0, 0, 0, 1, 3, 5, 0, 0, 0, 4, 5, 0, 0])
order_sizes.append([3, 3, 1, 0, 0, 2, 4, 0, 2, 2, 0, 3, 0, 0, 4, 5, 0, 3, 1, 2, 3, 4, 0, 2, 3, 3, 3])
order_sizes.append([3, 2, 3, 2, 3, 0, 4, 0, 3, 1, 0, 3, 3, 3, 3, 0, 2, 1, 0, 2, 2, 3, 4, 0, 3, 1, 1])
order_sizes.append([3, 2, 3, 3, 2, 0, 2, 3, 4, 3, 5, 2, 2, 3, 0, 3, 3, 3, 4, 3, 2, 1, 0, 3, 4, 3, 0])
order_sizes.append([3, 3, 4, 3, 0, 5, 3, 1, 3, 2, 3, 3, 3, 3, 3, 2, 4, 3, 3, 3, 3, 3, 4, 3, 5, 2, 0])
order_sizes.append([3, 3, 4, 3, 3, 2, 2, 3, 3, 4, 2, 3, 2, 2, 4, 3, 3, 4, 3, 4, 1, 3, 3, 4, 3, 3, 3])


order_deadlines.append([0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
order_deadlines.append([4, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 2, 0])
order_deadlines.append([0, 3, 2, 0, 0, 0, 0, 0, 2, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
order_deadlines.append([0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 3, 0, 3, 0, 0, 2, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0])
order_deadlines.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 4, 4, 0, 0, 0, 4, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0])
order_deadlines.append([0, 0, 0, 0, 4, 4, 0, 4, 4, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
order_deadlines.append([0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0])
order_deadlines.append([0, 0, 3, 0, 3, 2, 0, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 2, 0, 3, 0, 0, 0, 3, 4, 0, 3])
order_deadlines.append([3, 4, 3, 3, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 3, 3, 4, 0, 0, 0, 0])
order_deadlines.append([3, 0, 0, 3, 0, 0, 3, 0, 0, 3, 3, 0, 3, 3, 0, 3, 3, 0, 4, 3, 0, 0, 4, 0, 0, 0, 4])
order_deadlines.append([0, 3, 3, 0, 0, 2, 3, 3, 2, 0, 0, 0, 0, 3, 2, 3, 4, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0])
order_deadlines.append([3, 3, 0, 3, 0, 3, 0, 4, 0, 3, 0, 3, 3, 3, 0, 0, 0, 4, 4, 4, 4, 0, 0, 3, 0, 4, 0])
order_deadlines.append([0, 3, 3, 3, 4, 4, 4, 0, 0, 0, 4, 4, 3, 2, 0, 0, 0, 3, 3, 3, 0, 0, 4, 4, 0, 0, 0])
order_deadlines.append([0, 0, 3, 0, 0, 4, 0, 3, 3, 3, 3, 0, 0, 3, 3, 0, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 0])
order_deadlines.append([3, 4, 3, 3, 3, 3, 0, 0, 0, 3, 4, 4, 4, 4, 0, 0, 0, 3, 4, 3, 0, 0, 0, 3, 4, 0, 0])
order_deadlines.append([3, 3, 3, 0, 0, 3, 3, 0, 3, 3, 0, 3, 0, 0, 3, 3, 0, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3])
order_deadlines.append([4, 4, 4, 4, 4, 0, 3, 0, 3, 3, 0, 3, 3, 3, 3, 0, 3, 4, 0, 4, 4, 4, 3, 0, 3, 3, 3])
order_deadlines.append([3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 4, 0, 3, 3, 3, 0])
order_deadlines.append([3, 3, 3, 3, 0, 3, 3, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0])
order_deadlines.append([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])




standard_order_size[1] =  15.0
standard_order_size[2] = 20.0
standard_order_size[3] = 15.0
standard_order_size[4] = 20.0
standard_order_size[5] = 20.0
standard_order_size[6] = 20.0
standard_order_size[7] = 20.0
standard_order_size[8] = 15.0
standard_order_size[9] = 15.0
standard_order_size[10] = 15.0
standard_order_size[11] = 15.0
standard_order_size[12] = 7.5
standard_order_size[13] = 15.0
standard_order_size[14] = 20.0
standard_order_size[15] = 10.0
standard_order_size[16] = 15.0
standard_order_size[17] = 15.0
standard_order_size[18] = 15.0
standard_order_size[19] = 15.0
standard_order_size[20] = 10.0
standard_order_size[21] = 17.5
standard_order_size[22] = 17.5
standard_order_size[23] = 17.5
standard_order_size[24] = 17.5
standard_order_size[25] = 17.5
standard_order_size[26] = 17.5
standard_order_size[27] = 15.0

order_size_variations[1] = 0.5
order_size_variations[2] = 0.75
order_size_variations[3] = 1.0
order_size_variations[4] = 1.25
order_size_variations[5] = 1.5

def get_orders_in_scenario(scenario_number):
    scenario_demand = order_sizes[scenario_number]
    scenario_deadlines = order_deadlines[scenario_number]
    orders = []
    orders.append(Order(0, 0, installations[0], 0, 10))
    counter = 1
    for i in range(len(scenario_demand)):
        if scenario_demand[i] != 0:
            order_demand = math.floor(standard_order_size[i + 1] * order_size_variations[scenario_demand[i]])
            deadline_day = scenario_deadlines[i]
            installation = installations[i + 1]
            orders.append(Order(order_demand, 0, installation, counter, deadline_day))
            counter += 1;

    order_numbers = []
    for order in orders:
        order_numbers.append(order.number)

    return orders, order_numbers



# ---------------------------- Vessels ----------------------------

class Vessel:
    def __init__(self, number, return_day, capacity, name, cost, is_spot_vessel):
        self.number = number
        self.return_day = return_day
        self.capacity = capacity
        self.name = name
        self.cost = cost
        self.is_spot_vessel = is_spot_vessel

vessel_return_days =[]

vessel_return_days.append([4, 0, 0, 0, 0, 0])
vessel_return_days.append([3, 0, 0, 0, 0, 0])
vessel_return_days.append([4, 0, 0, 0, 0, 0])
vessel_return_days.append([4, 0, 0, 0, 0, 0])
vessel_return_days.append([4, 0, 0, 0, 0, 0])
vessel_return_days.append([4, 4, 0, 0, 0, 0])
vessel_return_days.append([4, 4, 0, 0, 0, 0])
vessel_return_days.append([4, 0, 0, 0, 0, 0])
vessel_return_days.append([4, 3, 0, 0, 0, 0])
vessel_return_days.append([3, 4, 0, 0, 0, 0])
vessel_return_days.append([3, 3, 0, 0, 0, 0])
vessel_return_days.append([4, 3, 3, 0, 0, 0])
vessel_return_days.append([4, 4, 2, 0, 0, 0])
vessel_return_days.append([4, 4, 4, 0, 0, 0])
vessel_return_days.append([4, 3, 4, 0, 0, 0])
vessel_return_days.append([4, 3, 3, 0, 0, 0])
vessel_return_days.append([4, 3, 3, 0, 0, 0])
vessel_return_days.append([3, 3, 2, 2, 0, 0])
vessel_return_days.append([4, 4, 3, 2, 0, 0])
vessel_return_days.append([4, 3, 3, 2, 3, 0])

def get_vessels_in_scenario(scenario_number):
    scenario_vessels = vessel_return_days[scenario_number]
    vessels = []
    counter = 0
    spot_included = False
    for i in range(len(scenario_vessels)):
        if scenario_vessels[i] != 0:
            name = "PSV_" + str(counter)
            return_day = scenario_vessels[i]
            vessels.append(Vessel(counter, return_day, 100, name, 0, False))
            counter += 1
        else:
            name = "PSV_" + str(counter)
            vessels.append(Vessel(counter, 4, 100, name, 608, True))
            break

    vessel_numbers = []
    for vessel in vessels:
        vessel_numbers.append(vessel.number)

    return vessels, vessel_numbers



#Times

Times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143]
time_periods = []

for hour in Times:
    for i in range(number_of_time_periods_per_hour):
        index_of_this_time_period = hour * number_of_time_periods_per_hour + i
        time_periods.append(index_of_this_time_period)

# ---------------------------- WeatherForecast ----------------------------

#        ___________________________________________________________________________________
#       | Weather settings:                                                                 |
#       |-----------------------------------------------------------------------------------|
#       | W[0] = Good                                                                       |
#       | W[1] = Good -> Bad                                                                |
#       | W[2] = Bad -> Good                                                                |
#       | W[3] = Good -> Bad -> Good -> Bad -> Good                                         |
#        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Weather_states = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
Weather = Weather_states[0]

SpeedImpact = [0,0, 2, 3]

ServiceImpact = [1, 1.2, 1.3, 2]

# ---------------------------- Functions ----------------------------

def get_weather_impact(real_time):
    weather_state = get_weather_state(real_time)
    return ServiceImpact[weather_state]

def get_weather_state(real_time):
    return Weather[math.floor(real_time)]


def is_installation_by_order_number_closed(destination_order, real_time):
    time_of_day = real_time%24
    if destination_order.installation.opening_hour > time_of_day or destination_order.installation.closing_hour < time_of_day:
        return True
    return False
