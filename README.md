Desafio Técnico - Squad "Melhorias Estruturantes"
Objetivo:
Criar uma API que permita realizar web scraping de informações de uma página pública e processar os dados de forma assíncrona utilizando filas de mensagens. A API deve ser escalável e preparada para ser implantada em um ambiente Docker com RabbitMQ e Redis.

Requisitos Técnicos:
    1. API com FastAPI
    2. Criar uma API utilizando o framework FastAPI com os seguintes endpoints:
        a. POST /scrape: Recebe um CNPJ como entrada e envia a tarefa de scraping para uma fila (RabbitMQ).
        b. GET /results/{task_id}: Retorna o status da tarefa de scraping e, caso esteja concluída, os dados processados.
    3. Processamento Assíncrono com RabbitMQ
Utilizar o RabbitMQ para gerenciar as tarefas de web scraping de forma assíncrona. O serviço de scraping deve pegar as tarefas da fila e processá-las.
    4. Armazenamento Temporário com Redis
Armazenar o status das tarefas e os resultados no Redis para consulta posterior através do endpoint GET /results/{task_id}.
    5. Docker e Docker Compose
Preparar o projeto para ser executado com Docker e Docker Compose. Todos os serviços (API, workers de scraping, RabbitMQ, Redis) devem estar devidamente configurados nos containers.

Instruções para Implementação:
    • Web Scraping:
Realizar o scraping dos dados no seguinte site:
        ◦ URL: Consulta Sintegra - Goiás
        ◦ Dados de entrada: CNPJ
Exemplos de CNPJs para consulta:
            ▪ 00006486000175
            ▪ 00012377000160
            ▪ 00022244000175
        ◦ Extrair as informações principais apresentadas na página para cada CNPJ consultado (razão social, endereço, situação cadastral, etc.).
    • Tarefas Assíncronas:
As tarefas de scraping devem ser enviadas para o RabbitMQ e processadas por workers assíncronos.
    • Redis:
Utilize o Redis para armazenar temporariamente o status e os resultados das tarefas, que poderão ser recuperados via a API.
    • Estrutura do Projeto:
Organize o projeto de forma modular, com arquivos e pastas bem definidas (por exemplo, app/, worker/, docker-compose.yml).

Critérios de Avaliação:
    1. Funcionalidade e Corretude:
        a. A API funciona conforme o esperado? O scraping é realizado corretamente?
        b. O sistema de filas e processamento assíncrono está bem implementado?
    2. Qualidade do Código:
        a. O código é limpo, modular e fácil de entender?
        b. Segue boas práticas de desenvolvimento Python (PEP8)?
    3. Uso de Docker:
        a. O projeto está corretamente configurado para rodar com Docker e Docker Compose?
        b. A arquitetura é escalável e extensível?
    4. Testes:
        a. O candidato incluiu testes automatizados? (Testes unitários para as funções principais são um diferencial)
    5. Documentação:
        a. O projeto está bem documentado, com instruções claras de como rodar o ambiente localmente e explicações sobre a arquitetura?

Entrega:
    • Submeter o projeto em um repositório Git público (GitHub, GitLab, etc.) com todas as instruções no arquivo README.md explicando como rodar o projeto.
    • Prazo de entrega: 5 dias.
