library(dplyr)
library(readr)
library(stringr)
schools <- read_csv(file = 'schools.csv', trim_ws = TRUE)
schools <- apply(schools,MARGIN=c(1,2), str_trim)
schools <- apply(schools,MARGIN=c(1,2), str_squish)

yr2000 <-read_csv(file = '2000rankings.csv', trim_ws = TRUE)
yr2000 <- apply(yr2000,MARGIN=c(1,2), str_trim)
yr2000 <- apply(yr2000,MARGIN=c(1,2), str_squish)
yr2000 <- gsub('.{2}$', '', yr2000)

clean2000 <- merge(yr2000,schools, by = "School", sort = FALSE)

notin <- setdiff(schools, clean2000$School)


