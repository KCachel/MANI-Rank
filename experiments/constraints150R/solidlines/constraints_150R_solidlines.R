library(cowplot)
library(tidyverse)
library(readr)
library("gridExtra")
library(ggpubr)
library(ggtext)

setwd("~/OneDrive - Worcester Polytechnic Institute (wpi.edu)/PycharmProjects/multi_fair_rank_agg/experiments/constraints150R/solidlines")
Malowsresults_150r_constraints <- read_csv("~/OneDrive - Worcester Polytechnic Institute (wpi.edu)/PycharmProjects/multi_fair_rank_agg/experiments/constraints150R/Malowsresults_150r_constraints.csv")

cleanResults <- Malowsresults_150r_constraints %>%
  rename('\u0394 (desired fairness)' = threshold, Gender = maxdifparity_gender , Race = maxdifparity_race, `Intersection (Race x Gender)` = maxdifparity_intersectional) %>%
  select(theta, method, Gender, Race, `Intersection (Race x Gender)`,'\u0394 (desired fairness)', level) %>%
  pivot_longer(cols = c("Gender", "Race", "Intersection (Race x Gender)", "\u0394 (desired fairness)"), names_to = "attribute", values_to = "score") %>%
  mutate(attribute=fct_relevel(attribute,c("\u0394 (desired fairness)","Gender","Race", "Intersection (Race x Gender)")))



kemenyResults <- cleanResults %>%
  filter(method == "Kemeny")

kemenyResults_LF <- kemenyResults %>%
  filter(level == "lowf")


kemenyResults_MF <- kemenyResults %>%
  filter(level == "medf")
kemenyResults_HF <- kemenyResults %>%
  filter(level == "highf")

pt_size <- 2
title_size <- 10
lowf <- "Low-Fair"
medf <- "Medium-Fair"
highf <- "High-Fair"
pdfwidth <- 3.75 #3.75
pdfheight <- 1.5 #1.5
fairnessarea <- "#b2df8a"
race_clr <- "mediumblue"
gender_clr <- "gray17"
inter_clr <- "#ff7f0e"
linesize <- .5

p_kem_lf <- ggplot(kemenyResults_LF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.9)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(lowf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))



p_kem_mf <- ggplot(kemenyResults_MF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.9)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(medf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))


p_kem_hf <- ggplot(kemenyResults_HF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.9)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(highf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))

grDevices::cairo_pdf(file = "kemeny_constraints.pdf",   # The directory you want to save the file in
                     width = pdfwidth, # The width of the plot in inches
                     height = pdfheight) 

ggarrange(p_kem_lf, p_kem_mf, p_kem_hf,
          ncol = 3, nrow = 1,
          common.legend = FALSE)
# Step 3: Run dev.off() to create the file!
dev.off()


#########################

paResults <- cleanResults %>%
  filter(method == "PA-Fair")

paResults_LF <- paResults %>%
  filter(level == "lowf")


paResults_MF <- paResults %>%
  filter(level == "medf")
paResults_HF <- paResults %>%
  filter(level == "highf")


p_pa_lf <- ggplot(paResults_LF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  scale_y_continuous(labels = scales::number_format(accuracy = 0.01), limits = c(0,.4))+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(lowf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))



p_pa_mf <- ggplot(paResults_MF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  scale_y_continuous(labels = scales::number_format(accuracy = 0.01), limits = c(0,.4))+
  #ylim(0,.4)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(medf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))

p_pa_hf <- ggplot(paResults_HF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  scale_y_continuous(labels = scales::number_format(accuracy = 0.01), limits = c(0,.4))+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(highf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))

grDevices::cairo_pdf(file = "pa_constraints.pdf",   # The directory you want to save the file in
                     width = pdfwidth, # The width of the plot in inches
                     height = pdfheight) 


ggarrange(p_pa_lf, p_pa_mf, p_pa_hf,
          ncol = 3, nrow = 1,
          common.legend = FALSE)

# Step 3: Run dev.off() to create the file!
dev.off()


#########################

interResults <- cleanResults %>%
  filter(method == "Inter-Fair")

interResults_LF <- interResults %>%
  filter(level == "lowf")

interResults_MF <- interResults %>%
  filter(level == "medf")
interResults_HF <- interResults %>%
  filter(level == "highf")


p_inter_lf <- ggplot(interResults_LF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.2)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(lowf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))



p_inter_mf <- ggplot(interResults_MF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.2)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(medf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))


p_inter_hf <- ggplot(interResults_HF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.2)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(highf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))


grDevices::cairo_pdf(file = "inter_constraints.pdf",   # The directory you want to save the file in
                     width = pdfwidth, # The width of the plot in inches
                     height = pdfheight) 


ggarrange(p_inter_lf, p_inter_mf, p_inter_hf,
          ncol = 3, nrow = 1,
          common.legend = FALSE)


# Step 3: Run dev.off() to create the file!
dev.off()



#########################

multiResults <- cleanResults %>%
  filter(method == "Multi-Fair")

multiResults_LF <- multiResults %>%
  filter(level == "lowf")


multiResults_MF <- multiResults %>%
  filter(level == "medf")
multiResults_HF <- multiResults %>%
  filter(level == "highf")


p_multi_lf <- ggplot(multiResults_LF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.2)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(lowf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))



p_multi_mf <- ggplot(multiResults_MF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.2)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(medf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))


p_multi_hf <- ggplot(multiResults_HF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.2)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(highf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))




grDevices::cairo_pdf(file = "multi_constraints.pdf",   # The directory you want to save the file in
                     width = pdfwidth, # The width of the plot in inches
                     height = pdfheight) 


ggarrange(p_multi_lf, p_multi_mf, p_multi_hf,
          ncol = 3, nrow = 1,
          common.legend = FALSE)


# Step 3: Run dev.off() to create the file!
dev.off()

#########################

greedyResults <- cleanResults %>%
  filter(method == "Greedy_Fair")

greedyResults_LF <- greedyResults %>%
  filter(level == "lowf")


greedyResults_MF <- greedyResults %>%
  filter(level == "medf")
greedyResults_HF <- greedyResults %>%
  filter(level == "highf")


p_greedy_lf <- ggplot(greedyResults_LF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.2)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(lowf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15, 19, 23, 8) ) ))



p_greedy_mf <- ggplot(greedyResults_MF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.2)+
  theme(legend.position = "none",
        legend.direction = "vertical")+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  ggtitle(medf) +
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))


p_greedy_hf <- ggplot(greedyResults_HF, aes(shape = attribute, color = attribute, linetype = attribute)) +
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = .1, fill = fairnessarea, color = NA)+
  geom_point(aes(x  = theta, y = score), size = pt_size)+
  geom_line(mapping = aes(x  = theta, y= score), size = linesize)+
  xlab("\u03B8 (Consensus)") +
  ylab("ARP/IRP score")+
  theme_linedraw()+
  ylim(0,.2)+
  theme(legend.position = "top",
        legend.direction = "horizontal", 
        legend.text = element_text(size = 14))+
  theme(text=element_text(family="Times New Roman")) + 
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.text = element_markdown())+
  guides(color=guide_legend(nrow=2))+
  guides(shape = guide_legend(nrow = 2))+
  scale_shape_manual("attribute", values =c(NA,  19, 23, 8))+
  scale_color_manual("attribute", values=c(fairnessarea,gender_clr, race_clr, inter_clr))+
  scale_linetype_manual("attribute", values=c(NA, "solid", "solid", "solid"))+
  #ggtitle(highf) +
  ggtitle("Legend")+
  theme(plot.title = element_text(hjust=0, size=title_size))+
  #guides(linetype = guide_legend(override.aes = list(linetype = c(NA, 0, 0, 0) ) ))+
  guides(color = guide_legend(override.aes = list(shape = c(15,  19, 23, 8) ) ))




grDevices::cairo_pdf(file = "post_constraints.pdf",   # The directory you want to save the file in
                     width = pdfwidth, # The width of the plot in inches
                     height = pdfheight) 


ggarrange(p_greedy_lf, p_greedy_mf, p_greedy_hf,
          ncol = 3, nrow = 1,
          common.legend = FALSE)


# Step 3: Run dev.off() to create the file!
dev.off()