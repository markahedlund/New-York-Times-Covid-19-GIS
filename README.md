# New York Times Covid-19 GIS
 New York Times Covid-19 tracking data for the US converted into a point feature class that can be "time enabled".
 
 The original data can be found here: https://github.com/nytimes/covid-19-data

 The data from the New York Times is distributed as a CSV file with each row containing Covid-19 case information about a county/date. 
 I wrote a python script to convert each point into a point feature with a time field. The points are derived from centroids of US Census 
 Tigerline county shapes. 
 
 Additional fields were added for data exploration which I'll describte in more detail later. 
