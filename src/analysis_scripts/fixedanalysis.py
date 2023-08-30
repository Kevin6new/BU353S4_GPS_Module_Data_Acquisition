import pandas as kevpd
import matplotlib.pyplot as kevplt
fixed_df = kevpd.read_csv(r'/home/kevin32/catkin_ws/src/data/fixed.csv')
kevplt.title("Stationary Data Analysis")
kevplt.xlabel("UTM-Easting")
kevplt.ylabel("UTM-Northing")
easting =fixed_df[".UTM_easting"]
northing = fixed_df[".UTM_northing"]
kevplt.plot(easting, northing, color='g')
kevplt.show()

