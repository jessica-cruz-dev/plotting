###############################################################################
## Description:   Make plots of predictive validity metrics of 10 year hold out run
##
## Inputs:        Predictive validity metrics for tb_latent run (pre and post shift)
##
## Output:        PDF of plots 
###############################################################################




require(data.table)
require(ggplot2)

save_file <- '/path/to/tb_latent_stats.pdf'
pdf(save_file, width = 14, height = 8)



# 2a. hold out results by age group
pv <- read.csv(file = '/path/to/age_rmse_plot.csv')
p <- ggplot(pv, aes(x = pv.f, y = rmse, color = sex_id )) +
          scale_color_manual(values=c("#56B4E9",  "#E69F00")) +
          guides(fill=guide_legend(title="sex_id")) +
          facet_grid(~sample) +
          geom_point() + geom_line() +
          labs(title='10 yr hold out RMSE by age group (with shift)') +
          theme(
            axis.title=element_blank(),
            axis.text.x=element_text(angle=45, hjust=1)
        )
print(p)


# 2a. hold out results by region
pv <- read.csv(file = '/path/to/sr_postshift.csv')
p <- ggplot(pv, aes(x = pv.f, y = rmse, color = sex_id )) +
          scale_color_manual(values=c("#56B4E9",  "#E69F00")) +
          guides(fill=guide_legend(title="sex_id")) +
          facet_grid(~sample) +
          geom_point() + geom_line() +
          labs(title='10 yr hold out RMSE by super region (with shift)') +
          theme(
            axis.title=element_blank(), 
            axis.text.x=element_text(angle = 45, hjust = 1)
        )
print(p)



# 2b. hold out pre-shift results by age group
pv <- read.csv(file = '/path/to/age_rmse_plot_pre_shift.csv')
p <- ggplot(pv, aes(x = pv.f, y = rmse, color = sex_id )) +
          scale_color_manual(values=c("#56B4E9",  "#E69F00")) +
          guides(fill=guide_legend(title="sex_id")) +
          facet_grid(~sample) +
          geom_point() + geom_line() +
          labs(title='10 yr hold out RMSE by age group (pre-shift)') +
          theme(
            axis.title=element_blank(),
            axis.text.x=element_text(angle = 45, hjust = 1)
        )
print(p)


# 2b. hold out pre-shift  results by region
pv <- read.csv(file = '/path/to/sr_rmse_plot_pre_shift.csv')
p <- ggplot(pv, aes(x = pv.f, y = rmse, color = sex_id )) +
          scale_color_manual(values=c("#56B4E9",  "#E69F00")) +
          guides(fill=guide_legend(title="sex_id")) +
          facet_grid(~sample) +
          geom_point() + geom_line() +
          labs(title='10 yr hold out RMSE by super region (pre-shift)') +
          theme(
            axis.title=element_blank(),
            axis.text.x=element_text(angle = 45, hjust = 1)
        )
print(p)


# version 1,rmse  overall stats
pv <- read.csv(file = '/plot/to/rmse_overall.csv')
p <- ggplot(pv, aes(x = shift, y = value, color = sample )) +
          scale_color_manual(values=c("#56B4E9",  "#E69F00")) +
          guides(fill=guide_legend(title="sample")) +
          facet_grid(~sex) +
          geom_point() + geom_line() +
          labs(title='RMSE overall stats') +
          theme(
            axis.title=element_blank(),
            axis.text.x=element_text(angle = 45, hjust = 1)
        )
print(p)

pv <- read.csv(file = '/path/to/r2_overall.csv')
p <- ggplot(pv,aes(x = shift, y = value, color = sample )) +
          scale_color_manual(values=c("#56B4E9",  "#E69F00")) +
          guides(fill=guide_legend(title="sample")) +
          facet_grid(~sex) +
          geom_point() + geom_line() +
          labs(title='R2 overall stats') +
          theme(
            axis.title=element_blank(),
            axis.text.x=element_text(angle = 45, hjust = 1)
        )
print(p)

dev.off()
