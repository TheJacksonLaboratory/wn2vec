
library("ggplot2")
library("ggsci")
 
# Considering P-Value for significancy
sets_counts_per_concept_set <- c(10, 0, 54, 9, 36, 4, 25, 10, 27, 6)

concept_set_name <- rep(c( 'MeSH','Biocarta', 'KEGG', 
                                   'GO (bp)', 'PID'),each = 2)


subgroup <- rep(c("Wordnet" , "Pubtator" ))

data <- data.frame(sets_counts_per_concept_set, concept_set_name, subgroup)

ggplot(data, aes(x = concept_set_name,
           y = sets_counts_per_concept_set,
           fill = subgroup)) +
  geom_bar(stat = "identity",
           position = "dodge") +
            theme(axis.title.x = element_blank(),
                    axis.title.y = element_blank(),
                    axis.text = element_text(size = 14)) +
        scale_fill_npg()


ggsave('P_mean_significant.pdf')




#Rregardless of P-Value for Significancy 

sets_counts_per_concept_set <- c(57, 24, 178, 104, 120, 53, 133, 93, 124, 70)

concept_set_name <- rep(c( 'Mesh Sets','biocarta', 'kegg_canonical', 
                                   'bp_gene_ontology', 'pid_canonical'),each = 2)


subgroup <- rep(c("Wordnet" , "Pubtator" ))

data <- data.frame(sets_counts_per_concept_set, concept_set_name, subgroup)

ggplot(data, aes(x = concept_set_name,
           y = sets_counts_per_concept_set,
           fill = subgroup)) +
            geom_bar(stat = "identity", position = "dodge") +
            theme(axis.title.x = element_blank(),
                    axis.title.y = element_blank(),
                    axis.text = element_text(size = 14, face = "bold"))


ggsave('Regardless_P_mean_significant.pdf')