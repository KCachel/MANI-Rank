library(tidyverse)
library(extrafont)
library(RColorBrewer)
library("gridExtra")
library(ggpubr)
library(ggtext)
library(cowplot)
font_import()
loadfonts(device="win") 
CFresults <- read_csv("Malowsresults_150r_pricefairness.csv")




Multi_Fair_ILP <- CFresults %>%
  select(theta, level,cf, method) %>%
  filter(method == "Fair") %>%
  mutate(level=fct_relevel(level,c("lowf","medf","highf")))%>%
  mutate(level=recode(level,
                   `lowf`="Low-Fair",
                   `medf`= "Medium-Fair",
                   `highf`= "High-Fair"))

Greedy <- CFresults %>%
  select(theta, level,cf, method) %>%
  filter(method == "Greedy_Fair") %>%
  mutate(level=fct_relevel(level,c("lowf","medf","highf")))%>%
  mutate(level=recode(level,
                   `lowf`="Low-Fair",
                   `medf`= "Medium-Fair",
                   `highf`= "High-Fair"))


lowf_color <- "#006d2c" #"darkblue"
medf_color <- "#2ca25f" #"dodgerblue"
highf_color <- "#66c2a4" #"cadetblue3"
title_size <- 11

p_mf <- ggplot(data = Multi_Fair_ILP, aes(shape = level, color = level, order = cf)) +
  geom_line(mapping = aes(x  = theta, y = cf), size = 1)+
  geom_point(aes(x  = theta, y = cf), size = 1.75)+
  xlab("\u03B8 (Consensus)") +
  ylab("Price of Fairness")+
  theme_linedraw()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        legend.title = element_blank(),
        axis.text.y = element_text(size = 7))+
  theme(text=element_text(family="Times New Roman")) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  ggtitle("MFRA-IP")+
  scale_color_manual(values=c(lowf_color, medf_color, highf_color))+
  scale_y_continuous(labels = scales::scientific, limits = c(0,100000))

p_greedy <- ggplot(data = Greedy, aes(shape = level, color = level, order = cf)) +
  geom_line(mapping = aes(x  = theta, y = cf), size = 1)+
  geom_point(aes(x  = theta, y = cf), size = 1.75)+
  xlab("\u03B8 (Consensus)") +
  ylab("Price of Fairness")+
  theme_linedraw()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        legend.title = element_blank(),
        axis.text.y = element_text(size = 7))+
  theme(text=element_text(family="Times New Roman",)) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  ggtitle("MFRA-PostCorrect")+
  scale_color_manual(values=c(lowf_color, medf_color, highf_color))+
  scale_y_continuous(labels = scales::scientific, limits = c(0,100000))


pdfwidth <- 4.22
pdfheight <- 1.75

grDevices::cairo_pdf(file = "pricefairness_150r.pdf",   # The directory you want to save the file in
                     width = pdfwidth, # The width of the plot in inches
                     height = pdfheight) 


ggarrange(p_mf, p_greedy,
          ncol = 2, nrow = 1, common.legend = TRUE)


# Step 3: Run dev.off() to create the file!
dev.off()


