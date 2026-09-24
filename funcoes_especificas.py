import time
from datetime import date, timedelta
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def pesquisar(driver, pesquisa, realizar_pesquisa):

    campo = None
    if realizar_pesquisa: 
        for i in range(30):
            campo = driver.execute_script(
                "return document.querySelector('#COMP3056')"
            )

            if campo:
                break

            time.sleep(3)
        if not campo:
            print("Campo #COMP3056 não encontrado.")
            return

        shadow = driver.execute_script(
            "return arguments[0].shadowRoot",
            campo
        )

        input_real = shadow.find_element(
            "css selector",
            "input"
        )

        input_real.click()

    

        # # ==========================================================
        # # TESTE 2 - HOME + SHIFT + END + BACKSPACE
        # # ==========================================================

        # print("TESTE 2 - HOME + SHIFT+END + BACKSPACE")

        # input_real.send_keys(Keys.HOME)

        # actions = ActionChains(driver)
        # actions.key_down(Keys.SHIFT)
        # actions.send_keys(Keys.END)
        # actions.key_up(Keys.SHIFT)
        # actions.send_keys(Keys.BACKSPACE)
        # actions.perform()

        # time.sleep(3)


        # # ==========================================================
        # # TESTE 3 - END + vários BACKSPACE
        # # ==========================================================

        # print("TESTE 3 - END + BACKSPACE")

        # input_real.send_keys(Keys.END)

        # for _ in range(100):
        #     input_real.send_keys(Keys.BACKSPACE)

        # time.sleep(3)
        # ==========================================================
        # TESTE 4 - JavaScript .value = ''
        # ==========================================================

        print("TESTE 4 - JavaScript value")

        driver.execute_script("""
            arguments[0].focus();
            arguments[0].value = '';

            arguments[0].dispatchEvent(
                new Event('input', { bubbles: true })
            );

            arguments[0].dispatchEvent(
                new Event('change', { bubbles: true })
            );
        """, input_real)

        time.sleep(5)
        # # ==========================================================
        # # TESTE 5 - JavaScript select()
        # # ==========================================================

        # print("TESTE 5 - JavaScript select")

        # driver.execute_script("""
        #     arguments[0].focus();
        #     arguments[0].select();
        # """, input_real)

        # input_real.send_keys(Keys.BACKSPACE)

        # time.sleep(3)
        # # ==========================================================
        # # TESTE 6 - HOME + SHIFT + END
        # # ==========================================================

        # print("TESTE 6 - seleção completa")

        # input_real.click()
        # input_real.send_keys(Keys.HOME)

        # actions = ActionChains(driver)
        # actions.key_down(Keys.SHIFT)
        # actions.send_keys(Keys.END)
        # actions.key_up(Keys.SHIFT)
        # actions.send_keys(Keys.BACKSPACE)
        # actions.perform()

        # time.sleep(3)
        # ==========================================================
        # DIGITA A PESQUISA
        # ==========================================================

        print("Digitando:", pesquisa)

        input_real.send_keys(pesquisa)
        input_real.send_keys(Keys.TAB)

        time.sleep(10)

        # ==========================================================
        # CLICA NO BOTÃO
        # ==========================================================

    btn = driver.find_element(
        By.CSS_SELECTOR,
        "button.button-image"
    )
    for _ in range (0, 6): 
        time.sleep(0.3)
        try: 
            btn.click()
            break
        except: 
            pass

def retorna_datas_MATR260():

    hoje = date.today()

    # Último dia do mês anterior
    ultimo_dia_mes_1 = (
        hoje.replace(day=1) - timedelta(days=1)
    )

    # Último dia de dois meses atrás
    ultimo_dia_mes_2 = (
        ultimo_dia_mes_1.replace(day=1) - timedelta(days=1)
    )

    return (
        ultimo_dia_mes_1.strftime("%d/%m/%Y"),
        ultimo_dia_mes_2.strftime("%d/%m/%Y")
    )


def retorna_datas_MATR900():

    hoje = date.today()

    # Último dia do mês anterior
    ultimo_dia_mes_anterior = (
        hoje.replace(day=1) - timedelta(days=1)
    )

    # Primeiro dia do mês anterior
    primeiro_dia_mes_anterior = (
        ultimo_dia_mes_anterior.replace(day=1)
    )

    return (
        primeiro_dia_mes_anterior.strftime("%d/%m/%Y"),
        ultimo_dia_mes_anterior.strftime("%d/%m/%Y")
    )

def renomear_download(nome, texto):
    import os
    import subprocess
    import time

    print("========================================")
    print("FECHANDO MICROSOFT EDGE")
    print("========================================")

    # Fecha o Microsoft Edge
    subprocess.run(
        ["taskkill", "/F", "/IM", "msedge.exe"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    # Dá um pequeno tempo para o Windows liberar os arquivos
    time.sleep(2)

    # ============================================================
    # Caminhos
    # ============================================================

    pasta = os.path.join(
        os.path.expanduser("~"),
        "Desktop",
        "Arquivos_Protheus"
    )

    caminho_atual = os.path.join(
        pasta,
        nome
    )

    # ============================================================
    # Extensão original
    # ============================================================

    extensao = os.path.splitext(nome)[1]

    # ============================================================
    # Limpar caracteres inválidos
    # ============================================================

    texto = str(texto).strip()

    caracteres_invalidos = '<>:"/\\|?*'

    for caractere in caracteres_invalidos:
        texto = texto.replace(caractere, "-")

    # Remove pontos/espaços no final
    texto = texto.rstrip(" .")

    caminho_novo = os.path.join(
        pasta,
        texto + extensao
    )

    print("\n========================================")
    print("CAMINHOS")
    print("========================================")

    print("Pasta:")
    print(pasta)

    print("\nArquivo atual:")
    print(caminho_atual)

    print("\nNovo arquivo:")
    print(caminho_novo)

    # ============================================================
    # Verificar arquivo atual
    # ============================================================

    if not os.path.exists(caminho_atual):

        print(
            "\nERRO: arquivo original não encontrado:"
        )

        print(caminho_atual)

        return False

    # ============================================================
    # Verificar se novo nome já existe
    # ============================================================

    if os.path.exists(caminho_novo):

        print(
            "\nERRO: já existe um arquivo com o novo nome:"
        )

        print(caminho_novo)

        return False

    # ============================================================
    # Renomear
    # ============================================================

    print("\n========================================")
    print("RENOMEANDO")
    print("========================================")

    for tentativa in range(10):

        try:

            os.rename(
                caminho_atual,
                caminho_novo
            )

            print(
                f"\nArquivo renomeado com sucesso "
                f"na tentativa {tentativa + 1}."
            )

            print(
                "Novo nome:",
                os.path.basename(caminho_novo)
            )

            return True

        except PermissionError as e:

            print(
                f"Arquivo ainda bloqueado "
                f"(tentativa {tentativa + 1}/10):"
            )

            print(e)

            time.sleep(3)

        except FileNotFoundError as e:

            print(
                f"Arquivo não encontrado: {e}"
            )

            return False

        except FileExistsError as e:

            print(
                f"O arquivo de destino já existe: {e}"
            )

            return False

        except Exception as e:

            print(
                f"Erro ao renomear "
                f"(tentativa {tentativa + 1}/10):"
            )

            print(e)

            time.sleep(3)

    # ============================================================
    # Falha final
    # ============================================================

    print(
        "\n========================================"
    )

    print(
        "ERRO: não foi possível renomear o arquivo."
    )

    print(
        "========================================"
    )

    return False

def encontrar_txtPath(driver, timeout=30):
    import time

    fim = time.time() + timeout

    while time.time() < fim:

        try:
            elemento = driver.execute_script("""
                function procurar(root) {

                    if (!root) {
                        return null;
                    }

                    // Procura o txtPath neste nível
                    if (root.querySelector) {
                        const encontrado = root.querySelector("#txtPath");

                        if (encontrado) {
                            return encontrado;
                        }
                    }

                    // Procura recursivamente nos Shadow DOMs
                    if (root.querySelectorAll) {

                        const elementos = root.querySelectorAll("*");

                        for (const elemento of elementos) {

                            if (elemento.shadowRoot) {

                                const encontrado =
                                    procurar(elemento.shadowRoot);

                                if (encontrado) {
                                    return encontrado;
                                }
                            }
                        }
                    }

                    return null;
                }

                return procurar(document);
            """)

            if elemento:
                print("txtPath encontrado!")
                return elemento

        except Exception as e:
            print("Erro durante busca:", e)

        time.sleep(0.5)

    raise Exception(
        f"txtPath não encontrado após {timeout} segundos."
    )
def encontrar_elemento_shadow(driver, seletor, timeout=30):
    import time

    fim = time.time() + timeout

    while time.time() < fim:

        elemento = driver.execute_script("""
            const seletor = arguments[0];

            function procurar(root) {

                if (!root) {
                    return null;
                }

                // Procura neste nível
                if (root.querySelector) {
                    const encontrado = root.querySelector(seletor);

                    if (encontrado) {
                        return encontrado;
                    }
                }

                // Procura dentro dos Shadow DOMs
                if (root.querySelectorAll) {

                    for (const elemento of root.querySelectorAll("*")) {

                        if (elemento.shadowRoot) {

                            const encontrado =
                                procurar(elemento.shadowRoot);

                            if (encontrado) {
                                return encontrado;
                            }
                        }
                    }
                }

                return null;
            }

            return procurar(document);
        """, seletor)

        if elemento:
            return elemento

        time.sleep(0.5)

    raise Exception(
        f"Elemento {seletor} não encontrado após {timeout} segundos."
    )