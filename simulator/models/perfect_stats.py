from dataclasses import dataclass

@dataclass
class PerfectStats:
    """Class to hold ideal growing conditions for plants"""
    light: tuple[float, float]  # min, max in lux
    ambientTemperature: tuple[float, float]  # min, max in Celsius
    ambientHumidity: tuple[float, float]  # min, max in %
    soilMoisture: tuple[float, float]  # min, max in %
    soilTemperature: tuple[float, float]  # min, max in Celsius
    soilPh: tuple[float, float]  # min, max pH

    @classmethod
    def for_tomatoes(cls):
        return cls(
            light=(15000, 85000),  # Tomatoes need bright light
            ambientTemperature=(20, 30),  # Ideal growing temp
            ambientHumidity=(65, 85),  # Moderate to high humidity
            soilMoisture=(60, 80),  # Keep soil moist but not waterlogged
            soilTemperature=(18, 24),  # Warm soil preferred
            soilPh=(6.0, 6.8)  # Slightly acidic soil
        )

    @classmethod
    def for_lettuce(cls):
        return cls(
            light=(10000, 70000),  # More shade tolerant
            ambientTemperature=(15, 22),  # Cooler temperatures
            ambientHumidity=(50, 70),  # Moderate humidity
            soilMoisture=(50, 70),  # Even moisture
            soilTemperature=(13, 20),  # Cool soil
            soilPh=(6.0, 7.0)  # Near neutral pH
        )

    def check_conditions(self, sensor_readings):
        """
        Check if current conditions match ideal conditions
        Returns dict of parameters that are out of range
        """
        issues = {}
        
        for reading in sensor_readings:
            value = reading["value"]
            if reading["type"] == "light":
                if not (self.light[0] <= value <= self.light[1]):
                    issues["light"] = (value, self.light)
                    
            elif reading["type"] == "temperature":
                if reading["subtype"] == "ambient":
                    if not (self.ambientTemperature[0] <= value <= self.ambientTemperature[1]):
                        issues["ambient_temperature"] = (value, self.ambientTemperature)
                else:  # soil temperature
                    if not (self.soilTemperature[0] <= value <= self.soilTemperature[1]):
                        issues["soil_temperature"] = (value, self.soilTemperature)
                        
            elif reading["type"] == "humidity":
                if reading["subtype"] == "ambient":
                    if not (self.ambientHumidity[0] <= value <= self.ambientHumidity[1]):
                        issues["ambient_humidity"] = (value, self.ambientHumidity)
                else:  # soil moisture
                    if not (self.soilMoisture[0] <= value <= self.soilMoisture[1]):
                        issues["soil_moisture"] = (value, self.soilMoisture)
                        
            elif reading["type"] == "ph":
                if not (self.soilPh[0] <= value <= self.soilPh[1]):
                    issues["soil_ph"] = (value, self.soilPh)
                    
        return issues