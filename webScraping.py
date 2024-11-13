from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time


# Configurar credenciales y calificación
matricula = ""
contraseña = ""
calificacion = "4" # Calificacion para todos los profesores
numero_de_profesores = 7


# Configura el controlador de Edge (debes tener msedgedriver en tu PATH o especificar la ubicación)
driver_path = './edgedriver_win64/msedgedriver.exe' 
service = Service(driver_path)
driver = webdriver.Edge(service=service)

# URL de inicio de sesión
url = "http://prometheus.utmorelia.edu.mx:8080/sigo/faces/access.xhtml"
driver.get(url)

# Esperar a que se cargue el campo de matrícula
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "form-login:input-user"))
)

# Ingresar matrícula y contraseña
driver.find_element(By.ID, "form-login:input-user").send_keys(matricula)
driver.find_element(By.ID, "form-login:input-pass").send_keys(contraseña)

# Clic en el botón de iniciar sesión
driver.find_element(By.ID, "form-login:j_idt35").click()

# Esperar hasta que la página cargue completamente después de iniciar sesión
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "j_idt166:j_idt167"))
)

# Seleccionar la tarjeta específica que contiene la encuesta
encuesta_card = driver.find_element(By.ID, "j_idt166:j_idt167")
ActionChains(driver).move_to_element(encuesta_card).click().perform()


# Recorrer cada profesor
for i1 in range(0, numero_de_profesores):

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, f"repeat-course:{i1}:form-evaluation-teacher:j_idt436:23:appreciation"))
    )

    # Seleccionar todos los elementos `select` y asignarles la calificación
    for i2 in range(0, 24):
        select = Select(driver.find_element(By.ID, f"repeat-course:{i1}:form-evaluation-teacher:j_idt436:{i2}:appreciation"))
        select.select_by_value(calificacion)
        #esperar 1 segundo
        time.sleep(0.5)

    # Click en la opción de recomendar al profesor
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, f"repeat-course:{i1}:form-evaluation-teacher:j_idt445"))
    )
    driver.find_element(By.ID, f"repeat-course:{i1}:form-evaluation-teacher:j_idt445").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, f"repeat-course:{i1}:form-evaluation-teacher:btn-next"))
    )
    # Clic en el botón de siguiente
    driver.find_element(By.ID, f"repeat-course:{i1}:form-evaluation-teacher:btn-next").click()

print("Por errores no es pasible rellenar la encuesta de tutor, por favor rellenela manualmente")
input("Presione enter para cerrar el navegador")
print("Estas seguro que quieres cerrar el navegador?")
