IBGE - Cadastro Nacional para fins estatísticos
===============================================

Essa ferramenta é útil para processamento dos dados do cadastro nacional para fins 
estatísticos. Ela percorre os arquivos disponibilizados no [Servidor FTP do IBGE](ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Cadastro_Nacional_de_Enderecos_Fins_Estatisticos/)
e recria a estrutura em formato JSON para fácil manipulação.

Execução
========

Para execução do código, basta popular a pasta **data/** com os arquivos baixados e descompactados do link acima, do 
seguinte modo:

    data/
        AC/
            10000...TXT
            10001...TXT
            ...
        AL/
            20000...TXT
            20001...TXT
        ...
        TO/
            99998...TXT
            99999...TXT

E executar o seguinte comando:

    $ python extract.py

Compatibilidade
===============

Este utilitário foi desenvolvido usando:

* Python 3.5.1
* Requests 2.9.1
* python-decouple 3.0

Suporte
=======

Esta é uma ferramenta em desenvolvimento e testes. Para qualquer problema ou dúvida, utilize Issues do repositório.

Contato
=======

Caso queira entrar em contato pessoalmente, meu e-mail é *hrqnogueira* [at] *gmail* [dot] *com*.
Tentarei responder assim que possível.