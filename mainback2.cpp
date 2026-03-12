#include <iostream>
#include <string>
#include <iomanip>
#include <algorithm>
#include <memory>

#include <jdbc/mysql_driver.h>
#include <jdbc/mysql_connection.h>
#include <jdbc/cppconn/prepared_statement.h>
#include <jdbc/cppconn/resultset.h>

using namespace std;

struct Produto {
    string codigo;
    string nome;
    double quantidade;
    double preco_custo;
};

sql::mysql::MySQL_Driver* driver;
unique_ptr<sql::Connection> con;

// ---------------- CONEXÃO ----------------

void conectarBanco() {
    driver = sql::mysql::get_mysql_driver_instance();
    con.reset(driver->connect("tcp://127.0.0.1:3306", "root", "FDSGZ26a!eSoF"));
    con->setSchema("material_construcao");
}

// ---------------- ENTRADA SEGURA ----------------

long double lerLongDoubleSeguro(string mensagem) {
    string entrada;
    long double numero = 0.0;
    bool valido = false;

    do {
        cout << mensagem;
        getline(cin, entrada);

        entrada.erase(remove(entrada.begin(), entrada.end(), ' '), entrada.end());
        replace(entrada.begin(), entrada.end(), ',', '.');

        if (entrada.empty()) continue;

        try {
            size_t processado;
            numero = stold(entrada, &processado);
            if (processado == entrada.length()) {
                valido = true;
            } else {
                cout << "[ERRO] Digite apenas numeros validos!\n";
            }
        } catch (...) {
            cout << "[ERRO] Entrada invalida. Tente novamente.\n";
        }
    } while (!valido);

    return numero;
}

// ---------------- BANCO DE DADOS ----------------

bool produtoExiste(string codigo) {
    auto stmt = con->prepareStatement(
        "SELECT COUNT(*) as total FROM produtos WHERE codigo=?"
    );

    stmt->setString(1, codigo);
    auto res = stmt->executeQuery();

    if (res->next()) {
        return res->getInt("total") > 0;
    }

    return false;
}

Produto buscarProduto(string codigo) {
    Produto p;

    auto stmt = con->prepareStatement(
        "SELECT * FROM produtos WHERE codigo=?"
    );

    stmt->setString(1, codigo);
    auto res = stmt->executeQuery();

    if (res->next()) {
        p.codigo = res->getString("codigo");
        p.nome = res->getString("nome");
        p.quantidade = res->getDouble("quantidade");
        p.preco_custo = res->getDouble("preco_custo");
    }

    return p;
}

void inserirProduto(Produto p) {
    auto stmt = con->prepareStatement(
        "INSERT INTO produtos (codigo,nome,quantidade,preco_custo) VALUES (?,?,?,?)"
    );

    stmt->setString(1, p.codigo);
    stmt->setString(2, p.nome);
    stmt->setDouble(3, p.quantidade);
    stmt->setDouble(4, p.preco_custo);

    stmt->execute();
}

void atualizarQuantidade(string codigo, double novaQtd) {
    auto stmt = con->prepareStatement(
        "UPDATE produtos SET quantidade=? WHERE codigo=?"
    );

    stmt->setDouble(1, novaQtd);
    stmt->setString(2, codigo);
    stmt->execute();
}

void deletarProduto(string codigo) {
    auto stmt = con->prepareStatement(
        "DELETE FROM produtos WHERE codigo=?"
    );

    stmt->setString(1, codigo);
    stmt->execute();
}

void listarEstoque() {

    cout << "\n--- ESTOQUE ATUAL ---\n";

    auto stmt = con->prepareStatement("SELECT * FROM produtos");
    auto res = stmt->executeQuery();

    cout << left << setw(10) << "CODIGO"
         << left << setw(20) << "NOME"
         << right << setw(10) << "QTD"
         << right << setw(15) << "PRECO(R$)" << endl;

    cout << "--------------------------------------------------------\n";

    while (res->next()) {

        cout << left << setw(10) << res->getString("codigo")
             << left << setw(20) << res->getString("nome").substr(0,19)
             << right << setw(10) << res->getDouble("quantidade")
             << right << setw(15) << fixed << setprecision(2)
             << res->getDouble("preco_custo") << "\n";
    }
}

// ---------------- MENU PRINCIPAL ----------------

void entradaSaidaEstoque() {

    string codigo;

    cout << "\n--- MOVIMENTACAO ---\n";
    cout << "Codigo do produto: ";
    cin >> codigo;
    cin.ignore();

    bool existe = produtoExiste(codigo);

    if (!existe) {

        cout << "Produto nao cadastrado. Cadastrar agora? (1-Sim / 0-Nao): ";
        int op = (int)lerLongDoubleSeguro("");

        if (op == 1) {

            Produto p;
            p.codigo = codigo;

            cout << "Nome do Material: ";
            getline(cin, p.nome);

            p.quantidade = lerLongDoubleSeguro("Quantidade inicial: ");
            p.preco_custo = lerLongDoubleSeguro("Preco de Custo (unidade): ");

            inserirProduto(p);

            cout << "Produto cadastrado com sucesso!\n";
        }

    } else {

        Produto p = buscarProduto(codigo);

        cout << "\nProduto: " << p.nome << endl;
        cout << "Estoque Atual: " << p.quantidade << endl;
        cout << "Preco: R$ " << p.preco_custo << endl;

        cout << "\n1 - Alterar Quantidade\n";
        cout << "2 - Deletar Produto\n";
        cout << "0 - Cancelar\n";

        int acao = (int)lerLongDoubleSeguro("Opcao: ");

        if (acao == 1) {

            cout << "Digite valor positivo para adicionar ou negativo para remover:\n";
            int qtd = (int)lerLongDoubleSeguro("Quantidade: ");

            double novaQtd = p.quantidade + qtd;

            if (novaQtd < 0) {
                cout << "[ERRO] Estoque ficaria negativo.\n";
            } else {
                atualizarQuantidade(codigo, novaQtd);
                cout << "Atualizado com sucesso!\n";
            }

        } else if (acao == 2) {

            cout << "Tem certeza? (1-Sim / 0-Nao): ";
            int confirma = (int)lerLongDoubleSeguro("");

            if (confirma == 1) {
                deletarProduto(codigo);
                cout << "Produto removido.\n";
            }
        }
    }
}

int main() {

    conectarBanco();

    int opcao;

    do {

        cout << "\n=== CONTROLE DE ESTOQUE ===\n";
        cout << "1. Gerenciar Produto\n";
        cout << "2. Listar Tudo\n";
        cout << "3. Sair\n";

        opcao = (int)lerLongDoubleSeguro("Opcao: ");

        if (opcao == 1) {
            entradaSaidaEstoque();
        } else if (opcao == 2) {
            listarEstoque();
        }

    } while (opcao != 3);

    return 0;
}