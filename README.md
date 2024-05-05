# Pylon Identity

## Descrição
Pylon Identity é uma biblioteca de gerenciamento de identidade e acesso, construída sobre a biblioteca [Pylon](https://github.com/marcorsouza/pylon). Ela oferece funcionalidades avançadas de autenticação e autorização, ideal para aplicações FastAPI que necessitam de um sistema de gerenciamento de usuários robusto e flexível.

## Funcionalidades
- Autenticação de usuários e gerenciamento de sessões
- Controle de acesso baseado em roles e permissões
- Suporte para tokens JWT
- Fácil integração com FastAPI e outras frameworks web Python
- Interface de administração para gerenciamento de usuários, roles e permissões

## Pré-requisitos
Este projeto requer Python 3.11+ e [Poetry](https://python-poetry.org/) como gerenciador de dependências.

## Instalação

Primeiramente, clone o repositório do Pylon Identity:

```bash
git clone https://github.com/marcorsouza/pylon_identity.git
cd pylon_identity
```

Como o Pylon Identity depende da biblioteca Pylon, é necessário adicioná-la como dependência. Se você está utilizando Poetry, pode fazer isso diretamente:

```bash
poetry add git+https://github.com/marcorsouza/pylon.git
```

Em seguida, instale as dependências restantes do projeto:

```bash
poetry install
```

## Configuração

Detalhe quaisquer passos necessários para configurar o projeto, incluindo a configuração de variáveis de ambiente, arquivos de configuração necessários, e como gerar chaves secretas para a autenticação JWT.

## Uso

## Contribuindo
Contribuições são muito bem-vindas! Se você tem interesse em melhorar o Pylon Identity, veja nosso guia de contribuição para saber como começar.

## Licença
Este projeto é licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.