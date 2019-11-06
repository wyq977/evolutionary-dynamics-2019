RW <- function(N, sample_size, fname){
  x <- N - 2 * rbinom(sample_size, N, 0.5)
  x_normalized <- table(x)/sample_size/2
  png(fname, width = 4, height = 4, units = 'in', res = 300)
  # dot plot for random walk
  plot(x_normalized, xlab = 'loc', ylab = 'fre', main='', pch=10)
  # line plot for normal distribution
  norm_x <- (c(0:sample_size)/(sample_size/2) - 1 ) * N
  norm_y <- dnorm(norm_x, 0, sqrt(N))
  lines(norm_x, norm_y, col='red')
  dev.off()
}

RW(10, 10000, 'ex6-1b_N_10.png')
RW(100, 10000, 'ex6-1b_N_100.png')
RW(1000, 10000, 'ex6-1b_N_1000.png')
