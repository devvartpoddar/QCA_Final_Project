# Topic modelling the lemmatised text

try(setwd("/home/devvart/Desktop/QCA_Final_Project"))
try(setwd("/home/devvart/QCA_Final_Project"))

source("packages.R")

# Exporing  the terms in a cleaner dataset

import("Data/term_breakdown.json") %>%
  group_by(topic) %>%
  top_n(20, beta) %>%
  group_by(topic) %>%
  summarise(term = toString(term)) %>%
  export("Data/term_breakdown.xlsx")
