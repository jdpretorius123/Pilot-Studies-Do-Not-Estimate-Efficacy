library(shiny)

# Define any Python packages needed for the app here:

PYTHON_DEPENDENCIES = c('pip', 'numpy')

# ------------------ App virtualenv setup (Do not edit) ------------------- #

virtualenv_dir = Sys.getenv('VIRTUALENV_NAME')

python_path = Sys.getenv('PYTHON_PATH')

# Create virtual env and install dependencies

reticulate::virtualenv_create(envname = virtualenv_dir, python = python_path)

reticulate::virtualenv_install(virtualenv_dir, packages = PYTHON_DEPENDENCIES, ignore_installed=TRUE)

reticulate::use_virtualenv(virtualenv_dir, required = T)

# ------------------ App server logic (Edit anything below) --------------- #

# Imports necessary python functions

reticulate::import_main()

reticulate::import_builtins()

reticulate::source_python('simulation.py')

# Defines UI

ui <- fluidPage(
  
  tags$head(
    
    tags$link(
      
      rel = "stylesheet",
      
      type = "text/css",
      
      href = "shinyCSS.css"
      
    )
    
  ),
  
  div(
    
    id = "ui",
    
    titlePanel(
      
      title = div(
        
        id = "title",
        
        img(
          
          id = "DukeEmblem",
          
          src = "DukeSOM.png",
          
          alt = "Duke School of Medicine Emblem",
          
          title = "Duke School of Medicine Emblem"
          
        ),
        
        "Pilot Studies Do Not Estimate Efficacy"
        
      ),
      
      windowTitle = "Duke School of Medicine App"
      
    ),
    
    br(),
    br(),
    
    sidebarLayout(
      
      div(
        
        id = "sidebar",
        
        sidebarPanel(
          
          p(
            
            id = "instructions",
            
            "Please enter a number between 2 and 5000",
            
            span(
              
              id = "range",
              
              "(range is inclusive)."
              
            ),
            
            "This represents the number of trials to 
            simulate. Then, please click ",
            
            span(
              
              id = "run",
              
              "Run."
              
            ),
            
            "The simulation results will appear shortly."
            
          ),
          
          br(),
          
          numericInput(
            
            inputId = "numTrials",
            
            label = "Number of Trials to Simulate:",
            
            value = 1000,
            
            min = 2,
            
            max = 5000,
            
          ),
          
          actionButton(
            
            inputId = "run",
            
            label = "Run"
            
          )
          
        )
        
      ),
      
      mainPanel(
        
        div(
          class = "table",
          
          tableOutput(
            
            outputId = "sim"
            
          )
          
        )
        
      )
      
    )
    
  )
  
)

# Defines Server

server <- shinyServer(function(input, output){
  
  observeEvent(input$run,{
    
    n <- input$numTrials
    
    n <- reticulate::r_to_py(n)
    
    simulation(n)
    
    myData <- read.csv(
      
      "data/data.csv",
      
      check.names = FALSE
      
      )
    
    output$sim <- renderTable(
      
      myData,
      
      align = "c",
      
      na = " "
      
      )
    
  })
  
})

# Calls application

shinyApp(ui = ui, server = server)
