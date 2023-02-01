"""Plotting Spline with highlighted select exemplar locations
"""
library(ggplot2)
library(dplyr)

# Indicator
indicator <- "u5m"
indicator_title <- "Under-5 Mortality rate"
covariate_title <- "log(LDI)"
time_period <- "2005-2019"

# Load indicator data and spline 
# Log(LDI) filepaths
indicator_data <- read.csv(file=paste0("/path/to/dir", indicator, ".csv"))
spline_data <- read.csv(
    file=paste0("/path/to/dir/", indicator, "spline_df.csv")
)

# Selecting exemplar locations based on time period ranking      
exemplar_locs <- c(169, 211, 187, 175, 213)

    
    # Plotting indicator data
scat_plot <-  ggplot(
    data=subset(
        indicator_data,
        !(location_id %in% exemplar_locs)) %>% arrange(year_id),
        aes(x=covariate, y=indicator, group=location_id)
    ) +
    geom_point(shape=21, color="grey", fill="grey", size=1) +
    geom_path(
        data=subset(
            indicator_data,
            !(location_id %in% exemplar_locs)) %>% arrange(year_id),
            color="grey"
    ) +
    ggtitle(paste0(
        indicator_title, " vs ", covariate_title, ", rankings for all time periods"
    )) +
    xlab(covariate_title) +
    ylab(indicator) +
    xlim(4, 12) +
    ylim(0, .3) + 
    # Highlighting the exemplar locs
    geom_path(
        data=subset(
            indicator_data,
            location_id %in% exemplar_locs) %>% arrange(year_id),
            aes(x=covariate, y=indicator, group=location_id),
            color="black"
    ) +
    geom_point(
        data=subset(
            indicator_data, location_id %in% exemplar_locs),
            aes(x=covariate, y=indicator, fill=year_id, color=year_id),
            shape=21,
            size=1.75
    ) +
    scale_colour_gradient(low = "black", high = "cyan3", guide="none") +
    geom_text(data=subset(
        indicator_data,
        location_id %in% exemplar_locs & year_id == 2019),
        aes(x=covariate, y=indicator, label=ihme_loc_id),
        hjust="left",
        nudge_x=0.01
    ) +
    # Spline line
    geom_line(
        data=spline_data,
        aes(x=covariate, y=spline_exp),
        color='blue',
        size=1.2
)
print(scat_plot)
  
ggsave(paste0("/path/to/dir", indicator, "_top5.pdf"),  scat_plot, width=5.5, height=3, units="in", scale=3)
  