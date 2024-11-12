#Nov 12, 2024
# Modified by Duong

SCION_hub <- function(target_genes_file,reg_genes_file,target_data_file,reg_data_file,normalize_edges,weightthreshold,
                  is_clustering,clustering_data_file,threshold,clusters_file,hubs,num.cores,working_dir){
  
  #set working directory which contains all your input files
  setwd(working_dir)
  
  #set seed to ensure same network each time
  set.seed(2020)
  
  
  #read in tables
  target_genes = read.csv(target_genes_file,stringsAsFactors=FALSE)
  reg_genes = read.csv(reg_genes_file,stringsAsFactors=FALSE)
  target_data = read.csv(target_data_file,row.names=1)
  reg_data = read.csv(reg_data_file,row.names=1)
  
  #convert normalize_edges to boolean
  if(normalize_edges=="Yes"){
    normalize=T
  }else{
    normalize=F
  }
  
  #get data for targets and regulators
  mytargetdata = target_data[row.names(target_data)%in%target_genes[,1],]
  myregdata = reg_data[row.names(reg_data)%in%reg_genes[,1],]
  
  #make valid row names
  rownames(mytargetdata) <- make.names(rownames(mytargetdata))
  rownames(myregdata) <- make.names(rownames(myregdata))
  
  hubs <- read.csv("all_hub_genes.csv", header=TRUE, stringsAsFactors=FALSE)  # hub genes outputted from Python output
  hubs_vector <- hubs$X0
  # subset data to include only these hub genes
  hubtargetdata = mytargetdata[row.names(mytargetdata)%in%hubs_vector,]
  hubregdata = myregdata[row.names(myregdata)%in%hubs_vector,]
  # infer network connecting the hubs
  if (nrow(hubtargetdata) == 0) {
    genes <- unlist(strsplit(as.character(hubs_vector), '\\.'))
    if (length(genes) > 0) {
    genes <- genes[seq(1, length(genes), by = 2)]
    }
    hubtargetdata <- mytargetdata[row.names(mytargetdata) %in% genes, ]
  }
    
  network = RS.Get.Weight.Matrix(t(hubtargetdata),t(hubregdata),normalize=normalize,num.cores=num.cores)
    
  #now make a new network where we eliminate all the low confidence edges
  trimmednet = data.frame(ifelse(network<weightthreshold,NaN,network))
  
  #translate the trimmed network into a table we can import into cytoscape
  networktable = data.frame(Regulator=character(), Interaction=character(), Target=character(), Weight=double(),
                            stringsAsFactors=FALSE)
  row=1
  for (j in 1:dim(trimmednet)[1]){
    for (k in 1:dim(trimmednet)[2]){
      #skip NaNs as these have no edge
      if (is.na(trimmednet[j,k])){
        next
      }else{
        networktable[row,] = cbind(colnames(trimmednet)[k],"regulates",rownames(trimmednet)[j],trimmednet[j,k])
        row = row+1
      }
    }
  }
  
  #write table to file
  write.table(networktable,'network_hub.txt',row.names=FALSE,quote=FALSE,sep='\t')
}


