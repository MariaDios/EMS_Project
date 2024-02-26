# EcoExt.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Amort:
    # Outputs an amortisation schedule, alias a cash flow, for a loan in pandas data frame.

    def __init__(self, capital_cost, procent_own_capital, annual_interest_rate, payments_per_year, years):
        self.capital_cost = capital_cost
        self.procent_own_capital = procent_own_capital
        self.annual_interest_rate = annual_interest_rate
        self.payments_per_year = payments_per_year
        self.years = years

    def PMT(self):
        loan = self.capital_cost*(1-(self.procent_own_capital/100))
        rate = self.annual_interest_rate / self.payments_per_year
        nper = self.payments_per_year * self.years
        if rate != 0:
            pmt = (rate * (loan * (1 + rate) ** nper)) / ((1 + rate) * (1 - (1 + rate) ** nper))
        else:
            pmt = (-1 * (loan) / nper)
        return pmt

    def IPMT(self, per):
        loan = self.capital_cost*(1-(self.procent_own_capital/100))
        rate = self.annual_interest_rate / self.payments_per_year
        ipmt = -(((1 + rate) ** (per - 1)) * (loan * rate + self.PMT()) - self.PMT())
        return ipmt

    def PPMT(self, per):
        ppmt = self.PMT() - self.IPMT(per)
        return ppmt

    def amortisation_schedule(self):
        loan = self.capital_cost*(1-(self.procent_own_capital/100))
        df = pd.DataFrame({"Principal": [self.PPMT(i + 1) for i in range(self.payments_per_year * self.years)],
                           "Interest": [self.IPMT(i + 1) for i in range(self.payments_per_year * self.years)]})

        df["Payment"] = df.Principal + df.Interest
        df["Balance"] = loan + np.cumsum(df.Principal)
        df["Period"] = range(1, df.shape[0] + 1)
        return df.abs()
    

class AmortPlot:
    # Visualises amortisation schedule (payement balance and loan balance).

    def __init__(self, amort):
        self.amort = amort

    def plot_payment_balance(self):
        fig, ax = plt.subplots()

        ax.stackplot(self.amort["Period"], self.amort["Interest"], self.amort["Principal"],
                      labels=["Interest", "Principal"], colors = ["r", "g"])
        plt.legend(loc="upper right")
        plt.margins(0, 0)
        plt.xlabel(f"Amortisation period: {self.amort['Period'].tolist()[-1]} months")
        ax.set_ylabel(f"Payment: {round(self.amort['Payment'][0], 2)} € monthly", ha="left", y=0, labelpad=0)
        plt.title("Payment balance")
        plt.show()
    

    def plot_loan_balance(self):
        fig, ax = plt.subplots()

        ax.bar(self.amort["Period"], self.amort["Balance"], color="g")
        plt.vlines(x=0, ymin=0, ymax=self.amort["Balance"].max(), color="r", linewidth=2)
        plt.xlabel(f"Amortisation period: {self.amort['Period'].tolist()[-1]} months")
        plt.margins(0.005, 0)
        ax.set_ylabel("Debt (€)", ha="left", y=0, labelpad=0)
        plt.title("Debt balance")
        plt.show()


class NPV:
    # Outputs Net Presnt Values: NPV, inflation adjusted NPV and NPV for loan amortisation in pandas data frame plus prints results.
    
    def __init__(self, capital_cost, annual_interest_rate, payments_per_year, years, inflation, amort, cash_flow = None, get_print = True):
        self.capital_cost = capital_cost
        self.annual_interest_rate = annual_interest_rate
        self.payments_per_year = payments_per_year
        self.years = years
        self.inflation = inflation
        self.amort = amort
        self.cash_flow = cash_flow
        self.get_print = get_print
        
    def npv(self):
        
        if self.cash_flow is not None:
            
            # NPV
            npv01 = sum(cashf / (1 + self.annual_interest_rate / self.payments_per_year) ** i for i, cashf in enumerate(self.cash_flow, 1))

            # Inflation adjusted NPV
            real_cash_flow = [cashf / (1 + self.inflation / self.payments_per_year) ** i for i, cashf in enumerate(self.cash_flow, 1)]
            npv02 = sum(cashf / (1 + self.annual_interest_rate / self.payments_per_year) ** i for i, cashf in enumerate(real_cash_flow, 1))

        # NPV for loan amortisation
        loan_payments = self.amort["Payment"].tolist()
        loan_payments.insert(0, self.capital_cost)
        npv03 = sum(payment / (1 + self.annual_interest_rate / self.payments_per_year) ** i for i, payment in enumerate(loan_payments, 1))

        # Create a DataFrame to store NPV values, print them if get_print = True
        if self.cash_flow is not None:
            df = pd.DataFrame({
                "npv": [npv01],
                "npv_inf": [npv02],
                "npv_loanp": [npv03]
                }) 
            if self.get_print:
                print(f"\nNPV: {round(df.npv[0], 2)} €")
                print(f"Inflation adjusted NPV: {round(df.npv_inf[0], 2)} €")
                print(f"Loan amortisation NPV: {round(df.npv_loanp[0], 2)} €\n")
            
        else: 
            df = pd.DataFrame({
                "npv_loanp": [npv03]
                })
            if self.get_print:
                print(f"\nLoan amortisation NPV: {round(df.npv_loanp[0], 2)} €\n")
        return df
    

class SimPlot:
    # For visualising monthly payement and NPV in dependence of other variables.

    def __init__(self, sim, groupBY = "", x = "", y = "", xlab = "", ylab = ""):
        self.sim = sim
        self.groupBY = groupBY
        self.x = x
        self.y = y
        self.xlab = xlab
        self.ylab = ylab

        groups = self.sim.groupby(self.groupBY)

        fig, ax = plt.subplots()
        for name, group in groups:
            ax.plot(group[self.x].tolist(), group[self.y].tolist(), marker="o", linestyle="", ms=12, label=name)
        ax.legend()
        plt.xlabel(self.xlab)
        plt.margins(0, 0)
        ax.set_ylabel(self.ylab, ha="left", y=0, labelpad=0)
        plt.title(f"{self.groupBY}")
        plt.show()

        
        
    


