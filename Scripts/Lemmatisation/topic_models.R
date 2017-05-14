# Topic modelling the lemmatised text

try(setwd("/home/devvart/Desktop/QCA_Final_Project"))
try(setwd("/home/devvart/QCA_Final_Project"))

source("packages.R")

# Setting up mail capabilities
## Copy mail settings
file.copy('~/Dropbox/.httr-oauth', '.', overwrite = TRUE)

## Force authentication
use_secret_file('~/Dropbox/gmail_outh.json')
gmail_auth()

# Writing mail
mime() %>%
  to('devvart123@gmail.com') %>%
  from('devvart.server@gmail.com') %>%
  cc('') %>%
  subject('[R:Server]: Topic Models') %>%
  text_body('Starting topic modelling') %>%
  send_message()

# Cleaning more common words
clean <- c("berlin", "bundestag", "dass", "deutsch", "deutschland", "erst", "geben",
           "gehen", "gut", "immer", "kommen", "land", "mehr", "neu", "schon", "sollen",
           "woche", letters)

# Loading data and final cleaning

text.data <- import("Data/lemma_text.json") %>%
  mutate(date = as.Date(date),
         year = year(date)) %>%
  filter(!is.na(clean.text)) %>%
  select(-date) %>%
  # sample_frac(0.02) %>%
  mutate(clean.text = tolower(clean.text)) %>%
  rename(text = clean.text)


# Creating document term matrix
error <- try({
  temp <- corpus(text.data) %>%
    dfm(remove = c(stopwords("german"), clean), 
        remove_punct = TRUE) %>%
    dfm_trim(min_docfreq = 0.005) %>%
  convert(to = "topicmodels")

  topic.model <- LDA(temp,
                     k = 100,
                     control = list(seed = 1236,
                                    alpha = 0.8))
  })

if (inherits(error, "try-error")) {
  # Writing mail
  mime() %>%
    to('devvart123@gmail.com') %>%
    from('devvart.server@gmail.com') %>%
    cc('') %>%
    subject('[R:Server]: Error :(') %>%
    text_body(
      paste('There was an error with the code. Look at: \n',
        attr(error, "condition"))
      ) %>%
    send_message()

  stop()
}

# getting the topics for each of the rows
text_topics <- topics(topic.model)

# Term wise distribution of the topics
trial <- tidy(topic.model, matrix = "beta") %>%
  group_by(topic) %>%
  top_n(50, beta) %>%
  arrange(topic, -beta)

# Exporting the terms
export(trial, "Data/term_breakdown.json")

# Exporting the topic distribution
final.data <- cbind(
  year = text.data$year,
  text_topics
) %>%
  as.data.frame()

export(final.data, "Data/topic_dist.json")

# Writing mail
mime() %>%
  to('devvart123@gmail.com') %>%
  from('devvart.server@gmail.com') %>%
  cc('') %>%
  subject('[R:Server]: Success!!') %>%
  text_body('Topic Models are now complete!') %>%
  send_message()

