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
  filter(
    wind_direction_cardinal %in% c("W", "NW"), 
    adverse_flight_count > 10
  ) %>% 
  mutate(
    x_var = adverse_flight_count, 
    y_var = correctedNO
  ) %>% 
  select(x_var, y_var)
#
df_2 %>%
  ggplot(mapping = aes(
    x = x_var, 
    y = y_var, 
    color = y_var,
    size = y_var
  )) +
  geom_point() +
  # geom_col()
  # geom_line()
  geom_smooth(method=lm) +
  scale_color_viridis_c() +
  labs(
    x = "adverse flights",
    y = "no2",
    title = "no versus adverse flights",
    size = "no",
    color = "no"
  )
#
mylm <- df_2 %>%
  lm(y_var ~ x_var, .)
print(mylm)
inter <- mylm[[1]]
slope <- mylm[[2]]
r2 <- summary(mylm)$r.squared
print(r2)

