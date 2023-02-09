library(ggplot2)
library(dplyr)
library(plyr)
library(tidyr)
library(RColorBrewer)

# Input the output file from the compare_embeddings.py script
dat <- read.table("comn_concepts.tsv", sep="\t", header=T)

# First do binomial test for random chance =0.5

k <- sum(dat$mean_distance_pm > dat$mean_distance_wn)
n <- dim(dat)[1]
binom.test(k, n)

## Paired t test
t.test(dat$mean_distance_wn, dat$mean_distance_pm, paired=TRUE, alternative="less")

dat <- dat %>% pivot_longer(cols=c('mean_distance_pm', 'mean_distance_wn'),names_to = "embedding", 
    values_to ="distance")
dat <- dat[c("embedding", "distance")]
dat$embedding[dat$embedding == 'mean_distance_pm'] <- 'Pubtator'
dat$embedding[dat$embedding == 'mean_distance_wn'] <- 'Wordnet'

# to calculate sd etc
data_summary <- function(data, varname, groupnames){
  #require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      sd = sd(x[[col]], na.rm=TRUE))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
 return(data_sum)
}

df3 <- data_summary(dat, varname="distance", 
                    groupnames=c("embedding"))
# Convert dose to a factor variable
df3$dose=as.factor(df3$embedding)
head(df3)

p <- ggplot(df3, aes(x=embedding, y=distance, fill=embedding)) + 
   geom_bar(stat="identity", position=position_dodge(), width=0.6) +
  geom_errorbar(aes(ymin=distance-sd, ymax=distance+sd), width=.05, position=position_dodge(.9)) +
  theme_minimal() +
  scale_fill_brewer(palette = "Dark2") +
  theme(axis.text=element_text(size=24),
        axis.title=element_blank(),
        legend.position = "none")
ggsave('pt_vs_wn.pdf')
    
  
## DO stats
t.test(dat$distance[dat$embedding=="Pubtator"], dat$distance[dat$embedding=="Wordnet"])


dat$embedding[dat$embedding == 'mean_distance_pm'] <- 'Pubtator'
dat$embedding[dat$embedding == 'mean_distance_wn'] <- 'Wordnet'


