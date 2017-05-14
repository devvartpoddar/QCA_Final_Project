# Intialisation
rm(list = ls())
pkgs <- c('dplyr', 'magrittr', 'methods', 'rvest', 'stringi', 'rio', 'gmailr', 'koRpus',
  'quanteda', 'topicmodels', 'tidytext', 'lubridate')

for (p in pkgs) {
  load <- require(p, character.only = T, quietly = T)

  if (!load) {
    install.packages(p)
    require(p, character.only = T, quietly = T)
  }
}
rm(pkgs, p)
