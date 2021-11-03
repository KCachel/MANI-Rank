library(PerMallows)
library(dplyr)
#central ranking corresponds to scenario with attributes max dif in rpar being close and intersection matching race
a1 <- c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2)
a2 <- c(0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1,
        2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3,
        4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0,
        1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2,
        3, 4)
df <- data.frame(a1, a2)
df <- df %>% mutate(a1=recode(a1,
                              `0`="Man",
                              `1`= "Woman",
                              `2`= "Non-Binary"))
df <- df %>% mutate(a2=recode(a2,
                              `0`="Black",
                              `1`= "White",
                              `2`= "AlaskaNat",
                              `3`= "Asian",
                              `4`= "NatHaawai"))

my_table_0 <- table(df$a1, df$a2)
print.table(my_table_0)

central_ranking <- c(25, 5, 10, 20, 15, 0, 70, 75, 80, 85, 60, 23, 24, 65, 2, 4, 69, 72, 8, 27, 3, 74, 77, 7, 68, 67, 78, 79, 9, 87, 13, 84, 14, 73, 17, 83, 22, 18, 28, 29, 19, 40, 82, 88, 16, 89, 6, 26, 50, 35, 30, 12, 21, 55, 62, 45, 64, 63, 1, 32, 34, 33, 37, 38, 76, 11, 39, 42, 43, 81, 71, 44, 47, 86, 48, 49, 52, 53, 54, 59, 57, 58, 61, 66, 31, 36, 41, 46, 51, 56)
central_ranking <- central_ranking + 1  #handle 1 indexing 
R <- rmm(150,central_ranking,.2,"kendall", "distances")
R <- R - 1
R <- data.frame(R)

write.table(R, file="Rtheta_2.csv", row.names = FALSE, col.names = FALSE, sep = ",")
