library(tidyverse)

exams <- read_csv("exams.csv")

#Make group key

exam_groups <- exams %>% mutate(gender=recode(gender,
                              `male`= 0,
                              `female`= 1))
exam_groups <- exam_groups %>% mutate(race=recode(race,
                              `group A`= 0,
                              `group B`= 1,
                              `group C`= 2,
                              `group D`= 3,
                              `group E`= 4))
exam_groups <- exam_groups %>% mutate(lunch=recode(lunch,
                                              `free/reduced`= 0,
                                              `standard`= 1))

exam_group_key <- data.frame(exam_groups$candidate_id, exam_groups$gender, exam_groups$race, exam_groups$lunch)

write.table(exam_group_key, file="exam_group_key.csv", row.names = FALSE, col.names = FALSE, sep = ",")
#Make base rankings

math <- data.frame(exam_groups$candidate_id, exam_groups$math_score)
math_sorted_df <- arrange(math, exam_groups$math_score)
math_sorted <- math_sorted_df$exam_groups.candidate_id

reading <- data.frame(exam_groups$candidate_id, exam_groups$reading_score)
reading_sorted_df <- arrange(reading, exam_groups$reading_score)
reading_sorted <- reading_sorted_df$exam_groups.candidate_id

writing <- data.frame(exam_groups$candidate_id, exam_groups$writing_score)
writing_sorted_df <- arrange(writing, exam_groups$writing_score)
writing_sorted <- writing_sorted_df$exam_groups.candidate_id

exam_base_rankings <- data.frame(math_sorted, reading_sorted, writing_sorted)
write.table(exam_base_rankings, file="exam_base_rankings.csv", row.names = FALSE, col.names = FALSE, sep = ",")

