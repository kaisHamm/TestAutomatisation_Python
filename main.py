from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import string
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_email():
    return generate_random_string(8) + "@example.com"

def generate_random_password():
    return generate_random_string(10)

# Initialisation du pilote
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()
url = "https://ztrain-web.vercel.app/"
driver.get(url)


# Création de compte
def create_account():


    driver.find_element(By.ID,"style_avatar_wrapper__pEGIQ").click()

    driver.find_element(By.XPATH, "//button[contains(text(), 'Inscription')]").click()

    email= generate_random_email()
    driver.find_element(By.ID, "email_register").send_keys(email)

    password = generate_random_password()

    driver.find_element(By.ID, "password_register").send_keys(password)
    driver.find_element(By.ID, "confirm_password_register").send_keys(password)
    driver.find_element(By.ID, "btn_register").click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "btn_register")))
    time.sleep(10)
    return email, password

# Connexion
def login(email, password):


    driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ").click()

    driver.find_element(By.ID, "email_login").send_keys(email)
    driver.find_element(By.ID, "password_login").send_keys(password)
    driver.find_element(By.ID, "btn_login").click()
    time.sleep(10)



# Déconnexion
def logout():
    driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ").click()

    driver.find_element(By.ID, "logout").click()
    time.sleep(10)

def add_product_to_cart(product_url, cart_url):
    # Ouvrir la page du produit
    driver.get(product_url)

    # Localiser et cliquer sur le bouton d'ajout au panier
    add_to_cart_button = driver.find_element(By.ID, "style_btn_add_cart__WFoN1")
    add_to_cart_button.click()

    # Aller à la page du panier
    driver.get(cart_url)

    # Vérifier le produit et la quantité
    product_name = driver.find_element(By.ID, "product_name_id").text  # Remplacez par l'ID correct
    quantity = driver.find_element(By.ID, "quantity_id").text  # Remplacez par l'ID correct

    return product_name, quantity


def rechercher_produit(product_name):
    print("Démarrage de la fonction search_product")
    driver.get(url)
    print(f"URL chargée : {url}")

    # Localiser la barre de recherche
    search_bar = driver.find_element(By.ID,"style_input_navbar_search__Scaxy")
    search_bar.send_keys(product_name)
    print(f"Produit recherché : {product_name}")

    # Soumettre la recherche
    search_bar.send_keys(Keys.RETURN)


    # Attendre le chargement des résultats
    time.sleep(5)


    try:

        results = driver.find_elements(By.XPATH, f"//*[contains(text(), '{product_name}')]")



        for result in results:
            if product_name.lower() in result.text.lower():
                print(f"Le produit {result.text} correspond à la recherche")

            else:
                print("Aucun produit correspondant trouvé.")
    except Exception as e:
        print("Erreur lors de la recherche")
        return "Erreur lors de la recherche : " + str(e)

def mdp_oublie(email):
    driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ").click()

    driver.find_element(By.CLASS_NAME, "style_forgotpass__JmLID").click()

    driver.find_element(By.ID, "email_reset_pass").send_keys(email)
    password = generate_random_password()

    driver.find_element(By.ID, "reset_password").send_keys(password)

    driver.find_element(By.ID, "btn_reset_password").click()
    time.sleep(10)



#mdp_oublie('kais')
# create_account()
rechercher_produit("Ampoule Vecteur Incandescent")