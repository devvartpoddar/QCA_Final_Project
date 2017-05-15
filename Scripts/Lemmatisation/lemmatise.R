# Code to lemmatise the election dataset

try(setwd("/home/devvart/Desktop/QCA_Final_Project"))

source("packages.R")

# Custom Function to clean and lemmatise text
# Lemmatising text to convert to tokens
text.lemma <- function(text) {
  stop.words <- paste0("\\b", stopwords("german"), "\\b")
  
  # Removing missing text
  if (text == "") return(NA)

  text <- as.character(text) %>%
    # tolower() %>%
    stri_replace_all_regex("[:punct:]|\\d", "") %>%
    stri_replace_all_fixed("+", "") %>%
    stri_replace_all_regex(stop.words, "", vectorize_all = F) %>%
    stri_replace_all_regex("\\s+", " ") %>%
    trimws()

  # Create a lemma dataframe of the text
  ## Creating a temporary file
  file.con <- file("temp.txt")
  writeLines(text, file.con)
  close(file.con)

  # Creating temporary dataframe with lemma
  temp.data <- treetag("temp.txt",
    treetagger = "manual",
    lang = "de",
    TT.options = list(
      path = "/home/devvart/treetagger",
      preset = "de"
      ))

  temp.data <- temp.data@TT.res %>%
    select(token, lemma) %>%
    mutate(
      lemma = ifelse(lemma == "<unknown>", token, lemma),
      lemma = ifelse(lemma == "@card@", token, lemma)
      )

  file.remove("temp.txt")

  # Replacing words with their lemma
  for (x in 1:nrow(temp.data)) {
    # Values
    token <- paste0("\\b", temp.data$token[x], "\\b")
    # token <- temp.data$token[x]
    lemma <- temp.data$lemma[x]

    # Replacing
    error <- try(text %<>% stri_replace_all_regex(token, lemma))

    if (inherits(error, "try-error")) {
      message.text <- paste0(token, " ----- ", lemma)
      base::message(message.text)
      stop("Stopping cleaning until error resolves")
    }
  }

  # Removing text spaces
  text %<>% stri_replace_all_regex("\\s+", " ")

  return(text)
}

# Loading dataset
news.data <- import("Data/election_news.json") %>%
  select(-url) %>%
  mutate(date = as.Date(date))

final.data <- NULL

for (x in 11383:nrow(news.data)) {
  # Print out after every 200 iterations
  if (x %% 200 == 0) {
    message.text <- paste("Completed", round(x / nrow(news.data) * 100, 2), "%")
    base::message(message.text)

    export(final.data, "Data/lemma_text.json")

    # Sleeping for 1 min
    # Sys.sleep(60)
  }

  temp <- try(clean.text <- news.data$text[x] %>%
    text.lemma())
  
  if (inherits(temp, "try-error")) {
    clean.text <- NA
  }

  temp.data <- data.frame(
    clean.text = clean.text,
    date = as.Date(news.data$date[x])
    )

  final.data %<>%
    rbind(temp.data)
}

export(final.data, "Data/lemma_text.json")

# Example
example <- import("Data/election_news.json") %>%
  select(-url) %>%
  mutate(date = as.Date(date)) %>%
  top_n(1)

temp.text <- example$text
clean.text <- text.lemma(temp.text)

writeLines(c(temp.text, clean.text), "Data/example.txt")
