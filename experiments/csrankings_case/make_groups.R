library(readxl)
library(tidyverse)
allyr_baserankings <- read_excel("allyr_baserankings.xlsx")
csrankings_dictionary <- read_excel("csrankings_dictionary.xlsx")

group_info <- csrankings_dictionary %>% 
  mutate(id = (seq.int(nrow(csrankings_dictionary)) - 1))%>%
  mutate(Location=recode(Location,
                          `Northeast`= 0,
                          `Midwest`= 1,
                          `West`= 2,
                          `South`= 3))%>%
  mutate(Type=recode(Type,
                         `Private`= 0,
                         `Public`= 1)) 

groups <- group_info %>% 
  select(id, Location, Type)


write.table(groups, file="cs_groups.csv", row.names = FALSE, col.names = FALSE, sep = ",")

