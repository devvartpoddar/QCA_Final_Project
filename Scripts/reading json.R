rm(list = ls())

pkgs <- c('dplyr', 'magrittr', 'ggplot2', "stringi", 'jsonlite', 'rio')
lapply(pkgs, require, character.only = T)
rm(pkgs)

try(setwd("~/Desktop/QCA_Final_Project/"))
try(setwd("~/germanelection2017/"))

temp.data <- readLines("Data/News/news.json") %>%
  paste(collapse = ",") %>%
  stri_replace_all_regex("\\t", "") %>%
  stri_replace_all_fixed("\\", "") %>%
  paste("[", ., "]", sep = "\n") %>%
  fromJSON() %>%
  mutate(date = as.Date(date)) %>%
  filter(date >= as.Date("2001-09-22") & date <= as.Date("2002-09-22") |
           date >= as.Date("2004-09-18") & date <= as.Date("2005-09-18") |
           date >= as.Date("2008-09-27") & date <= as.Date("2009-09-27") |
           date >= as.Date("2012-09-22") & date <= as.Date("2013-09-22") |
           date >= as.Date("2016-09-22"))

export(temp.data, "../election_news.json")