library("ggplot2")
library("ggsci")

if(!require('ggpubr')) {
  install.packages('ggpubr')
  library('ggpubr')
}

# Considering P-Value for significancy
sets_counts_per_concept_set <- c(13, 9, 32, 12, 35, 13, 36, 27, 29, 5)

concept_set_name <- rep(c('MeSH', 'Biocarta', 'KEGG', 'GO (bp)', 'PID'), each = 2)
sets_counts_per_concept_set2 <- c(46, 42, 154, 131, 112, 70, 147, 125, 115, 79)

subgroup <- rep(c("Wordnet", "Pubtator"))

data <- data.frame(sets_counts_per_concept_set, concept_set_name, subgroup)


p1 <- ggplot(data, aes(x = concept_set_name,
           y = sets_counts_per_concept_set,
           fill = subgroup)) +
            geom_bar(stat = "identity", position = "dodge") +
            scale_fill_nejm() + theme_bw() +
            theme(axis.title.x = element_blank(), 
                  axis.title.y = element_blank(), 
                  axis.text = element_text(size = 10),
                  legend.text = element_text(size = 15),
                  plot.title = element_text(size = 10)) +
            labs(color = NULL) +
            guides(fill = guide_legend(title = NULL)) +
            ylim(0, max(sets_counts_per_concept_set, sets_counts_per_concept_set2)) +
            labs(title = "Significant")

#Rregardless of P-Value for Significancy 

sets_counts_per_concept_set2 <- c(46, 42, 154, 131, 112, 70, 147, 125, 115, 79)

data2 <- data.frame(sets_counts_per_concept_set2, concept_set_name, subgroup)

p2 <- ggplot(data2, aes(x = concept_set_name,
           y = sets_counts_per_concept_set2,
           fill = subgroup)) +
            geom_bar(stat = "identity", position = "dodge") +
            scale_fill_nejm() + theme_bw() +
            theme(axis.title.x = element_blank(), 
                  axis.title.y = element_blank(), 
                  axis.text = element_text(size = 10),
                  legend.text = element_text(size = 20),
                  plot.title = element_text(size = 10)) +
            guides(fill = guide_legend(title = NULL)) +
            ylim(0, max(sets_counts_per_concept_set, sets_counts_per_concept_set2)) +
            labs(title = "All comparisons")




ggarrange(p1, p2, common.legend = TRUE)
ggsave('mean_comparision.png')
ggsave('mean_comparision.pdf')



library(ggplot2)
library(ggpubr)

# Create DataFrame from CSV file
data = read.table('/Users/niyone/Desktop/wn2vec/dump/pid_2010_comn_concepts.tsv', sep="\t", header=T)

mean_distance_pm <- data['mean_distance_pm']
mean_distance_wn <- data['mean_distance_wn']

data$mean_diff <- (data$mean_distance_pm) - (data$mean_distance_wn)

data_frame_mod <- data[data$pval  <= 0.05,]

p3 <- ggplot(data_frame_mod, aes(x = "", y = mean_diff)) +
  scale_fill_nejm() + 
  theme_bw() +
  theme(axis.title.x = element_blank(), 
        axis.title.y = element_blank(), 
        axis.text = element_text(size = 15),
        axis.title = element_text(size = 15),
        panel.grid.major = element_line(size = 2),
        panel.grid.minor = element_line(size = 1),
        plot.title = element_text(size = 15)) +
  geom_jitter(size = 3) +
  geom_hline(yintercept = mean(data_frame_mod$mean_diff, na.rm=TRUE), color='red')+
  labs(title = "Significant", size=10)

p4 <- ggplot(data, aes(x = "", y = mean_diff)) +
  scale_fill_nejm() + 
  theme_bw() +
  theme(axis.title.x = element_blank(), 
        axis.title.y = element_blank(), 
        axis.text = element_text(size = 15),
        axis.title = element_text(size = 15),
        panel.grid.major = element_line(size = 2),
        panel.grid.minor = element_line(size = 1),
        plot.title = element_text(size = 15)) +
  geom_jitter(size = 3) +
  geom_hline(yintercept = mean(data$mean_diff, na.rm=TRUE), color='red')+
  labs(title = "All comparisons", size=10)


ggarrange(p3, p4)

ggsave('pid_mean_diff.png')
ggsave('pid_mean_diff.pdf')
