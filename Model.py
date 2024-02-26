# Model.py

class Battery:
    
    capacity_kWh = 1000
    charge_kW = 200
    discharge_kW = 200
    current_kWh = capacity_kWh
    
    @property
    def SoC(self):
        """returns the State of Charge als Wert zwischen [0 - 1]"""
        return self.current_kWh / self.capacity_kWh

    @property
    def max_charge(self):
        """returns the maximum possible charge to the battery 
        limited by the maximum charging power and the current battery charge 
        for a given hour in [kWh]"""
        return min(self.charge_kW, self.capacity_kWh - self.current_kWh)
    
    @property
    def max_discharge(self):
        """returns the maximum possible DIScharge FROM the battery 
        limited by the maximum DIScharging power and the current battery charge 
        for a given hour in [kWh]"""
        return min(self.discharge_kW, self.current_kWh)

    def charge(self, amount):
        """charges the battery by the maximum possible amount, 
        up to the requested parameter [amount] 
        and RETURNS the actual amount charged (which is <= the [amount] requested)"""
        cha = min(self.max_charge, amount)
        self.current_kWh += cha
        return cha

    def discharge(self, amount):
        """DIScharges the battery by the maximum possible amount, 
        up to the requested parameter [amount] 
        and RETURNS the actual amount charged (which is <= the [amount] requested)"""
        discha = min(self.max_discharge, amount)
        self.current_kWh -= discha
        return discha

    
class Etruck(Battery):
    
    capacity_kWh = 400     
    charge_kW = 100
    discharge_kW = 150
    current_kWh = capacity_kWh
    avg_km_per_h = 15
    consumption = 0.85 # kWh/km

    def __init__(self, 
                 schedule = "workday",  # workday, worknight
                 avg_km_per_h = 15): 
        """initializes a truck with a schedule string, and an avg_km_per_h mileage when the schedule is 'offsite'"""
        
        super().__init__()  # Initialize the Battery class attributes
        self.schedule = schedule
        
        if self.status == "offsite":
            self.avg_km_per_h = avg_km_per_h  


    def status(self, hour_of_day, day_of_week): #hour_of_day [0-23], day_of_week [0-4 workday, 5,6 weekend] 
        """if the trucks's schedule parameter is 'workday', 
        it should return the string 'onsite' on weekends and on workdays from 3:00 until 6:00 AM
        otherwise 'offsite'
        if the trucks's schedule parameter is 'worknight', 
        it should return the string 'onsite' on weekends and on workdays from 7:00 until 19:00 AM,
        otherwise 'offsite'
        """

        if self.schedule == "workday":
            if day_of_week >= 5 or (day_of_week < 5 and 3 <= hour_of_day <= 6):
                return "onsite"
            else:
                return "offsite"
            
        if self.schedule == "worknight":
            if day_of_week >= 5 or (day_of_week < 5 and 7 <= hour_of_day <= 19):
                return "onsite"
            else:
                return "offsite"
        if self.schedule == "daytime":
            if 3 <= hour_of_day <= 6:
                return "onsite"
            else:
                return "offsite"
        if self.schedule == "nighttime":
            if 7 <= hour_of_day <= 19:
                return "onsite"
            else:
                return "offsite"
        if self.schedule == "evening":
            if day_of_week >= 5 or (day_of_week < 5 and 16 <= hour_of_day <= 19):
                return "onsite"
            else:
                return "offsite"
        if self.schedule == "lunchbreak":
            if (6 <= hour_of_day <= 12) or (14 <= hour_of_day <= 19):
                return "offsite"
            else:
                return "onsite"
            
    @property
    def chargeable(self, hour_of_day, day_of_week):
        """returns True if the Truck is currently chargeable"""
        if self.status(hour_of_day, day_of_week) == "onsite":
            return True
        else:
            return False

    @property
    def hourly_demand(self):
        """returns the hourly energy demand in [kWh] of a typical hour"""
        return self.avg_km_per_h * self.consumption
    
    @property
    def weekly_energy_demand(self):
        """returns the WEEKLy energy demand in [kWh] of the car"""
        # 5 workdays * 12 working hours
        return self.hourly_demand * 5 * 12
    
    def __repr__(self):
        """should return the string:
        Etruck(schedule='schedulestring')
        """
        return f"Etruck(schedule='{self.schedule}')"






