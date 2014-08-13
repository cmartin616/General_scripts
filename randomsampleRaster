import arcpy
from arcpy.sa import *

inShape = SET THIS VALUE

#convert Feature to Raster
arcpy.FeatureToRaster_conversion(inShape, SET THIS VALUE IN QUOTES, I.E. "OBJECTID", "shpToRast", 65.6168 )

#Set cell size and extent to input raster
arcpy.env.cellSize = 'shpToRast'
arcpy.env.extent = 'shpToRast'
arcpy.env.overwriteOutput = True

#Create random raster from input
randRaster= arcpy.sa.CreateRandomRaster(419,'shpToRast','shpToRast')

#Return a raster of X values within input raster, decrease VALUE to increase returns
sampFrame = arcpy.sa.Con(randRaster, "shpToRast", "", "VALUE > .999")

#Converts random sample to points
arcpy.RasterToPoint_conversion (sampFrame, 'sampFrame_feat', "Value")
