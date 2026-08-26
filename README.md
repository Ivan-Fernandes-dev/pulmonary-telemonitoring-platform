⁹# Plataforma Inteligente de Telemonitoramento da Recuperação Pulmonar

alteração Kelvin

## Smart Pulmonary Recovery Telemonitoring Platform

## Descrição

A Plataforma Inteligente de Telemonitoramento da Recuperação Pulmonar é um sistema desenvolvido para o monitoramento remoto de pacientes em recuperação pulmonar utilizando Internet das Coisas (IoT), ESP32, sensores biomédicos e uma plataforma web.

O sistema realiza a coleta, armazenamento e visualização de dados fisiológicos e ambientais por meio de um dashboard intuitivo, permitindo o acompanhamento da evolução do paciente e servindo como base para futuras aplicações em saúde.

Esta é a Versão 1 (MVP) do projeto, desenvolvida para validar a arquitetura do sistema, a comunicação entre hardware e software e as principais funcionalidades da plataforma.

## Objetivos

- Monitorar remotamente pacientes em recuperação pulmonar.
- Coletar e armazenar dados fisiológicos e ambientais.
- Disponibilizar as informações em uma plataforma web.
- Facilitar o acompanhamento da evolução do paciente.
- Servir como base para pesquisas e desenvolvimento tecnológico.

## Tecnologias Utilizadas

### Hardware

- ESP32 DevKit
- Sensores IoT
- Comunicação Wi-Fi

### Software

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

## Funcionalidades da Versão 1 (MVP)

- Dashboard Web
- Cadastro de medições
- Banco de dados SQLite
- Visualização dos dados
- Relatórios
- Exportação de dados
- Integração inicial com ESP32
- Integração inicial com sensores IoT

## Estrutura do Projeto

```
/
├── estatico/
├── modelos/
├── app.py
├── database.py
├── requirements.txt
└── README.md
```

## Arquitetura do Sistema

```
Sensores IoT
      │
      ▼
    ESP32
      │
      ▼
Servidor Flask
      │
      ▼
Banco de Dados SQLite
      │
      ▼
 Dashboard Web
      │
      ▼
 Relatórios
```

## Próximas Etapas

- Cadastro de múltiplos pacientes
- Sistema de autenticação
- Controle de usuários
- Melhorias no dashboard
- Integração completa dos sensores
- Publicação online da plataforma
- Evolução para ambiente clínico

## Equipe

### Ivan Fernandes de Oliveira Filho

- Idealizador do projeto
- Desenvolvedor principal
- Desenvolvimento Backend
- Desenvolvimento Frontend
- Arquitetura do sistema
- Banco de dados
- Integração com ESP32
- Integração dos sensores IoT
- Administração do projeto e do repositório GitHub

### Kelvin Bruno de Oliveira

- Desenvolvedor colaborador
- Desenvolvimento Backend
- Desenvolvimento Frontend
- Integração com ESP32
- Integração dos sensores IoT
- Desenvolvimento de novas funcionalidades
- Correção de bugs e melhorias

## Status do Projeto

**Versão:** MVP 1.0

**Status:** Em desenvolvimento.
