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

central_ranking <- c(35, 23, 25, 5, 24, 3, 70, 75, 67, 69, 32, 68, 73, 10, 72, 74, 4, 15, 30, 85, 2, 71, 79, 81, 26, 20, 78, 6, 77, 82, 80, 7, 76, 84, 34, 9, 1, 83, 87, 37, 13, 88, 89, 39, 27, 33, 38, 8, 17, 45, 14, 86, 42, 31, 40, 18, 19, 22, 47, 43, 44, 28, 29, 36, 16, 41, 50, 48, 49, 46, 55, 54, 52, 21, 53, 59, 0, 51, 57, 58, 12, 56, 11, 60, 65, 62, 63, 64, 61, 66)
central_ranking <- central_ranking + 1  #handle 1 indexing 
R <- rmm(150,central_ranking,.2,"kendall", "distances")
R <- R - 1
R <- data.frame(R)

write.table(R, file="Rtheta_2.csv", row.names = FALSE, col.names = FALSE, sep = ",")