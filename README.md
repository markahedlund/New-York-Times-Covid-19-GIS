# New York Times Covid-19 GIS
 New York Times Covid-19 tracking data for the US converted into a GIS shapefile, point feature class, that can be "time enabled".
 
 The original data can be found here: https://github.com/nytimes/covid-19-data

 The data from the New York Times is distributed as a CSV file with each row containing Covid-19 case information about a county/date. 
 I wrote a python script to convert each point into a point feature with a time field. The points are derived from centroids of US Census 
 Tigerline county shapes. 
 
 Geography: New York City data is combined for all five boroughs by NYT. To map it, I used the centriod of the New York City "place" 
 Tigerline shape. Kansas City is reported seperately from the counties that the city spans. County centriods were assigned county numbers
 and Kansas City data was assigned to the centroid of the Kansas City "place" Tigerline shape. 
 
 Many entries in the data set are not assigned to any county. These were not mapped. Each of these skipped entires can be found in the 
 NYT-Covid-19_not_mapped.txt file. That file also contains entries for New York and Kansas City that were mapped as descibed above.
 
 The PreviousDC field are the number of cases for that point on the previous date. The PreviousWC field are the number of cases for that 
 point seven days previous. The PreviousDD and PreviousWD are the same with deaths. 
 
 Cases are automatically added to the Recovered field when they are 21 days old. Subtracting this field and Deaths from cumulative cases
 might give some approximation of the active case number. 
 
 I can update this as long as the New York Times continues to update their data, if anyone is interested.
