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

central_ranking <- c(25, 70, 75, 80, 5, 85, 10, 15, 24, 4, 23, 67, 68, 69, 72, 73, 74, 77, 78, 79, 3, 82, 20, 2, 7, 83, 9, 84, 71, 8, 30, 76, 13, 27, 1, 87, 26, 45, 14, 88, 17, 40, 35, 50, 6, 81, 89, 18, 55, 19, 0, 16, 22, 28, 29, 32, 33, 86, 21, 34, 37, 60, 38, 39, 42, 31, 65, 43, 44, 47, 48, 49, 52, 53, 36, 54, 57, 41, 59, 58, 12, 46, 62, 63, 64, 51, 56, 11, 61, 66)
central_ranking <- central_ranking + 1  #handle 1 indexing 
R <- rmm(150,central_ranking,.2,"kendall", "distances")
R <- R - 1
R <- data.frame(R)

write.table(R, file="Rtheta_2.csv", row.names = FALSE, col.names = FALSE, sep = ",")