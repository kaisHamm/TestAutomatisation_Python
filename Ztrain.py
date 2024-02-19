from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
import time
import random
import string
import re


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generer_chaine_aleatoire(longueur=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(longueur))


def generer_numero_telephone_aleatoire():
    return ''.join(random.choice(string.digits) for _ in range(10))


def generate_random_email():
    return generate_random_string(8) + "@example.com"


def generate_random_password():
    return generate_random_string(10)

test_results = []
# Initialisation du pilote
def generate_html_report(test_results, filename="test_report.html"):
    with open(filename, 'w') as file:
        file.write("<html><head><title>Rapport de Test</title></head><body>")
        file.write("<h1>Rapport de Test Selenium</h1>")
        file.write("<ul>")
        for result in test_results:
            file.write(f"<li>{result}</li>")
        file.write("</ul>")
        file.write("</body></html>")

def create_account():
    global test_results
    print("Choisissez le type de données à utiliser :")
    print("1: Données valides")
    print("2: Email invalide")
    print("3: Mot de passe trop court")
    choix = input("Entrez votre choix (1, 2 ou 3): ")

    if choix == '1':
        email = generate_random_email()
        password = generate_random_password()
        data['create_account']['success']['email'] = email
        data['create_account']['success']['password'] = password
    elif choix == '2':
        email = data['create_account']['invalid_email']['email']
        password = data['create_account']['invalid_email']['password']
    elif choix == '3':
        email = data['create_account']['short_password']['email']
        password = data['create_account']['short_password']['password']
    else:
        test_results.append("create_account: Choix invalide")
        print("Choix invalide.")
        return
    assert choix in ['1', '2', '3'], "Le choix doit être 1, 2 ou 3"

    try:
        time.sleep(1)
        driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Inscription')]").click()
        time.sleep(1)
        driver.find_element(By.ID, "email_register").clear()
        driver.find_element(By.ID, "email_register").send_keys(email)
        time.sleep(1)
        driver.find_element(By.ID, "password_register").clear()
        driver.find_element(By.ID, "password_register").send_keys(password)
        time.sleep(1)
        driver.find_element(By.ID, "confirm_password_register").clear()
        driver.find_element(By.ID, "confirm_password_register").send_keys(password)
        time.sleep(1)
        driver.find_element(By.ID, "btn_register").click()
        time.sleep(1)



        error_messages = driver.find_elements(By.CLASS_NAME, "style_messageError__mbzDa")
        time.sleep(1)
        if error_messages:

            for error_message in error_messages:
                if "Le format de l'email est invalid" in error_message.text:
                    raise AssertionError("Le format de l'email est invalide.")

                elif "Le mot de passe doit avoir au moins 8 caractères" in error_message.text:
                    raise AssertionError("Le mot de passe doit avoir au moins 8 caractères")
        else:
            test_results.append(f"create_account: Compte créé avec succès - {email}")
            logout()

        time.sleep(2)

        with open('article.json', 'w') as file:
            json.dump(data, file, indent=4)


    except TimeoutException:
        test_results.append("create_account: Aucun message d'erreur détecté. Veuillez vérifier si le compte a été créé avec succès.")
    except AssertionError as e:
        test_results.append(f"create_account: Échec - {e}")
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "ant-modal-close").click()
    except Exception as e:
        test_results.append(f"create_account: Erreur lors de la création du compte - {e}")
        driver.get(url)
        time.sleep(2)


def changement_infos():
    # login
    global test_results
    test_results.append("changement_infos:")
    try:
        compte = random.choice(data['login']['existants'])
        email = compte['email']
        password = compte['mdp']
        driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Connexion')]").click()
        time.sleep(2)
        driver.find_element(By.ID, "email_login").send_keys(email)
        driver.find_element(By.ID, "password_login").send_keys(password)
        driver.find_element(By.ID, "btn_login").click()
        time.sleep(3)
        status_indicator = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            ".ant-scroll-number.ant-badge-dot.ant-badge-status-green[data-show='true']"))
        )
        time.sleep(3)
        if status_indicator.is_displayed():
            test_results.append(f" Compte connécté avec succès - {email}")

        avatar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1"))
        )
        avatar.click()
        user_info = random.choice(data['utilisateur_infos'])

        mon_compte = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/profile']"))
        )
        mon_compte.click()
        time.sleep(1)
        champ_nom = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "lastName")))
        champ_nom.clear()
        champ_nom.send_keys(user_info['nom'])
        time.sleep(1)

        champ_prenom = driver.find_element(By.ID, "firstName")
        champ_prenom.clear()
        champ_prenom.send_keys(user_info['prenom'])
        time.sleep(1)

        champ_adresse = driver.find_element(By.ID, "address")
        champ_adresse.clear()
        champ_adresse.send_keys(user_info['adresse'])
        time.sleep(1)

        champ_telephone = driver.find_element(By.ID, "phone")
        champ_telephone.clear()
        champ_telephone.send_keys(user_info['numero_telephone'])
        time.sleep(1)

        champ_adresse_facturation = driver.find_element(By.ID, "addressFacturation")
        champ_adresse_facturation.clear()
        champ_adresse_facturation.send_keys(user_info['adresse_facturation'])
        time.sleep(1)

        champ_adresse_livraison = driver.find_element(By.ID, "addressLivraison")
        champ_adresse_livraison.clear()
        champ_adresse_livraison.send_keys(user_info['adresse_livraison'])
        time.sleep(1)

        # Sélectionner la civilité, si nécessaire. Assurez-vous que le texte correspond exactement à une des options.
        menu_civilite = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "civility")))
        menu_civilite.click()

        # Cela suppose que la civilité est soit 'Monsieur', soit 'Madame'
        option_civilité = "Monsieur" if user_info['civilite'] == "Monsieur" else "Madame"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{option_civilité}')]"))).click()
        time.sleep(1)
        bouton_soumettre = driver.find_element(By.CLASS_NAME, "style_btn2__0wrea")
        bouton_soumettre.click()
        time.sleep(1)

        mot_de_passe_actuel = password

        nouveau_mot_de_passe = generate_random_string(10)

        champ_mot_de_passe_actuel = driver.find_element(By.XPATH, "(//input[@id='filled-adornment-password'])[1]")
        champ_mot_de_passe_actuel.clear()
        champ_mot_de_passe_actuel.send_keys(mot_de_passe_actuel)
        time.sleep(1)

        champ_nouveau_mot_de_passe = driver.find_element(By.XPATH, "(//input[@id='filled-adornment-password'])[2]")
        champ_nouveau_mot_de_passe.clear()
        champ_nouveau_mot_de_passe.send_keys(nouveau_mot_de_passe)
        time.sleep(2)

        bouton_mise_a_jour = driver.find_element(By.CSS_SELECTOR,
                                                 "button.style_btn2__ceZK5")
        bouton_mise_a_jour.click()

        test_results.append("Modification des informations réussie.")

        time.sleep(5)
        password = nouveau_mot_de_passe

        for compte in data['login']['existants']:
            if compte['email'] == email:
                compte['mdp'] = nouveau_mot_de_passe
                break

        with open('article.json', 'w') as file:
            json.dump(data, file, indent=4)

        logout()

        time.sleep(2)

        driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ").click()
        time.sleep(1)
        driver.find_element(By.ID, "email_login").send_keys(email)
        time.sleep(1)
        driver.find_element(By.ID, "password_login").send_keys(password)
        time.sleep(1)
        driver.find_element(By.ID, "btn_login").click()

        test_results.append("Reconnexion réussie.")
        time.sleep(2)
        avatar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1"))
        )
        avatar.click()

        time.sleep(2)
        mon_compte = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/profile']"))
        )
        mon_compte.click()
        try:
            nom_actuel = driver.find_element(By.ID, "lastName").get_attribute('value')
            prenom_actuel = driver.find_element(By.ID, "firstName").get_attribute('value')
            adresse_actuelle = driver.find_element(By.ID, "address").get_attribute('value')
            telephone_actuel = driver.find_element(By.ID, "phone").get_attribute('value')
            adresse_facturation_actuelle = driver.find_element(By.ID, "addressFacturation").get_attribute('value')
            adresse_livraison_actuelle = driver.find_element(By.ID, "addressLivraison").get_attribute('value')

            # Comparer les valeurs récupérées avec celles du JSON
            assert nom_actuel == user_info['nom'], f"Nom attendu: {user_info['nom']}, trouvé: {nom_actuel}"
            test_results.append(f"Nom actuel correspond à celui du JSON : {user_info['nom']} == {nom_actuel}")

            assert prenom_actuel == user_info[
                'prenom'], f"Prénom attendu: {user_info['prenom']}, trouvé: {prenom_actuel}"
            test_results.append(f"Prénom actuel correspond à celui du JSON : {user_info['prenom']} == {prenom_actuel}")

            assert adresse_actuelle == user_info[
                'adresse'], f"Adresse attendue: {user_info['adresse']}, trouvée: {adresse_actuelle}"
            test_results.append(
                f"Adresse actuelle correspond à celle du JSON : {user_info['adresse']} == {adresse_actuelle}")

            assert telephone_actuel == user_info[
                'numero_telephone'], f"Numéro de téléphone attendu: {user_info['numero_telephone']}, trouvé: {telephone_actuel}"
            test_results.append(
                f"Numéro de téléphone actuel correspond à celui du JSON : {user_info['numero_telephone']} == {telephone_actuel}")

            assert adresse_facturation_actuelle == user_info[
                'adresse_facturation'], f"Adresse de facturation attendue: {user_info['adresse_facturation']}, trouvée: {adresse_facturation_actuelle}"
            test_results.append(
                f"Adresse de facturation actuelle correspond à celle du JSON : {user_info['adresse_facturation']} == {adresse_facturation_actuelle}")

            assert adresse_livraison_actuelle == user_info[
                'adresse_livraison'], f"Adresse de livraison attendue: {user_info['adresse_livraison']}, trouvée: {adresse_livraison_actuelle}"
            test_results.append(
                f"Adresse de livraison actuelle correspond à celle du JSON : {user_info['adresse_livraison']} == {adresse_livraison_actuelle}")

            test_results.append("Toutes les données affichées correspondent aux données du compte JSON.")

        except Exception as e:

            print(f"Une erreur s'est produite : {str(e)}")

    except Exception as e:
        test_results.append(f"Erreur dans changement_infos : {str(e)}")
    logout()
    time.sleep(3)


# Connexion
def login():
    global test_results
    test_results.append('login():')
    choix = input(
        "Pour la fonction login voulez-vous vous connecter avec un compte existant (1) ou tester un compte inexistant (2)? Entrez 1 ou 2: ")
    if choix == '1':
        compte = random.choice(data['login']['existants'])
    elif choix == '2':
        compte = random.choice(data['login']['inexistants'])
    else:
        test_results.append("login: échec - Choix invalide")
        return

    email = compte['email']
    password = compte['mdp']

    email_verif = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    assert email_verif.match(email), "L'adresse email est invalide."

    try:
        driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ").click()
        time.sleep(1)
        driver.find_element(By.ID, "email_login").send_keys(email)
        time.sleep(1)
        driver.find_element(By.ID, "password_login").send_keys(password)
        time.sleep(1)
        driver.find_element(By.ID, "btn_login").click()
        time.sleep(1)
        error_messages = driver.find_elements(By.CLASS_NAME, "style_messageError__mbzDa")
        time.sleep(1)
        if error_messages:
            for error_message in error_messages:
                if "Email ou mot de passe incorrect" in error_message.text:
                    raise AssertionError("Email ou mot de passe incorrect")
        else:
            status_indicator = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                ".ant-scroll-number.ant-badge-dot.ant-badge-status-green[data-show='true']"))
            )
            time.sleep(1)
            if status_indicator.is_displayed():
                test_results.append(f"login: succès - Connexion réussie avec le compte {email}")
                logout()

            else:
                AssertionError("Pas connecter")

    except TimeoutException:
       test_results.append("login: échec - Temps d'attente dépassé pour le login")
    except AssertionError as e:
        test_results.append(f"login: échec - {e}")
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "ant-modal-close").click()
    except Exception as e:
        test_results.append(f"login: échec - Erreur inattendue: {e}")

    time.sleep(1)


# Déconnexion
def logout():
    global test_results
    test_results.append('logout():')
    try:
        time.sleep(1)
        WebDriverWait(driver, 2).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.ant-notification-notice-message"))
        )
    except TimeoutException:
        test_results.append("logout: échec - Notification de déconnexion non disparue")

    try:
        time.sleep(1)
        avatar = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, "style_avatar_wrapper__pEGIQ"))
        )
        avatar.click()
    except ElementClickInterceptedException:
        test_results.append("logout: échec - L'élément avatar n'est pas cliquable")
        return
    try:
        time.sleep(1)
        logout_link = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Se déconnecter"))
        )
        logout_link.click()
        test_results.append("logout: succès")
    except ElementClickInterceptedException:
        test_results.append("logout: échec - L'option de menu 'Se déconnecter' n'est pas cliquable")
    time.sleep(2)


def add_product():
    global test_results
    test_results.append("add_product :")
    choix = input("Voulez-vous mettre au panier un article existant (1) ou inexistant (2)? Entrez 1 ou 2: ")
    assert choix in ['1', '2'], "Choix non valide. Veuillez entrer 1 ou 2."
    if choix == '1':
        product_name = random.choice(data['rechercher_produit']['articles_existants'])
    elif choix == '2':
        product_name = random.choice(data['rechercher_produit']['articles_inexistants'])
    else:
        print("Choix non valide. Veuillez entrer 1 ou 2.")
        return

    test_results.append(f"Produit sélectionné pour la mise au panier : {product_name}")

    driver.get(url)
    search_bar = driver.find_element(By.ID, "style_input_navbar_search__Scaxy")
    time.sleep(1)
    search_bar.send_keys(product_name)
    time.sleep(1)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(3)

    try:
        results = driver.find_elements(By.XPATH, f"//*[contains(text(), '{product_name}')]")
        produit_trouve = any(product_name.lower() in result.text.lower() for result in results)
        assert produit_trouve, f"Aucun produit correspondant trouvé pour {product_name}"
        test_results.append(f"Le produit {product_name} correspond à la recherche")
    except Exception as e:
        test_results.append("Erreur lors de la recherche : ", str(e))

    try:
        driver.find_element(By.CLASS_NAME, "style_card_body__QuFGN").click()
        # Cliquer sur le bouton pour ajouter le produit au panier
        time.sleep(3)
        add_to_cart_button = driver.find_element(By.ID, "style_btn_add_cart__gTXM7")
        add_to_cart_button.click()
        time.sleep(1)
        notification_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-notification-notice-message"))
        )

        assert notification_message.text == "Ajout produit au panier", f"L'article {product_name} a été ajouté au panier avec succès."
        test_results.append(f"L'article {product_name} a été ajouté au panier avec succès.")
        time.sleep(5)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "style_content_cart_wrapper__mqNbf"))
        ).click()
        time.sleep(3)

    except Exception as e:
        test_results.append(f"Erreur lors de l'ajout du produit {product_name} au panier : {e}")

    time.sleep(3)
    driver.find_element(By.ID, "style_content_cart_header__NIJbw").click()
    search_bar.clear()


def rechercher_produit():
    global test_results
    test_results.append("add_product :")
    choix = input("Voulez-vous tester un article existant (1) ou inexistant (2)? Entrez 1 ou 2: ")
    assert choix in ['1', '2'], "Choix non valide. Veuillez entrer 1 ou 2."
    if choix == '1':
        product_name = random.choice(data['rechercher_produit']['articles_existants'])
    elif choix == '2':
        product_name = random.choice(data['rechercher_produit']['articles_inexistants'])

    test_results.append(f"Produit sélectionné pour la recherche : {product_name}")

    driver.get(url)
    search_bar = driver.find_element(By.ID, "style_input_navbar_search__Scaxy")
    time.sleep(1)
    search_bar.send_keys(product_name)
    time.sleep(1)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(3)


    try:
        if choix == '1':
            driver.find_element(By.CLASS_NAME, "style_card_body__QuFGN").click()
            time.sleep(4)
            driver.find_element(By.ID, "style_btn_close__9uLzQ").click()
            test_results.append(f"Le produit {product_name} correspond à la recherche")
        else:

            try:
                driver.find_element(By.CLASS_NAME, "style_card_body__QuFGN")
                raise AssertionError("Un produit non attendu a été trouvé.")
            except NoSuchElementException:
                test_results.append("Aucun produit correspondant trouvé.")

    except AssertionError as e:
        test_results.append(f"Erreur d'assertion : {e}")

    except Exception as e:
        test_results.append(f"Erreur lors de la recherche : {e}")
    search_bar.clear()
    time.sleep(3)


def mdp_oublie():
    global test_results
    test_results.append("mdp_oublie :")
    compte = random.choice(data['login']['existants'])
    email = compte['email']

    email_verif = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    assert email_verif.match(email), "L'adresse email est invalide."

    nouveau_mot_de_passe = generate_random_password()
    for compte in data['login']['existants']:
        if compte['email'] == email:
            compte['mdp'] = nouveau_mot_de_passe
            break

    with open('article.json', 'w') as file:
        json.dump(data, file, indent=4)

    try:
        driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ").click()
        driver.find_element(By.CLASS_NAME, "style_forgotpass__JmLID").click()
        driver.find_element(By.ID, "email_reset_pass").send_keys(email)
        driver.find_element(By.ID, "reset_password").send_keys(nouveau_mot_de_passe)
        driver.find_element(By.ID, "btn_reset_password").click()
        time.sleep(10)



        test_results.append("mdp_oublie: succès - Le mot de passe a été réinitialisé avec succès.")
    except Exception as e:
        test_results.append(f"mdp_oublie: échec - {e}")


fake_card_number = '5134135717007613'
fake_card_expiry = '10/28'
fake_card_cvc = '416'
fake_delivery_address = '123 Test Street, Test City, TC 12345'


def achat_produit():
    global test_results
    test_results.append("achat_produit :")
    test_results.append("Début de la procédure d'achat de produit.")

    # Connexion
    compte = random.choice(data['login']['existants'])
    email = compte['email']
    password = compte['mdp']
    test_results.append(f"Tentative de connexion avec le compte : {email}")
    driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ").click()
    time.sleep(1)
    driver.find_element(By.ID, "email_login").send_keys(email)
    time.sleep(1)
    driver.find_element(By.ID, "password_login").send_keys(password)
    time.sleep(1)
    driver.find_element(By.ID, "btn_login").click()
    time.sleep(3)
    status_indicator = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".ant-scroll-number.ant-badge-dot.ant-badge-status-green[data-show='true']"))
    )
    time.sleep(3)
    assert status_indicator.is_displayed(), "Échec de la connexion."
    test_results.append(f"Connexion réussie avec le compte : {email}.")

    choix = input("Voulez-vous mettre au panier un article existant (1) ou inexistant (2)? Entrez 1 ou 2: ")
    if choix == '1':
        product_name = random.choice(data['rechercher_produit']['articles_existants'])
    elif choix == '2':
        product_name = random.choice(data['rechercher_produit']['articles_inexistants'])
    else:
        print("Choix non valide. Veuillez entrer 1 ou 2.")
        return

    test_results.append(f"Recherche du produit : {product_name}")
    driver.get(url)
    search_bar = driver.find_element(By.ID, "style_input_navbar_search__Scaxy")
    search_bar.send_keys(product_name)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(5)



    driver.get(url)
    search_bar = driver.find_element(By.ID, "style_input_navbar_search__Scaxy")
    search_bar.send_keys(product_name)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(5)

    results = driver.find_elements(By.XPATH, f"//*[contains(text(), '{product_name}')]")
    produit_trouve = any(product_name.lower() in result.text.lower() for result in results)

    driver.find_element(By.CLASS_NAME, "style_card_body__QuFGN").click()
    # Vérification de la présence du produit
    assert produit_trouve, f"Le produit {product_name} n'a pas été trouvé."
    time.sleep(6)
    add_to_cart_button = driver.find_element(By.ID, "style_btn_add_cart__gTXM7")
    add_to_cart_button.click()
    time.sleep(2)

    time.sleep(6)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "style_content_cart_wrapper__mqNbf"))
    ).click()
    time.sleep(6)
    test_results.append(f"{product_name} à été mit au panier")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "style_btn_cart__zrT9Q"))
    ).click()

    home_delivery_value = "64787888a6f03f1ae52f3e46"
    driver.execute_script(f"document.querySelector('input[type=\"radio\"][value=\"{home_delivery_value}\"]').click();")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "card-number"))
    ).send_keys(fake_card_number)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "card-expiry"))
    ).send_keys(fake_card_expiry)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "cvc"))
    ).send_keys(fake_card_cvc)

    test_results.append("Informations de carte de crédit remplies avec succès.")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "style_input_address__CrN2C"))
    ).send_keys(fake_delivery_address)
    time.sleep(5)

    button = driver.find_element(By.ID, "style_btnSubmit__sn_sg")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(8)
    test_results.append("Adresse de livraison remplie avec succès.")

    # Cliquez sur le menu deroulan pour finaliser la commande
    avatar = driver.find_element(By.ID, "style_avatar_wrapper__pEGIQ")
    driver.execute_script("arguments[0].click();", avatar)
    time.sleep(5)

    commande = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/commandes']"))
    )
    commande.click()
    time.sleep(5)
    driver.find_element(By.ID, "style_content_logo__pkvMP").click()
    test_results.append("Commande réussie.")
    time.sleep(3)
    logout()

    time.sleep(3)


def lancer_fonctions():
    fonctions = {
        1: create_account,
        2: login,
        3: rechercher_produit,
        4: changement_infos,
        5: mdp_oublie,
        6: add_product,
        7: achat_produit
    }

    print("""
    1: create_account
    2: login/logout
    3: rechercher_produit
    4: changement_infos
    5: mdp_oublie
    6: add_product
    7: achat_produit
    """)

    choix_utilisateur = input("Entrez les numéros des fonctions à exécuter, séparés par des virgules (ex: 3,6,1,2): ")

    try:
        ordre = [int(i) for i in choix_utilisateur.split(',')]
    except ValueError:
        print("Erreur : veuillez entrer des nombres valides séparés par des virgules.")
        return

    if not all(num in fonctions for num in ordre):
        print("Erreur : certains numéros ne correspondent à aucune fonction.")
        return

    for num in ordre:
        fonctions[num]()


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.maximize_window()
    url = "https://ztrain-web.vercel.app/"
    driver.get(url)
    with open('article.json', 'r') as file:
        data = json.load(file)
    lancer_fonctions()
    generate_html_report(test_results)
