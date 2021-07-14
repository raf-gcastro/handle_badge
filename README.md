# Pré-requisitos:
* Instalação do Python3 (https://www.python.org/)
    * `$ sudo apt update && sudo apt install python3`
* Instalação do Pip3
    * `$ sudo apt install python3-pip`
* Instalação de dependências:
    * `$ pip3 install Unidecode`
    * `$ pip3 install python-Levenshtein`
* Caso o gateway não esteja instalado no diretório raiz do seu usuário (`$HOME/gateway`), será necessário atualizar a variável `GW_DIR` (presente em `bin/handle_city_badge.sh`)

# Uso:
1. Baixe uma imagem no formato .png, .jpeg ou .jpg contendo o brasão município;
2. Renomeie-a para o nome tokenizado do município. Ex.: `curitiba.png`
3. Execute:
`$ ./bin/handle_city_badge.sh curitiba.png`
4. Confirme o nome e a UF do município digitando o número correspondente, seguido de `Enter`:
>
```
Por favor, confirme o nome da cidade e a UF:
--------------------------------------------
0: Curitiba - PR [Enter]

1: Muritiba - BA
2: Piritiba - BA
3: Peritiba - SC
--------------------------------------------
Insira o número correspondente à opção:

```
> Observação: caso seja a opção número 0, apenas pressione `Enter`.

5. Verifique o brasão salvo no caminho exibido.
`Brasão salvo em: /[...]/gateway/public/images/brasao-4106902.png`
