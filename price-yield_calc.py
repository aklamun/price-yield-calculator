# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 16:52:49 2016

@author: ariah
"""

import numpy as np
from scipy import optimize
import datetime

def pv(r,cashflows,periods):
    d = np.ones(len(cashflows))*(1+r)
    d = np.power(d,periods)
    v = np.divide(cashflows,d)
    pv = np.sum(v)
    return pv

def calc_yield(coupon, servicing, SMM, price, WAM, settlement, delay):
    # calculates yield (monthly) assuming the settlement day is the purchase day
    f = open('cashflows','w')
    f.write('period\tperiod2\tbal\tamort\tprepay\tinterest\n')
    bal = float(1)
    coupon = float(coupon)
    gc = coupon + float(servicing)
    delay_days = delay + 1 - settlement.day
    cashflows = np.zeros(WAM+1)
    periods = np.zeros(WAM+1)
    periods[0] = float(0)
    accrued_days = settlement.day-1
    cashflows[0] = -price/100 - coupon/36000*accrued_days
    for i in range(1,WAM+1):
        cur_WAM = float(WAM-i+1)
        amort = ((1+gc/1200)-1)/((1+gc/1200)**cur_WAM-1)*bal
        prepay = SMM*(bal-amort)
        interest = coupon/1200*bal
        cashflows[i] = interest + amort + prepay
        bal = bal - amort - prepay
        periods[i] = float(i) + float(delay_days)/30.0
        f.write("%s\t%s\t%s\t%s\t%s\t%s\n" %(str(i),str(periods[i]),str(bal),str(amort),str(prepay),str(interest)))
    #x = np.irr(cashflows)
    r0 = float(4.0/1200.0)
    y = optimize.newton(pv,r0,args=(cashflows,periods))
    
    f.close()
    return y*1200

settle=datetime.date(2016,3,14)
y0 = calc_yield(3.5,0.6,0.0,104.3125,355,settle,24)
y2 = calc_yield(3.5,0.6,0.02,104.3125,355,settle,24)