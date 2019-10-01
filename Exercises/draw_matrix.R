write_matex_name <- function(x) {
  if (is.null(colnames(x))) {x_col <- seq(ncol(x))} else {x_col <- colnames(x)}
  if (is.null(rownames(x))) {x_row <- seq(nrow(x))} else {x_row <- rownames(x)}
  begin <- "\\begin{blockarray}"
  col_p <- paste(rep("c", length(x_col)+1), collapse = "")
  begin <- paste(begin, "{", col_p, "}", paste(x_col, collapse = "&"), sep="")
  begin <- paste(begin, "\\\\",sep="")
  begin <- paste(begin,paste("\\begin{block}{[", paste(rep("c", length(x_col)), collapse = ""),"]c}", sep=""))
  begin
  end <- "\\end{block}\\end{blockarray}"
  res <- ""
  for (i in 1:nrow(x)) {
    eachrow = x[i,1]
    for (j in 2:ncol(x)) {
      eachrow <- paste(eachrow, x[i,j], sep = '&')
    }
    eachrow <- paste(eachrow, x_row[i], sep = '&')
    eachrow <- paste(eachrow, "\\\\", sep="")
    res <- paste(res, eachrow, sep="")
  }
  
  paste(c(begin, res, end), collapse = "")
  
}

write_matex <- function(x) {
  begin <- "\\begin{bmatrix}"
  end <- "\\end{bmatrix}"
  X <-
    apply(x, 1, function(x) {
      paste(
        paste(x, collapse = "&"),
        "\\\\"
      )
    })
  paste(c(begin, X, end), collapse = "")
}