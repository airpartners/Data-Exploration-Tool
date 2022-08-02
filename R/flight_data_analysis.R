library(arrow)
library(tidyverse)
library(magrittr)
library(viridis)

df_1 <- read_parquet("C:/dev/Air Partners/Data Analysis/data/east_boston/processed/sn45-final-w-ML-PM.parquet") %>%
# df_1 <- read_parquet("C:/Users/zxiong/Desktop/Olin/Air Partners/downsampled/sn45-final-w-ML-PM.parquet") %>%
  mutate(
    time = as.POSIXct(timestamp_local, format="%m/%d/%Y %H:%M", tz="UTC"),
    wd_cardinal = wd %>% 
      mod(360 * (1 - 1/16)) %>% 
      cut(
        breaks = c(0, seq(from = 360 * (1/16), to = 360 * (1 - 1/16), by = 360 * 1/8)), 
        labels = c("N", "NE", "E", "SE", "S", "SW", "W", "NW")
      )
  )

df_cardinal <- 
  df_1 %>% 
  select(wd, wind_direction_cardinal, wd_cardinal)
  

df_2 <- 
  df_1 %>%
  # head(500) %>%
  filter(
    wind_direction_cardinal %in% c("NW", "SE"),
    # wd_cardinal %in% c("S", "SW", "SE"),
    # adverse_flight_count > 5,
    ws > 6,
    temp_manifold > 10,
    # rh_manifold > 70,
    # ws < 12
  ) %>%
  mutate(
    # x_var = adverse_flight_count,
    x_var = count,
    y_var = co.ML
  )
  # select(x_var, y_var)
#
df_2 %>%
  ggplot(mapping = aes(
    x = x_var, 
    y = y_var, 
    color = rh_manifold,
    size = rh_manifold
  )) +
  geom_point() +
  # geom_col()
  # geom_line()
  geom_smooth(method=lm) +
  scale_color_viridis_c() + 
  labs(
    x = "Adverse Flights", 
    y = "CO"
  )
#
mylm <- df_2 %>%
  lm(y_var ~ x_var, .)
print(mylm)
inter <- mylm[[1]]
slope <- mylm[[2]]
r2 <- summary(mylm)$r.squared
print(r2)

