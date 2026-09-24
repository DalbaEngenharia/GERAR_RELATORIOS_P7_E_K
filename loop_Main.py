from listas import armazens
from biblioteca_protheus import *
from funcoes_especificas import *
import traceback


def loop(driver):
    log("Iniciando loop de pesquisas.")

    pesquisas = ["MATR260", "MATR260", "MATR900"]

    try:
        for index_pesquisa, pesquisa in enumerate(pesquisas):
            log(f"Iniciando pesquisa {pesquisa} - índice {index_pesquisa}.")

            try:
                if pesquisa == "MATR260":
                    data1, data2 = retorna_datas_MATR260()
                else:
                    data1, data2 = retorna_datas_MATR900()

                log(f"Datas obtidas: {data1} --- {data2}")

                realizar_pesquisa = True

                for armazen in armazens:
                    log(f"Iniciando {pesquisa} para o armazém {armazen}.")

                    try:
                        for _ in range(0, 6):
                            pesquisar(driver, pesquisa, realizar_pesquisa)
                            realizar_pesquisa = False

                            time.sleep(5)

                            log("Preenchendo parâmetros da pesquisa.")

                            try:
                                esperar_existir(
                                    driver,
                                    "wa-button",
                                    "Confirmar"
                                )

                                inserir_texto(
                                    driver,
                                    "COMP4512",
                                    "030201"
                                )

                                break

                            except Exception:
                                continue

                        textos = ["Confirmar", "Planilha", "Outras"]

                        for index, texto in enumerate(textos):
                            log(f"Selecionando opção: {texto}")

                            funcao_tres_e_demais(
                                driver,
                                "wa-button",
                                texto
                            )

                            if texto != "Outras":
                                esperar_existir(
                                    driver,
                                    "wa-button",
                                    textos[index + 1]
                                )

                        funcao_tres_e_demais(
                            driver,
                            "wa-menu-popup-item",
                            "P"
                        )

                        if pesquisa != "MATR900":
                            log(f"Configurando parâmetros do {pesquisa}.")

                            inserir_texto(driver, "COMP6018", armazen)
                            time.sleep(0.5)

                            inserir_texto(driver, "COMP6020", armazen)
                            time.sleep(0.5)

                            inserir_texto(driver, "COMP6022", "")
                            time.sleep(0.5)

                            inserir_texto(
                                driver,
                                "COMP6024",
                                "zzzzzzzzzzzzzzz"
                            )

                            if index_pesquisa == 0:
                                inserir_texto(
                                    driver,
                                    "COMP6054",
                                    data1,
                                    enter=True
                                )
                            else:
                                inserir_texto(
                                    driver,
                                    "COMP6054",
                                    data2,
                                    enter=True
                                )

                        else:
                            log("Configurando parâmetros do MATR900.")

                            inserir_texto(driver, "COMP6016", armazen)
                            time.sleep(0.5)

                            inserir_texto(driver, "COMP6018", armazen)
                            time.sleep(0.5)

                            inserir_texto(driver, "COMP6020", data1)
                            time.sleep(0.5)

                            inserir_texto(
                                driver,
                                "COMP6022",
                                data2,
                                enter=True
                            )

                        time.sleep(1)

                        funcao_tres_e_demais(
                            driver,
                            "wa-button",
                            "OK"
                        )

                        log("Configurando combos do relatório.")

                        driver.execute_script("""
                            const combo = document
                                .querySelector('#COMP4554')
                                .shadowRoot
                                .querySelector('select');

                            combo.value = '2';

                            combo.dispatchEvent(
                                new Event('change', {
                                    bubbles: true
                                })
                            );
                        """)

                        driver.execute_script("""
                            const combo = document
                                .querySelector('#COMP4556')
                                .shadowRoot
                                .querySelector('select');

                            combo.value = '2';

                            combo.dispatchEvent(
                                new Event('change', {
                                    bubbles: true
                                })
                            );
                        """)

                        time.sleep(3)

                        radio = driver.find_element(
                            By.CSS_SELECTOR,
                            "#COMP4560"
                        )

                        shadow = driver.execute_script(
                            "return arguments[0].shadowRoot",
                            radio
                        )

                        paisagem = shadow.find_element(
                            By.CSS_SELECTOR,
                            "#radio-1"
                        )

                        driver.execute_script(
                            "arguments[0].click();",
                            paisagem
                        )

                        log("Iniciando impressão.")

                        funcao_tres_e_demais(
                            driver,
                            "wa-button",
                            "mprimir"
                        )

                        time.sleep(5)

                        #######################

                        campo = encontrar_txtPath(driver)

                        shadow_root = campo.shadow_root

                        input_real = shadow_root.find_element(
                            By.CSS_SELECTOR,
                            "input[type='text']"
                        )

                        input_real.click()
                        input_real.clear()

                        input_real.send_keys(
                            r"C:\Users\DALBAPY\Desktop\Arquivos_Protheus"
                        )

                        time.sleep(5)

                        botao = encontrar_elemento_shadow(
                            driver,
                            "#btnConfirm"
                        )

                        botao.click()

                        #######################

                        log("Aguardando finalização do download.")

                        esperar_existir(
                            driver,
                            "wa-button",
                            "im"
                        )

                        time.sleep(3)

                        try:
                            driver.find_element(
                                By.ID,
                                "COMP6012"
                            ).click()

                        except Exception:
                            pass

                        esperar_sumir_panel(
                            driver,
                            "Cancelar"
                        )

                        time.sleep(10)

                        if index_pesquisa == 0:
                            dia_renomear = data1
                            nome = "matr260.xml"

                        elif index_pesquisa == 1:
                            dia_renomear = data2
                            nome = "matr260.xml"

                        else:
                            dia_renomear = f"{data1}-{data2}"
                            nome = "matr900.xml"

                        texto = (
                            f"{pesquisas[index_pesquisa]}_"
                            f"{armazen}_"
                            f"{dia_renomear}"
                        )

                        log(
                            f"Renomeando arquivo: "
                            f"{nome} -> {texto}"
                        )

                        renomear_download(nome, texto)

                        log(
                            f"Pesquisa {pesquisa} do armazém "
                            f"{armazen} concluída."
                        )

                    except Exception as erro_armazen:
                        log(
                            f"ERRO na pesquisa {pesquisa} "
                            f"do armazém {armazen}: {erro_armazen}"
                        )

                        log(
                            f"TRACEBACK:\n"
                            f"{traceback.format_exc()}"
                        )

                        # Continua para o próximo armazém
                        continue

            except Exception as erro_pesquisa:
                log(
                    f"ERRO na pesquisa {pesquisa} "
                    f"(índice {index_pesquisa}): {erro_pesquisa}"
                )

                log(
                    f"TRACEBACK:\n"
                    f"{traceback.format_exc()}"
                )

                # Continua para a próxima pesquisa
                continue

    except Exception as erro_geral:
        log(f"ERRO GERAL NA EXECUÇÃO DO LOOP: {erro_geral}")

        log(
            f"TRACEBACK COMPLETO:\n"
            f"{traceback.format_exc()}"
        )

        raise

    log("Todas as pesquisas foram concluídas.")