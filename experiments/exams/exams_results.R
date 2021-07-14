library(tidyverse)
library(readr)
setwd("~/OneDrive - Worcester Polytechnic Institute (wpi.edu)/PycharmProjects/multi_fair_rank_agg/experiments/exams")
exam_results_raw <- read_csv("exam_results.csv")


exam_results <- exam_results_raw %>% 
  rename(`intersection (gender x race x lunch)` = irp) %>%
  mutate(method_group = recode(method_group, `base_rank` ="Base Rankings")) %>%
  pivot_longer(cols = c("gender", "race", "lunch", "intersection (gender x race x lunch)"), names_to = "attribute", values_to = "score") %>%
  mutate(rank_type=recode(rank_type,
                      `kemeny`="kemeny consensus",
                      `Multi-Fair`= "fair consensus",
                      `greedy_fair`= "fair consensus")) %>%
  mutate(method_group=recode(method_group,
                          `Kemeny`="Kemeny",
                          `Multi-Fair`= "MFRA-IP",
                          `greedy_fair`= "MFRA-PC"))%>%
  mutate(attribute=fct_relevel(attribute,c("gender", "race", "lunch", "intersection (gender x race x lunch)")))



pdfwidth <- 3.75
pdfheight <- 3
gender_clr <- "mediumblue"
lunch_clr <- "gray17"
race_clr <- "#8c564b"
intersection_clr <- "#ff7f0e"
grDevices::cairo_pdf(file = "exam_results.pdf",   # The directory you want to save the file in
                     width = pdfwidth, # The width of the plot in inches
                     height = pdfheight) 

ggplot(exam_results, aes(rank_type, score, color = attribute)) + 
  geom_point(aes(shape = attribute), size = 3)+
  facet_grid(cols = vars(method_group), scales = "free", space = "free")+
  theme_linedraw()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        legend.title = element_blank(),
        legend.text = element_text(size = 10),
        strip.background = element_rect(fill="white"))+
  guides(color=guide_legend(nrow=2))+
  guides(shape = guide_legend(nrow = 2))+
  scale_shape_manual("attribute", values =c(19, 17, 15, 8))+
  theme(strip.text.x = element_text(size = 8, color = "black"))+
  ylab("ARP/IRP score")+
  xlab("")+
  theme(text=element_text(family="Times New Roman"))+
  scale_color_manual(values=c(gender_clr,lunch_clr, race_clr, intersection_clr))+
  scale_x_discrete(labels = function(x) str_wrap(x, width = 4))

# Step 3: Run dev.off() to create the file!
dev.off()
