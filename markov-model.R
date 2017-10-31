library(dplyr)
library(reshape2)
library(ggplot2)
library(ChannelAttribution)
library(markovchain)


df1 <- read.csv("data/user_path_df.csv")

channel_column = "CHANNEL_NAME"  # "CHANNEL_NAME" 
# calculating the models
mod1 <- markov_model(df1,
                     var_path = channel_column,
                     var_conv = 'conv',
                     var_null = 'no_conv',
                     out_more = TRUE)

# extracting the results of attribution
df_res1 <- mod1$result

# extracting a transition matrix
df_trans1 <- mod1$transition_matrix
df_trans1 <- dcast(df_trans1, channel_from ~ channel_to, value.var = 'transition_probability')
write.csv(df_res1, file = "markov_chain_result.csv")
write.csv(df_trans1, file = "trans1.csv")
