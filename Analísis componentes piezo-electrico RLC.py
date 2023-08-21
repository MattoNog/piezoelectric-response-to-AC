# -*- coding: utf-8 -*-
"""
Created on Tue May 30 12:55:35 2023

@author: matia
"""
import uncertainties as unc
import uncertainties.unumpy as unp
import numpy as np
import pandas as pd

#%%definos errores res in out #OHMS, ancho de banda y frec de res #Hz

r_1 = 9820
err_r1 = 500

r_2 = 9850
err_r2 = 500


#LOCKIN

w_s = 50095.85 * 2 * np.pi
err_ws = 0.5 * 2 * np.pi #dos veces la res de la frec

delta_w = 6 * 2 * np.pi
err_dw = 1 * 2 * np.pi

w_p = 50283.62 * 2 * np.pi
err_wp = 0.5 * 2 * np.pi 

r_1 = unc.ufloat(r_1, err_r1)

r_2 = unc.ufloat(r_2, err_r2)    

w_s = unc.ufloat(w_s, err_ws)  

delta_w = unc.ufloat(delta_w, err_dw)  

w_p = unc.ufloat(w_p, err_wp)  


#%% 

#OSC

w_s_osc = 50095.70 * 2 * np.pi
err_ws_osc = 3 * 2 * np.pi

delta_w_osc = 6 * 2 * np.pi
err_dw_osc = 1 * 2 * np.pi

w_p_osc = 50281.37 * 2 * np.pi
err_wp_osc = 3 * 2 * np.pi


w_s_osc = unc.ufloat(w_s_osc, err_ws_osc)  

delta_w_osc = unc.ufloat(delta_w_osc, err_dw_osc)  

w_p_osc = unc.ufloat(w_p_osc, err_wp_osc)  


#%%
#DEFINO VALORES PARA TRANSFERENCIA VPP

v_osc = 0.664
err_osc = 0.008

v_loc = 0.6023
err_loc = 4.618182333597846e-05

v_gen = 0.983
err_gen = 0.007

v_osc = unc.ufloat(v_osc, err_osc)
v_loc = unc.ufloat(v_loc, err_loc)
v_gen = unc.ufloat(v_gen, err_gen)


#%% Calculo R

def T(V_1, V_2):
    return (V_1 / V_2)

def R(T, r_2):
    return ((r_2 / T) - r_2)

T_osc = T(v_osc, v_gen) 
T_loc = T(v_loc, v_gen) 

R_osc = R(T_osc, r_2) 
R_loc = R(T_loc, r_2) 

print("T: ", T_osc, " osc; ", T_loc, " loc.")
print("R: ", R_osc, " osc; ", R_loc, " loc.")

#%% Calculo L

def L(delta_w, R, r_2, w_s):
    return ((delta_w * (R + r_2))/w_s)

L_osc = L(delta_w_osc, R_osc, r_2, w_s_osc) 
L_loc = L(delta_w, R_loc, r_2, w_s) 

print("L: ", L_osc, " osc; ", L_loc, " loc.")

#%% Calculo C

def C(w_s, L):
    return (1/(w_s**(2) * L))

C_osc = C(w_s_osc, L_osc)
C_loc = C(w_s, L_loc)


print("C: ", C_osc, " osc; ", C_loc, " loc.")



#%% Calculo C PARALELO

def C2(w_p, C, L):
    return (C/( w_p**(2) * L * C -1))


C2_osc = C2(w_p_osc, C_osc, L_osc)
C2_loc = C2(w_p, C_loc, L_loc)

print("C2: ", C2_osc, " osc; ", C2_loc, " loc.")


#%%

