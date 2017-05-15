library(rio)

setwd("C:/RajuPC/Content Analysis/Final/QCA_Final_Project")

term_breakdown <- rio::import("C:/RajuPC/Content Analysis/Final/QCA_Final_Project/Data/term_breakdown.json")

export(term_breakdown, "term_breakdown.csv")

term_breakdown_eng <- read.csv("C:/RajuPC/Content Analysis/Final/QCA_Final_Project/term_breakdown_eng.csv")
