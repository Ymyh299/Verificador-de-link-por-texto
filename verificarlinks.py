from playwright.sync_api import sync_playwright, TimeoutError # type: ignore
import pandas as pd # type: ignore

#lê o arquivo .xlsx que contêm os links, (lê a coluna com indicador "Links")
df_links = pd.read_excel("meus_links.xlsx") #nome do arquivo
links = df_links["Links"].tolist()#nome da coluna

resultados = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) #false se quer ver o playwright abrindo as páginas
    context = browser.new_context()
    page = context.new_page()

    for link in links:
        status = ""
        try:
            page.goto(link, timeout=5000)
            page.get_by_text("Detalhes").wait_for(timeout=3000)#a palavra que procura
            status = "OK"
        except TimeoutError:
            status = "Erro - Texto não encontrado"
        except Exception as e:
            status = f"Falha - {e}"

        resultados.append({"Link": link, "Status": status})

    browser.close()


erros = [r for r in resultados if r["Status"] != "OK"]

if erros:
    df_erros = pd.DataFrame(erros)
    df_erros.to_excel("erros_links.xlsx", index=False) #como ele vai salvar o arquivo
    print("✅ salvos em 'erros_links.xlsx'")
else:
    print("✅ nenhum erro encontrado.")

    #Executar:      python3 verificarlinks.py