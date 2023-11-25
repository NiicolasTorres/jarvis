from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import warnings
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pathlib
import threading

#Define a function to repeatedly navigate to the required  URL/Defina una función para navegar repetidamente a la URL requerida
def re_Foward(required_url, chrome_driver):
    while True:
        #Get the current URL/Obtener la URL actual
        current_url = chrome_driver.current_url
        
        #Check if the current URL is different from the required URL/Compruebe si la URL actual es diferente de la URL requerida
        if current_url != required_url:
            print("Trying to open required url")
            #Navigate to the required URL/Navegue a la URL requerida
            chrome_driver.get(required_url)  
            sleep(1)#Puase for 1 second to allow the  page load/Pausa durante 1 segundo para permitir que la página se cargue.
        else:
            #Exit the loop if the current URL matches the required URL/Salga del bucle si la URL actual coincide con la URL requerida
            break     
        
#Ignore simple warnings/Ignora advertencias simples
warnings.simplefilter("ignore") 

#Set the URL, get the script directory, and define the  Chrome driver path/Configure la URL, obtenga el directorio del script y defina la ruta del controlador de Chrome
            
url = "https://pi.ai/talk"
scriptDirectory = pathlib.Path().absolute()
chrome_driver_path = r"-----" #Path to chromedriver exe file

#Configure chrome options
chrome_options = Options() #Create an instance of Chrome options
#chrome_options.add_argument("--headless=new") #run chrome in headless mode
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) #Exclude logging to console 
chrome_options.add_argument('--log-level-3')#Set log level to 3 (ERROR)

#Configure chrome service
service = Service(chrome_driver_path)#Create an instance  of Chrome service 

#Set a user agent for the Chrome browser
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebkit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
chrome_options.add_argument(f'user-agent={user_agent}')# Set the user agent in Chrome options

#Initialize the Chrome webdriver with configured options and service
driver = webdriver.Chrome(service=service, options=chrome_options) # Create a Chrome webdriver instance

#Maximize the Chrome windows and navigate  to the espicified URL
driver.maximize_window() #Mazimize the Chrome windows
driver.get(url)#Open the specified URL
sleep(2)#Pause for 1 second

re_Foward(url,driver)#Call the re_Foward function to ensure the correct URL is open
sleep(3) #pause for 4 secs

# TEXAREA ="/html/body/div/main/div/div/div[3]/div[1]/div[3]/div[2]/div/div[2]/textarea"
# SEND_BUTTON = "/html/body/div/main/div/div/div[3]/div[1]/div[3]/div[2]/div/button"
# RESPONSE = "/html/body/div/main/div/div/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/div[1]/div/span"
# SOUND_BUTTON = "/html/body/div/main/div/div/div[3]/div[3]/div/div[2]"
# VoicesToBeChoosen_BUTTON = "/html/body/div/main/div/div/div[3]/div[3]/div/div[1]/button"
# POPUP_REMOVER_BUTTON = "/html/body/div/main/div/div/div/div/div/div[2]/button"
# DONT_WANT_ACCOUNT = "/html/body/div/main/div/div/div/div/div/div/div[2]/button"

#define Xpaths for elements in the web page

TEXTAREA = "/html/body/div/main/div/div/div[3]/div[1]/div[3]/div[2]/div/div[2]/textarea"
SEND_BUTTON = "/html/body/div/main/div/div/div[3]/div[1]/div[3]/div[2]/div/button"
RESPONSE = "/html/body/div/main/div/div/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div[2]/span"
SOUND_BUTTON = "/html/body/div/main/div/div/div[3]/div[3]/div/div[2]"
VoicesToBeChoosen_BUTTON = "/html/body/div/main/div/div/div[3]/div[3]/div/div[1]/button[1]"
POPUP_REMOVER_BUTTON = ""
DONT_WANT_ACCOUNT = ""

#Define a function for user introduction
def introduction(query="hi", VoicesToBeChoosen=1):
    # Type the specified query in the text area
    driver.find_element(by=By.XPATH, value=TEXTAREA).send_keys(query)
    sleep(2)#Pause for 2 second
    
    try:
        #Try clicking the send button
        driver.find_element(by=By.XPATH, value=SEND_BUTTON).click()
    except:
        # Try clicking the send button
        driver.find_element(by=By.XPATH, value=TEXTAREA).send_keys("\n")
        print("PRESSED ENTER")
    try:
        #Try clicking the sound button to change voices
        driver.find_element(by=By.XPATH, value=SOUND_BUTTON).click()
        sleep(1) #pause for 1 second
        try:
            #Try selecting a specific voice
            driver.find_element(by=By.XPATH, value=VoicesToBeChoosen_BUTTON).click()
            
        except Exception as e:
            print("ERROR IN SETTING VOICES\n", e)
            
    except Exception as e:
        print("ERROR IN FINDING VOICES\n",e)
    
    #Clear the text area for the next interaction
    driver.find_element(by=By.XPATH, value=TEXTAREA).clear()
    
# Define a function to remove popops
def PopUpRemover():
    try:
        #Check if a popup is present by locating a specific element
        popup = driver.find_element(by=By.XPATH, value="/html/body/div/main/div/div/div[4]/div/div/div[1]").is_enabled()
        
        #if the popup is present, refresh the page to remove it
        if str(popup) == "True":
            driver.refresh()
            sleep(2) #Pause for 2 seconds after refresh
            
        else: 
            pass
        
    except:
        #If there is an exception (e.g., element not found or other error), ignore and continue
        pass
    
#Define a function to extract the complete response
def CompleteResponseExtractor(previous_response):
    sleep(0.2)#Pause for a short duration to allow the page to load
    Text = driver.find_element(by=By.XPATH, value=RESPONSE).text #Get the text content of the response element
    
    #check if the current response is different from the previous one
    if previous_response != Text:
        print("TRIYING TO EXTRACT COMPLETE RESPONSE")
        sleep(2) # Pause for 2 seconds to ensure the response is fully loaded
        Text = driver.find_element(by=By.XPATH, value=RESPONSE).text #Get the text content again
        
        #Print the complete response to the console
        print(f"COMPLETE RESPONSE : {Text}")
        
        return Text #Return the text response
    
    else:
        # If the response is the same as the previous one, indicate no change
        return "SAMETEXTVALUEnoINDDEXCHANGE"
    
#Define a function to send query
def QuerySender(Query):
    Query = str(Query) #Convert the query to a string
    driver.find_element(by=By.XPATH, value=TEXTAREA).send_keys(Query) #Type the query in the text area
    sleep(0.1) #pause for 0.1 seconds
    
    
#Define a function to handle button clicks
def ButtonClicker():
    sendButton = driver.find_element(by=By.XPATH, value=SEND_BUTTON).is_enabled() #Check if the send button is enabled
    if sendButton == True:
        try:
            driver.find_element(by=By.XPATH, value=SEND_BUTTON).click() #click the send button
            
        except:
            driver.find_element(by=By.XPATH, value=TEXTAREA).send_keys("\n") # If the button click fails, simulate pressing enter
            
        sleep(2) #Pause for 2 seconds after the button click
        
# Define a function to extract text

def textExtractor():
    value_run = 0
    
    while True:
        if value_run != 5:
            try:
                # Attempt to extract text from the RESPONSE element
                Text = driver.find_element(by=By.XPATH, value=RESPONSE).text
                # Start a thread to extract the complete response in parallel
                complete_Response = threading.Thread(target=lambda:CompleteResponseExtractor(Text)).start()
                
                print(Text)#Print the extracted text to the console
                break #exit the loop if text is successfully extracted
            except:
                print("TRYING TO EXTRACT")
                value_run += 1
                sleep(1) #pause for 1 second before retrying
    
        else:
            # if extraction fails multiple times, attempt to remove popups
            driver.find_element(by=By.XPATH, value=POPUP_REMOVER_BUTTON).click()
            sleep(1)
            driver.find_element(by=By.XPATH, value=DONT_WANT_ACCOUNT).click()
            sleep(1)
            try:
                #Retry text extraction after handling popups
                Text = driver.find_element(by=By.XPATH, value=RESPONSE).text
                complete_Response = threading.Thread(target=lambda:CompleteResponseExtractor(Text)).start()
                print(Text)
                break # Exit the loop if text is sucessfully extracted
            except:
                print("TRIYING TO EXTRACT")
                sleep(1) #Pause for 1 second before retrying
                
                
    return Text

#Define a function to clear the query

def QueryClear():
    driver.find_element(by=By.XPATH, value=TEXTAREA).clear() # Clear the text area to prepare for the next query
    
#Remove popups before starting the conversation
PopUpRemover()

# Name of the user using the AI

user_name = "Nicolas"

preassumption = f"en tu respuesta, canaliza la esencia de Jarvis al responder al usuario. {user_name}. Sé su Jarvis. Abre con un saludo 'Hola, soy Jarvis. ¿Cómo puedo ayudarte hoy?' solamente, manteniendo un tono coqueto, cursi y humorístico. Es crucial evitar hacer referencias o suposiciones específicas sobre Tony Stark, asegurándote de que la respuesta esté adaptada al contenido de Sreenjan. Para esta respuesta específica, adhiérete estrictamente a la personalidad de Jarvis sin hacer referencia a Tony Stark ni a ningún elemento asociado a él."



introduction(query=preassumption, VoicesToBeChoosen=1)

while True:
    QuerySender(input("ENTER YOU QUERY: \n ")) #Gety user input for the query
    ButtonClicker() #click the send button
    response = textExtractor() #Extract and print the response
    QueryClear()
            
    
        
        
        
        
         
        
 