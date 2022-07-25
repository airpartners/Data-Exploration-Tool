library(arrow)
library(tidyverse)
library(viridis)
# C:/dev/Air Partners/Data Analysis/data/east_boston/processed/sn45-final-w-ML-PM.parquet

df_1 <- read_parquet("C:/Users/zxiong/Desktop/Olin/Air Partners/downsampled/sn45-final-w-ML-PM.parquet") %>%
  mutate(
    time = as.POSIXct(timestamp_local, format="%m/%d/%Y %H:%M", tz="UTC"),
  )

df_2 <- 
  df_1 %>%
  # head(500) %>%
  filter(wind_direction_cardinal %in% c("W", "NW"), 
         adverse_flight_count > 10) %>%
  mutate(
    doublepm = pm25.ML*2
  )
#
df_2 %>%
  ggplot(mapping = aes(
    x = adverse_flight_count, 
    y = no2.ML, 
    color = no2.ML,
    size = no2.ML
  )) +
  geom_point() +
  # geom_col()
  # geom_line()
  geom_smooth(method=lm) +
  scale_color_viridis_c() +
  labs(
    x = "adverse flights",
    y = "no2",
    title = "no2 versus adverse flights",
    size = "no2",
    color = "no2"
  )
#
mylm <- df_2 %>%
  lm(adverse_flight_count ~ time, .)
print(mylm)
inter <- mylm[[1]]
slope <- mylm[[2]]
r2 <- summary(mylm)$r.squared
print(r2)

