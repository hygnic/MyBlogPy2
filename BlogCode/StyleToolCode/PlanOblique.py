# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              PlanOblique
# Author:            Hygnic
# Created on:        2023/2/2 0:10
# Version:           
# Reference:         
"""
Description:         平面斜轴图
# PLANOBLIQUIFIER by Bernhard Jenny (RMIT University)
# Applies shearing to a terrain model along the vertical y axis.
# Programming in python: Bojan Savric (Esri)

Usage:               
"""
# -------------------------------------------
# Importing libraries and modules
import math
import arcpy
import numpy


def planOblique(inDEM, outRaster, angle):
    """
    clusterHillshade: calculates a hillshade raster from a DEM

    Required arguments:
    Inputs:
        inDEM -- Input DEM.
        majFW -- majority filter smoothing.
        meanFW -- mean filter smoothing.
        minL -- maximum light direction.
        maxL -- minimum light direction.
    Outputs:
        outRaster -- cluster shaded relief.
    """
    try:
        #Storing ArcGIS parameters
        filePath = arcpy.GetParameterAsText(0)
        outputPath = arcpy.GetParameterAsText(1)
        inclinationAngle = float(arcpy.GetParameterAsText(2))
        
        noData = float('nan')
        
        # Check out the Spatial Analyst license
        arcpy.CheckOutExtension("Spatial")
        
        # Shearing factor of vertical exaggeration
        elevationScale = 1.0 / math.tan(math.radians(inclinationAngle))
        
        # Input Raster properties
        arcpy.AddMessage("Reading input raster...")
        inRas = arcpy.Raster(filePath)
        if inRas.isInteger:
            inRas = inRas * 1.0
        # end if
        
        # Lower left point
        lowerLeft = arcpy.Point(inRas.extent.XMin,inRas.extent.YMin)
        # Number of rows
        nRows = inRas.height
        # Number of columns
        nCols = inRas.width
        # Minimum elevation in grid (i.e. the elevation that will not shift)
        refElevation = inRas.minimum
        # Maximum elevation in grid (i.e. the elevation that will shift the most)
        maxElevation = inRas.maximum
        # y coordinate of northern most vertices in grid
        north = inRas.extent.YMax
        # Raster cell size
        cellSize = inRas.meanCellWidth
        
        
        # Computing the maximum y coordinate change of the highest raster point
        arcpy.AddMessage("Preparing input raster...")
        max_dy = (maxElevation - refElevation) * elevationScale
        
        # Max number of extra rows needed north of raster
        dRows = int(max_dy / cellSize + 1)
        
        # Update nRows and north
        nRows += dRows
        north += dRows * cellSize;
        
        # Convert Raster to numpy array
        arrIn = arcpy.RasterToNumPyArray(inRas,nodata_to_value=noData)
        
        # Init enlarged grid
        arr = numpy.empty((nRows,nCols))
        arr[:] = noData
        
        # Copy original raster to enlarged array
        arr[dRows:nRows,0:nCols] = arrIn
        
        # Init sheared grid
        arrOut = numpy.empty((nRows,nCols))
        arrOut[:] = noData
        
        
        # Fill sheared grid: iteerate over all columns
        arcpy.AddMessage("Filling sheared raster...")
        for col in range(nCols):
            # Keep track of the last vertext of the source grid that has been sheared.
            # This accelerates the algorithm, because we don't need to start
            # each search at the lower grid border, but can instead continue
            # searching at the last found vertex.
            prevRow = nRows - 1;
            
            # find the first valid grid value in the current column (from the bottom)
            # and remember its value
            prevZ = float('nan')
            for row in reversed(range(prevRow + 1)):
                if math.isnan(arr[row, col]):
                    arrOut[row, col] = float('nan')
                else:
                    prevRow = row
                    break
            #end if
            # end for
            
            # store the sheared y coordinate of the grid vertex below the current vertex
            prevShearedY = north - prevRow * cellSize
            
            #iterate over all rows, from bottom to top
            for row in reversed(range(prevRow + 1)):
                # the vertical y coordinate where an elevation value is needed
                targetY = north - row * cellSize
                
                # initialize z value at targetY
                interpolatedZ = float('nan')
                
                # vertically traverse the column towards upper border, starting
                # at the last visited vertex
                for r in reversed(range(prevRow + 1)):
                    # the elevation for the current vertex
                    z = arr[r, col]
                    
                    # move vertically accross patches of void values
                    if math.isnan(z):
                        move = r - 1
                        while ((move >= 0) and math.isnan(arr[move, col])):
                            move = move - 1
                        # end while
                        prevRow = move
                        interpolatedZ = noData
                        prevZ = noData
                        break
                    # end if
                    
                    # shear the y coordinate
                    shearedY = north - r * cellSize + (z - refElevation) * elevationScale;
                    
                    # if the sheared y coordinate is vertically higher than the
                    # y coordinate where an elevation value is needed, we have
                    # found the next upper vertex
                    if shearedY > targetY:
                        # linearly interpolate the elevations of the vertices
                        # that are vertically above and below
                        w = (targetY - prevShearedY) / (shearedY - prevShearedY)
                        interpolatedZ = w * z + (1.0 - w) * prevZ
                        break
                    # end if
                    
                    # the next target vertex might again fall between the same
                    # pair of vertices, so only update prevRow now.
                    prevRow = r;
                    
                    # store the sheared y coordinate and the elevation if the current
                    # vertex is not occluded by a previously sheared vertex
                    if shearedY >= prevShearedY:
                        prevShearedY = shearedY;
                        prevZ = z;
                # end if
                # end for
                
                # store the found z value in the grid
                arrOut[row, col] = interpolatedZ
        # end for
        # end for
        
        
        arcpy.AddMessage("Storing sheared raster...")
        # Search for empty rows on the north and south
        mask = numpy.isnan(arrOut)
        rows = numpy.flatnonzero((~mask).sum(axis=1))
        
        # Calculate start and end indecies of the output array
        start = rows[0]
        end = rows[-1] + 1
        
        # Correct lower left point for the removed empty rows on the south
        newLowerLeft = arcpy.Point(lowerLeft.X,lowerLeft.Y + cellSize * (nRows - end))
        
        # Convert array to raster (keep the original cellsize and new lower left)
        outRaster = arcpy.NumPyArrayToRaster(arrOut[start:end,:],newLowerLeft,cellSize,
                                             value_to_nodata=noData)
        
        # Definding spatial reference of the output raster
        spatialReference=inRas.spatialReference
        arcpy.DefineProjection_management(outRaster,spatialReference)
        
        #Saving an output Raster
        outRaster.save(outputPath)
    
    
    #RuntimeError exceptions
    except RuntimeError as y:
        arcpy.AddMessage("***ERROR OCCURRED!!!***\n" + format(y)) #Prompt message for user
    
    #Other exceptions
    except Exception as x:
        arcpy.AddMessage("***ERROR OCCURRED!!!***\nMessage from the system: " + format(x)) #Prompt message for user

# End main function

if __name__ == '__main__':
    
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  工具由 GIS荟 制作并发布  ------")
    arcpy.AddMessage(" --- 参考 by Kenneth Field (Esri) ---")
    arcpy.AddMessage(" ---- 技术 by Bojan Savric (Esri) ----")
    arcpy.AddMessage("|---------------------------------|\n")
    args = tuple(arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount()))
    planOblique(*args)
