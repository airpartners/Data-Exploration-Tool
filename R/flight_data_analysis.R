library(arrow)
library(tidyverse)

df_1 <- read_parquet("C:/dev/Air Partners/Data Analysis/data/east_boston/processed/sn45-final-w-ML-PM.parquet") %>%
  mutate(
    time = as.POSIXct(timestamp_local, format="%m/%d/%Y %H:%M", tz="UTC"),
  )

df_1 %>%
  head(500) %>%
  ggplot(mapping = aes(x = time, y = adverse_flight_count)) +
  geom_point()
