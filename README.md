# Maritime Routing Congestion

This repository holds the code and data files pertaining to the study: "Shortest-path travel-time errors and annual traffic-density associations in AIS-derived U.S. cargo voyages".

In particular, this repository contains the Python code used to construct cargo-ship voyages with AIS data, calculate Dijkstra-based travel-time estimates, measure the annual traffic density of these routes with various methods, and generate the statistical results reported in the paper. Along with the Python scripts, data files of the final trajectories, the port radius and vessel speed sensitivity analyses, the port data gathered from World Port Index, and statistical data collected over the final trajectories are also included.

## Process

1. Port identifiers and coordinates were retrieved from the World Port Index, and the coordinates were converted from degrees, minutes, seconds (DMS) to decimal degrees.
2. Voyages were constructed from AIS data over the span of two weeks, testing three constant values for the selected port radius.
3. The observed duration was calculated between the first and last broadcast points of each voyage, while the Python package _searoute_ was implemented to estimate every trip's duration based on Dijkstra's shortest-path algorithm. Various constant speeds were tested with searoute's calculations.
4. Raster values that represent annual traffic density were obtained along every journey, and each voyage was attributed with its mean, median, and maximum congestion value.
5. Tables that summarize important variables, compare route-based statistics, display Pearson's correlation coefficients for the three congestion metrics, and conduct sensitivity analyses for the port radius and vessel speed were created.
6. Two figures were created to display the relationship between observed and predicted duration and compare error metrics between routes.

## Data

AIS broadcast point data and annual transit count data were obtained from MarineCadastre, co-hosted by the National Oceanic and Atmospheric Administration (NOAA). 
Port coordinates were obtained from the World Port Index.
