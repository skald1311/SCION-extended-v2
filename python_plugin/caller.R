library(jsonlite)

# Create a list or data frame
input_data <- list(name = "Gene", value = 42)

# Convert to JSON
json_input <- toJSON(input_data, auto_unbox = TRUE)

# Call Python with JSON data
system2("python", args = c("called.py", json_input))