from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas


banco = mysql.connector.connect(
    host = "localhost",
    user = "",
    password = "",
    database = "Cadastro"
)

def salvar_dados():
    #Busca os dados para editar
    codigo = editar.codigo.text()
    descricao = editar.descricao.text()
    preco = editar.preco.text()
    categoria = editar.categoria.text()
    #Atualiza os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = {}".format (codigo, descricao.title(), preco, categoria, valor_id))
    editar.close()
    lista.close()
    banco.commit()


def editar_produtos():
    global valor_id
    linha = lista.tabela_produtos.currentRow()
    lista.tabela_produtos.removeRow(linha)
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    comando_SQL = "SELECT * FROM produtos WHERE id="+ str(valor_id)
    cursor.execute(comando_SQL)
    registro = cursor.fetchall()
    editar.show()
    editar.id.setText(str(registro[0][0]))
    editar.codigo.setText(str(registro[0][1]))
    editar.descricao.setText(str(registro[0][2]))
    editar.preco.setText(str(registro[0][3]))
    editar.categoria.setText(str(registro[0][4]))
    banco.commit()

#Função que apaga um registro
def excluir_produtos():
    #Pega a linha do resgistro selecionado
    linha = lista.tabela_produtos.currentRow()
    #Exclui apenas da interface gráfica
    lista.tabela_produtos.removeRow(linha)
    #Exclui do banco de dados
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    #Pega o ID da linha para excluir o registro
    valor_id = dados_lidos[linha][0]
    comando_SQL = "DELETE FROM produtos WHERE id="+ str(valor_id)
    cursor.execute(comando_SQL)
    banco.commit()



def gera_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("Cadastro de Produtos.pdf")
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(200, 800, "Produtos Cadastrados:")
    pdf.setFont("Times-Bold", 15)
    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CÓDIGO")
    pdf.drawString(210, 750, "PRODUTO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y += 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))
    pdf.save()
    print("PDF gerado com Sucesso!")


def funcao_principal():
    codigo_cadastrado = cadastro.codigo.text()
    descricao_cadastrada = cadastro.descricao.text().title()
    preco_cadastrado = cadastro.preco.text()
    print("Código:", codigo_cadastrado)
    print("Descrição:", descricao_cadastrada)
    print("Preço", preco_cadastrado)
    
    if cadastro.informatica.isChecked():
        print("Categoria Informática")
        categoria = 'Informática'
    elif cadastro.alimentos.isChecked():
        print("Categoria Alimentos")
        categoria = 'Alimentos'
    elif cadastro.eletronicos.isChecked():
        print("Categoria Eletrônicos")
        categoria = 'Eletrônicos'
    

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (%s, %s, %s, %s)"
    dados = (str(codigo_cadastrado), str(descricao_cadastrada), str(preco_cadastrado), str(categoria))
    cursor.execute(comando_SQL, (dados))
    banco.commit()

    # Comando para limpar os campos depois de inserir os dados na tabela
    cadastro.codigo.setText("")
    cadastro.descricao.setText("")
    cadastro.preco.setText("")

def mostra_produtos():
    lista.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT*FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    lista.tabela_produtos.setRowCount(len(dados_lidos))
    lista.tabela_produtos.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0,5):
            lista.tabela_produtos.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))




app = QtWidgets.QApplication([])
cadastro = uic.loadUi("cadastro.ui")
lista = uic.loadUi("lista.ui")
editar = uic.loadUi("editar.ui")
cadastro.enviar.clicked.connect(funcao_principal)
cadastro.listar.clicked.connect(mostra_produtos)
lista.gerar_pdf.clicked.connect(gera_pdf)
lista.excluir.clicked.connect(excluir_produtos)
lista.editar.clicked.connect(editar_produtos)
editar.salvar.clicked.connect(salvar_dados)

cadastro.show()
app.exec()