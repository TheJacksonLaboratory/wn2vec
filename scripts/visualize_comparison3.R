
# --- Regardless of P-Value 
library("ggplot2")
 

 
 # Create DataFrame from CSV file
data = read.table('/Users/niyone/Desktop/Results_visualization/bio_0_comn_concepts.tsv', sep="\t", header=T)

mean_distance_pm <- data['mean_distance_pm']
mean_distance_wn <- data['mean_distance_wn']

df_size = dim(data)[1]

count_concept_set <- 1:df_size



# Check the Datatypes


p <- (ggplot() +
  geom_point(data = data, aes(count_concept_set, mean_distance_wn), colour = 'red') +
  geom_point(data = data , aes(count_concept_set, mean_distance_pm), colour = 'blue'))


print(p + geom_jitter())



ggsave('bio_cluster_visualization.pdf')




#------ Considering P-Value 



 # Create DataFrame from CSV file
data = read.table('/Users/niyone/Desktop/Results_visualization/bio_0_comn_concepts.tsv', sep="\t", header=T)



data_frame_mod <- data[data$pval  <= 0.05,]

count_concept_set <- 1:(dim(data_frame_mod)[1])




p <- (ggplot() +
  geom_point(data = data_frame_mod, aes(count_concept_set, mean_distance_wn), colour = 'red') +
  geom_point(data = data_frame_mod , aes(count_concept_set, mean_distance_pm), colour = 'blue'))


print(p + geom_jitter())



ggsave('bio_cluster_visualization_P_Value.pdf')