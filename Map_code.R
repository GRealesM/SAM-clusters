#### --- Figure 1 Script -------------------

### Load libraries

library(data.table)
library(sf)
library(ggsn)
library(dplyr)
library(ggplot2)
library(raster)
library(rasterVis)
library(rnaturalearth)
library(ggrepel)


  
theme_set(theme_bw()) # Theme which is appropriate for maps
    
### Gather map, elevation, and population data

world <- ne_countries(scale = "medium", returnclass = "sf")

popdata <- fread("Pop_data.tsv")
popdata <- na.omit(popdata, cols = c("lat", "lon"))

 map <- ggplot(data = world) +
            geom_sf(fill = "#E8CDB0") +
            coord_sf(xlim = c(min(popdata$lon)-3, max(popdata$lon)+3), ylim = c(max(popdata$lat) + 3, min(popdata$lat)-3), expand = FALSE) +
            geom_point(data = popdata, aes(x=lon, y = lat, shape = Etiology_label), size =2, position = position_dodge(1.5)) +
            scale_shape_discrete("Etiology")+
            ggsn::scalebar(world[world$sovereignt == "Brazil" | world$sovereignt == "Panama",], dist = 500, dist_unit = "km", transform = TRUE, model = "WGS84", anchor = c(x= -34, y = -43)) +
            north(world[world$sovereignt == "Brazil" | world$sovereignt == "Nicaragua",], scale = 0.15) +
            theme(panel.grid.major = element_line(color = gray(.5), linetype = "dashed", size = 0.5), panel.background = element_rect(fill = "#B2D4E6"), axis.title = element_blank(), ) 

 map
 ggsave("Map_20220723.png", map, width = 22, height = 22, units = "cm", bg = "white")
 
