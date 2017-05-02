fileModelLabels = 'C:\\Users\\Hedonistic\\Desktop\\Stats 897\\FinalProject\\Water Pumps\\Pump_it_Up_Data_Mining_the_Water_Table_-_Training_set_labels.csv'
fileModelValues = 'C:\\Users\\Hedonistic\\Desktop\\Stats 897\\FinalProject\\Water Pumps\\Pump_it_Up_Data_Mining_the_Water_Table_-_Training_set_values.csv'
fileFinalValues = 'C:\\Users\\Hedonistic\\Desktop\\Stats 897\\FinalProject\\Water Pumps\\Pump_it_Up_Data_Mining_the_Water_Table_-_Test_set_values.csv'

# Get Data
modelDataValues = read.csv(fileModelValues, header = TRUE, stringsAsFactors = TRUE,  na.strings = "")
modelDataLabels = read.csv(fileModelLabels, header = TRUE, stringsAsFactors = TRUE,  na.strings = "")
WaterPumps = modelDataValues

WaterPumps$recorded_by <- NULL
killList = which(sapply(WaterPumps, function(x) length(unique(x) ) ) > 100)
killList = killList[-1]
fnames = names(WaterPumps)
for (i in killList) { WaterPumps[fnames[i]] <- NULL}
WaterPumps$date_recorded <- NULL

WaterPumps$PumpState =  modelDataLabels[,2]
WaterPumps = WaterPumps[,c(ncol(WaterPumps),1:ncol(WaterPumps)-1)]
WaterPumps = WaterPumps[complete.cases(WaterPumps),]

X = WaterPumps[,-c(1,2)]
Y = WaterPumps$PumpState


mLevelProbs <- function(X,Y){
    nPredictors = ncol(X)
    allOutcomes = unique(Y)
    nOutcomes = length(allOutcomes)
    
    P = list()
    for(i in 1 : nPredictors){
        L = list()
        allLevels = unique(X[,i])
        nLevels = length(allLevels) # how man ylevels does this predicotr have
        
        for(j in 1 : nOutcomes){
            data = X[as.character(Y) == as.character(allOutcomes[j]),]
            totalEntries = length(data[,1]) # how man yoccurences are there of the specified outcome?
            c = 0
            for(k in 1 : nLevels){
                nPoints = sum(as.character(data[,i]) == as.character(allLevels[k]))
                c[k] = nPoints/totalEntries # what proportion of points fall on this level, 
                # for this predictor, given this outcome
            }   
            L[[j]] = c
        }
        P[[i]] = L
    }
    
}

P = mLevelProbs(X,Y)

