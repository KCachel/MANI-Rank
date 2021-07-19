library(tidyverse)
library(readr)
csrankings_results <- read_csv("csrankings_results.csv")


csrankings <- csrankings_results %>% 
  rename('intersection (location x type)' = irp) %>%
  mutate(method_group = recode(method_group, `base_rank` ="Base Rankings")) %>%
  pivot_longer(cols = c("location", "type", "intersection (location x type)"), names_to = "attribute", values_to = "score")%>%
  mutate(rank_type=recode(rank_type,
                          `kemeny`="kemeny consensus",
                          `Multi-Fair`= "fair consensus",
                          `greedy_fair`= "fair consensus")) %>%
  mutate(method_group=recode(method_group,
                             `Kemeny`="Kemeny",
                             `Multi-Fair`= "MFRA- IP",
                             `greedy_fair`= "MFRA- PC"))%>%
  mutate(attribute=fct_relevel(attribute,c("location", "type", "intersection (location x type)")))

  
pdfwidth <- 9.5
pdfheight <- 3
location_clr <- "mediumblue"
type_clr <- "gray17"
intersection_clr <- "#ff7f0e"

grDevices::cairo_pdf(file = "csrankings_results_ref.pdf",   # The directory you want to save the file in
                     width = pdfwidth, # The width of the plot in inches
                     height = pdfheight, fallback_resolution=600) 


ggplot(csrankings, aes(rank_type, score, color = attribute)) + 
  geom_point(aes(shape = attribute), size = 3)+
  facet_grid(cols = vars(method_group), scales = "free", space = "free", shrink = TRUE, labeller = label_wrap_gen(width = 4))+
  theme_linedraw()+
  theme(legend.position = "top",
        legend.direction = "horizontal",
        legend.title = element_blank(),
        legend.text = element_text(size = 14),
        strip.background = element_rect(fill="white"))+
  scale_shape_manual("attribute", values =c(19, 17, 8))+
  theme(strip.text.x = element_text(size = 8, color = "black"))+
  theme(axis.text.x = element_text(angle=35))+
  ylab("ARP/IRP score")+
  xlab("")+
  theme(text=element_text(family="Times New Roman"))+
  scale_color_manual(values=c(location_clr, type_clr , intersection_clr))+
  scale_x_discrete(labels = function(x) str_wrap(x, width = 4))


# Step 3: Run dev.off() to create the file!
dev.off()
