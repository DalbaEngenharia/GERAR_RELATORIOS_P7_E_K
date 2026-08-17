##################
from listas import armazens
from biblioteca_protheus import *
from funcoes_especificas import *

def loop(driver): 
    pesquisas = ["MATR260","MATR260","MATR900"]
    for index_pesquisa, pesquisa in enumerate(pesquisas):
        if pesquisa == "MATR260":
            data1, data2 = retorna_datas_MATR260()
        else: 
            data1, data2 = retorna_datas_MATR900()
        print(data1,"---", data2)
        realizar_pesquisa = True
        for armazen in armazens: 
            pesquisar(driver,pesquisa,realizar_pesquisa)
            realizar_pesquisa = False
            esperar_existir(driver,"wa-button","Confirmar")
            textos = ["Confirmar","Planilha","Outras"]
            for index, texto in enumerate(textos):
                funcao_tres_e_demais(driver,"wa-button",texto)
                if texto != "Outras": 
                    esperar_existir(driver,"wa-button",textos[index+1])

            funcao_tres_e_demais(driver,"wa-menu-popup-item","P")
            if pesquisa != "MATR900":
                inserir_texto(driver,"COMP6018",armazen)
                time.sleep(0.5)
                inserir_texto(driver,"COMP6020",armazen)
                time.sleep(0.5)
                if index_pesquisa == 0:
                    inserir_texto(driver,"COMP6054",data1,enter=True)
                else: 
                    inserir_texto(driver,"COMP6054",data2,enter=True)
            else: 
                inserir_texto(driver,"COMP6016",armazen)
                time.sleep(0.5)
                inserir_texto(driver,"COMP6018",armazen)
                time.sleep(0.5)
                inserir_texto(driver,"COMP6020",data1)
                time.sleep(0.5)
                inserir_texto(driver,"COMP6022",data2, enter=True)
            
            time.sleep(1)
            funcao_tres_e_demais(driver,"wa-button","OK")
            driver.execute_script(f"""
                const combo = document
                    .querySelector('#COMP4554')
                    .shadowRoot
                    .querySelector('select');

                combo.value = '2';

                combo.dispatchEvent(
                    new Event('change', {{
                        bubbles: true
                    }})
                );
            """)
            time.sleep(3)
            radio = driver.find_element(By.CSS_SELECTOR, "#COMP4560")
            shadow = driver.execute_script("return arguments[0].shadowRoot", radio)
            paisagem = shadow.find_element(By.CSS_SELECTOR, "#radio-1")
            driver.execute_script("arguments[0].click();",paisagem)

            funcao_tres_e_demais(driver,"wa-button", "mprimir")
            time.sleep(5)
            #######################
            campo = encontrar_txtPath(driver)

            # Acessa o Shadow DOM do wa-simple-input-text
            shadow_root = campo.shadow_root

            # Pega o input real
            input_real = shadow_root.find_element(
                By.CSS_SELECTOR,
                "input[type='text']"
            )

            # Preenche
            input_real.click()
            input_real.clear()
            input_real.send_keys(
                r"C:\Users\gustavo.elicker\Desktop\ARQ_HOMOLOG"
            )          
            time.sleep(5)
            botao = encontrar_elemento_shadow(
                driver,
                "#btnConfirm"
            )

            botao.click()            
            #######################            
            esperar_existir(driver,"wa-button","im")
            time.sleep(3)
            #            
            try: 
                driver.find_element(By.ID, "COMP6012").click()
            except: 
                pass
            #Scriptfind(driver,item="wa-button")    
            esperar_sumir_panel(driver,"Cancelar")
            time.sleep(10)
            #esperar_existir(driver,"wa-menu-button","tualizações")
            if index_pesquisa == 0: 
                dia_renomear = data1
                nome = "matr260.xml"
            if index_pesquisa == 1:
                dia_renomear = data2
                nome = "matr260.xml"
            if index_pesquisa == 2:
                dia_renomear = f"{data1}-{data2}"
                nome = "matr900.xml"

            texto = f"{pesquisas[index_pesquisa]}_{armazen}_{dia_renomear}"
            print(f"renomeando: {texto}")
            renomear_download(nome, texto)
            #renomear_download()
            None


