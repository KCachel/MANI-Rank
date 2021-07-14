library(PerMallows)
library(dplyr)


central_ranking <- c(10, 20, 0, 70, 80, 60, 24, 2, 4, 8, 14, 68, 18, 74, 25, 28, 78, 5, 22, 15, 40, 50, 30, 82, 72, 75, 84, 88, 12, 85, 6, 23, 26, 16, 3, 7, 76, 73, 86, 62, 69, 65, 67, 27, 79, 83, 13, 87, 9, 32, 64, 19, 77, 17, 34, 38, 29, 42, 89, 44, 58, 48, 52, 54, 45, 35, 55, 63, 66, 1, 21, 36, 33, 46, 56, 39, 37, 43, 47, 59, 49, 53, 57, 11, 71, 81, 61, 31, 41, 51)
central_ranking <- central_ranking + 1  #handle 1 indexing 
R <- rmm(100,central_ranking,.8,"kendall", "distances")
R <- R - 1
R <- data.frame(R)

write.table(R, file="Rtheta_8lotsatr.csv", row.names = FALSE, col.names = FALSE, sep = ",")