library("ggplot2")
library("ggsci")

if(!require('ggpubr')) {
  install.packages('ggpubr')
  library('ggpubr')
}

# Considering P-Value for significancy
sets_counts_per_concept_set <- c(10, 0, 54, 9, 36, 4, 25, 10, 27, 6)

concept_set_name <- rep(c('MeSH', 'Biocarta', 'KEGG', 'GO (bp)', 'PID'), each = 2)
sets_counts_per_concept_set2 <- c(57, 24, 178, 104, 120, 53, 133, 93, 124, 70)

subgroup <- rep(c("Wordnet", "Pubtator"))

data <- data.frame(sets_counts_per_concept_set, concept_set_name, subgroup)


p1 <- ggplot(data, aes(x = concept_set_name,
           y = sets_counts_per_concept_set,
           fill = subgroup)) +
            geom_bar(stat = "identity", position = "dodge") +
            scale_fill_nejm() + theme_bw() +
            theme(axis.title.x = element_blank(), 
                  axis.title.y = element_blank(), 
                  axis.text = element_text(size = 15)) +
            labs(color = NULL) +
            guides(fill = guide_legend(title = NULL)) +
            ylim(0, max(sets_counts_per_concept_set, sets_counts_per_concept_set2))

#Rregardless of P-Value for Significancy 

sets_counts_per_concept_set2 <- c(57, 24, 178, 104, 120, 53, 133, 93, 124, 70)

data2 <- data.frame(sets_counts_per_concept_set2, concept_set_name, subgroup)

p2 <- ggplot(data2, aes(x = concept_set_name,
           y = sets_counts_per_concept_set2,
           fill = subgroup)) +
            geom_bar(stat = "identity", position = "dodge") +
            scale_fill_nejm() + theme_bw() +
            theme(axis.title.x = element_blank(), 
                  axis.title.y = element_blank(), 
                  axis.text = element_text(size = 15)) +
            guides(fill = guide_legend(title = NULL)) +
            ylim(0, max(sets_counts_per_concept_set, sets_counts_per_concept_set2))


print(ggarrange(p1, p2, common.legend = TRUE))
