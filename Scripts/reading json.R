rm(list = ls())

pkgs <- c('dplyr', 'magrittr', 'ggplot2', "stringi", 'jsonlite')
lapply(pkgs, require, character.only = T)
rm(pkgs)

setwd("~/Desktop/")

temp.data <- readLines("news.json") %>%
  paste(collapse = ",") %>%
  stri_replace_all_regex("\\t", "") %>%
  paste("[", ., "]", sep = "\n") %>%
  fromJSON() %>%
  mutate(date = as.Date(date))

temp.data %>%
  group_by(date) %>%
  summarise(value = n()) %>%
  ggplot() +
  geom_point(es)