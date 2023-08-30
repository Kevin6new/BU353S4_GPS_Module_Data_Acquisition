import pandas as kevpd
import matplotlib.pyplot as kevplt
active_df = kevpd.read_csv(r'/home/kevin32/catkin_ws/src/data/active.csv')
kevplt.title("Moving Data Analysis")
kevplt.xlabel("UTM-Easting")
kevplt.ylabel("UTM-Northing")
easting =active_df[".UTM_easting"]
northing = active_df[".UTM_northing"]
kevplt.plot(easting, northing, color='y')
kevplt.show()

