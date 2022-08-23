import csv # imports necessary python packages

class Table:
    def __init__(self):
        self.dataTable = [["ES",
                           "Number of Trials",
                           "Treatment ES (95% CI)",
                           "ES Incorrect (% of trials)",
                           "ES Slightly Correct (% of trials)",
                           "ES Moderately Correct (% of trials)",
                           "ES Largely Correct (% of trials)"],
                          [-0.2,10],
                          [" ",20],
                          [" ",30],
                          [-0.35,10],
                          [" ",20],
                          [" ",30],
                          [-0.5,10],
                          [" ",20],
                          [" ",30]] # initializes table to be printed

        self.data = None # stores copy of simulation results

    def __repr__(self):
        return self.__class__.__name__ + str(self.getDataTable)

    def __str__(self):
        return "A table to be transcribed into a CSV file using this template: " + str(self.getDataTable)
        
    def getDataTable(self):
        return self.dataTable

    def getData(self):
        return self.data

    def setDataTable(self, table):
        self.dataTable = table

    def setData(self, data):
        self.data = data

    def storeData(self, data): # stores simulation results, populates table, and writes CSV file
        self.setData(data)
        self.processData()
        self.writeCSV()

    def processData(self): # populates table with simulation results
        table = self.getDataTable()
        data = self.getData()

        for row in range(1,10):
            arow = data[row - 1]

            EShat = str(arow[0])
            lb = str(arow[1])
            ub = str(arow[2])

            EStable = EShat + " (" + lb + "," + ub + ")"
            table[row].append(EStable)
            
            bins = arow[3]
            for abin in range(4):
                table[row].append(bins[abin])
            
        self.setDataTable(table)

    def writeCSV(self): # writes CSV file
        csvFile = open('data/data.csv', 'w', newline='')
        writer = csv.writer(csvFile)
        table = self.getDataTable()

        for row in table:
            writer.writerow(row)

        csvFile.close()
