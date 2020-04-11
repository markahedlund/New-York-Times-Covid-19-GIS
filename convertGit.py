
#This converts CSV files from the New York Times Covid-19 tracking repository into ArcGIS shapefiles or features in a 
#geodatabase. This script requires a template point feature class with the centers of all the counties you want to map. 
#It is included as a zip file on this repository as template.zip. The template must be stored in the same folder or 
#geodatabase that the output will be written to, or you could change the script. The three file names and file paths 
#must be added to the script below. Paths have to include the trailing /.

import arcpy
arcpy.env.overwriteOutput = True

outName = "Output_Name"
inputCSV = "InputFile.csv"
templateName = "Template"

dataDir = "Full path to incoming data directory including the trailing /"
errorDir = "Full path to the folder where you want messages/errors written including the trailing /"
outputDir = "Full path to the folder or .gdb where you want the new feature class including the last /"

template = outputDir + templateName
inputFile = dataDir + inputCSV
errorFile = errorDir + outName + "_Not_Mapped.txt"
output = outName + "_z"
outputP = outputDir + output

errors = open(errorFile, "w")
file = open(inputFile)

sr = arcpy.Describe(template).spatialReference
arcpy.management.CreateFeatureclass(outputDir, output, "POINT", template, "", "", sr)

countyCenters = {}

with arcpy.da.SearchCursor(template, ["FIPS", "PopEst2019", "SHAPE@XY"]) as cursor:
    for row in cursor:
        countyCenters[row[0]] = [row[1], row[2]]

with arcpy.da.InsertCursor(outputP, ["Date", "County", "State", "Cases", "Deaths", "PopEst2019", "FIPS", "SHAPE@XY"]) as cursor:
    for line in file:
        tL = line.split(",")
        if not tL[3]:
            if tL[1] == "New York City":
                errors.write("Caught: " + str(line))
                fips = "00005"
            elif tL[1] == "Kansas City":
                errors.write("Caught: " + str(line))
                fips = "00004"
            else:
                fips = "00001"
        elif tL[3].isalpha():
            errors.write(str(line) + "\n")
            fips = "00001"
        else:
            fips = tL[3]

        if fips in countyCenters.keys():
            dateL = tL[0].split("-")
            date = dateL[1] + "/" + dateL[2] + "/" + dateL[0]
            info = countyCenters[fips]
            xy = info[1]
            population = info[0]
            cursor.insertRow([date, tL[1], tL[2], tL[4], tL[5], population, fips, xy])
        else:
            errors.write(str(tL) + tL[3] + "\n")

errors.close()
file.close()

print("Finished drawing points. Now calculating previous fields.")

outName = outputP[:-2]

arcpy.management.Sort(outputP, outName, "FIPS ASCENDING;Date ASCENDING", "UR")

cases = []
deaths = []

location = "00009"

with arcpy.da.UpdateCursor(outName, ["FIPS", "Cases", "Deaths", "PreviousDC", "PreviousWC", "PreviousDD", "PreviousWD", "Recovered"]) as cursor:
    for row in cursor:
        if row[0] == location:
            row[3] = pCases
            row[5] = pDeaths
            pCases = row[1]
            pDeaths = row[2]
            cases.append(row[1])
            deaths.append(row[2])
            count += 1
            if count > 7:
                row[4] = cases[indexW]
                row[6] = deaths[indexW]
                indexW += 1
            if count > 21:
                row[7] = cases[indexR]
                indexR += 1
        else:
            cases.clear()
            deaths.clear()
            location = row[0]
            pCases = row[1]
            pDeaths = row[2]
            cases.append(row[1])
            deaths.append(row[2])
            count = 1
            indexW = 0
            indexR = 0

        cursor.updateRow(row)
print(outputP)
arcpy.Delete_management(outputP)

print("Done")
