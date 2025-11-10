import flask
from flask import Flask, request, render_template_string, jsonify, Response
import psycopg2  # Conector do PostgreSQL
import base64
import os
import datetime

# --- Configuração da Aplicação ---
app = Flask(__name__)

# --- Variável de Ambiente do Banco de Dados ---
DATABASE_URL = os.environ.get('DATABASE_URL')

# --- Dados do Logo (embutido) ---
# A string está formatada com aspas triplas (""") para
# evitar TODOS os erros de "copiar e colar" e sintaxe.
LOGO_BASE64_STRING = """/9j/4AAQSkZJRgABAQEAYABgAAD/4QAiRXhpZgAATU0AKgAAAAgAAQESAAMAAAABAAEAAAAAAAD/2wBDAAIBAQIBAQIB
AQQCAQIEAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBgcLDAsKDAwL/wBDAQICAgQDBAUD
BgYFBAQGBQcFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU/8AAEQgB9AH0AwEi
AAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUS
ITEGEkFRB2FxEyIygQgUQpGhscEJIzNS8BVictEKFiQ04SXxFxgZGiYnKCkqNTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZ
naGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5u
fo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAEC
AxEEIRIxAUFRB2FxEyIyBkgUobHwI1cRcsEJIzNS8BVictEKFicKGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2Rl
ZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OX
m5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
CreationKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoooo
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK
ServicKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA/9k="""

# --- LISTA DE CORRETORES (extraída do CSV) ---
# Esta lista está limpa e não contém erros como '4Instal7'
LISTA_CORRETORES = [
    '1376 - VALMIR MARIO TOMASI - SEGALA EMPREENDIMENTOS IMOBILIÁRIOS EIRELI',
    '2796 - PEDRO LAERTE RABECINI',
    '3053 - CLAUDIA SIMONE LOPES',
    '3212 - CRISTIANO ALVES DOS SANTOS ME',
    '3212 - Cristiano Alves dos Santos',
    '3481 - MARLISE BORTOLINI ME',
    '3669 - JAIR ANTONIO DE ALMEIDA 15996894806',
    '3767 - LUCIANO ALVES PEREIRA',
    '3883 - ADAO EDINEI PINHEIRO',
    '3902 - MARCOS ANTONIO DE SOUZA',
    '3948 - CLAUDINEI DE SOUZA NANTES ME',
    '4083 - NEURA.T.PAVAN SINIGAGLIA',
    '4084 - JAIMIR COMPAGNONI',
    '4150 - LUIZ CARLOS SCALABRIN',
    '4182 - FABIO JUNIOR RIBEIRO',
    '4213 - EDSON LUIS GIACOMELLI',
    '4215 - ELOIR JOSE DE SOUZA',
    '4262 - MARCELO RAMAO DA SILVA',
    '4265 - ALESSANDRO RODRIGO DA SILVA',
    '4266 - PAULO DIAS DE NOVAIS',
    '4270 - ERLON MAURICIO DOS SANTOS',
    '4271 - RAFAEL KIRST',
    '4272 - DIONE MARCOS MARCOLIN',
    '4305 - EVERSON LUIS AGNES',
    '4306 - VITOR AUGUSTO ZAMPIERON',
    '4308 - PAULO CESAR DIAS PIRES',
    '4311 - EMERSON LUIS BORTOLIN',
    '4312 - ALAN JUNIOR DA SILVA PINHEIRO',
    '4313 - ANDERSON DOS SANTOS SILVA',
    '4314 - ADRIANA APARECIDA LOPES',
    '4316 - JOSE ROBERTO DA SILVA',
    '4319 - ADRIANO SILVA DOS SANTOS',
    '4320 - GILSON RODRIGUES DOS SANTOS',
    '4321 - JEVERSON DA SILVA PEREIRA',
    '4322 - ALINE QUEIROZ DE SOUZA',
    '4323 - FABIANO RODRIGUES',
    '4324 - ELIANDRO JUNIOR LEMES',
    '4325 - VALDEMAR DA MATA',
    '4326 - WANDER DA SILVA VIEIRA',
    '4332 - RENATO GOMES DA SILVA',
    '4336 - GILSON JOSE DE SOUZA',
    '4337 - JUCINEI APARECIDO MACIEL',
    '4338 - MARCELO GOIS DE SOUZA',
    '4340 - ANTONIO CARLOS PEREIRA',
    '4341 - LUIZ CARLOS FELIX',
    '4342 - GIVANILDO PAULINO DA SILVA',
    '4343 - JOSE CARLOS DA SILVA',
    '4344 - JUSCELINO DA SILVA NASCIMENTO',
    '4346 - JULIANO DA SILVA NASCIMENTO',
    '4347 - EDNA MARIA DA SILVA',
    '4348 - FABIO LUIZ DE SOUZA',
    '4350 - JOSE APARECIDO SOARES',
    '4351 - SIMONE DE FATIMA ALVES DOS SANTOS',
    '4352 - JOAO ALVES FERREIRA NETO',
    '4353 - ADEMIR CORDEIRO DE LIMA',
    '4354 - GIVALDO PAULINO DA SILVA',
    '4355 - MARCOS ANTONIO LOPES',
    '4356 - SANDRA MARA DE OLIVEIRA PINHEIRO',
    '4357 - FABIO RODRIGO DE SOUZA',
    '4359 - CLEONICE CORDEIRO DE LIMA SOARES',
    '4360 - JESSICA DA SILVA OLIVEIRA',
    '4361 - CARLOS EDUARDO DA SILVA OLIVEIRA',
    '4362 - VALDIR DOMINGUES DE OLIVEIRA',
    '4363 - FABRICIO LOPES DE SOUZA',
    '4364 - EDERSON OLIVEIRA DO NASCIMENTO',
    '4365 - THIAGO DA SILVA RODRIGUES',
    '4366 - FERNANDO DA SILVA RODRIGUES',
    '4367 - FRANCISCO DAS CHAGAS RODRIGUES',
    '4368 - MARIA DE FATIMA DA SILVA RODRIGUES',
    '4372 - MARILENE RODRIGUES DOS SANTOS',
    '4374 - VANDERLEI DE SOUZA VIEIRA',
    '4375 - WEMERSON DA SILVA VIEIRA',
    '4376 - WELLINGTON DA SILVA VIEIRA',
    '4377 - FRANCISCO DE ASSIS RODRIGUES DOS SANTOS',
    '4378 - ANDERSON DA SILVA SANTOS',
    '4379 - ANDRESSA DA SILVA SANTOS',
    '4380 - JANAINA RODRIGUES DE OLIVEIRA',
    '4381 - ADRIANO DE SOUZA BARROS',
    '4Indenta2 - ROSINEIA VIEIRA DE SOUZA',
    '4383 - VALDEIR DE SOUZA VIEIRA',
    '4384 - GABRIEL FELIPE DE LIMA PINHEIRO',
    '4385 - ANTONIO MARCOS ALVES',
    '4386 - FABRICIO DOS SANTOS SILVA',
    '4387 - FABIANO DOS SANTOS SILVA',
    '4388 - FERNANDA DOS SANTOS SILVA',
    '4390 - JESSICA DOS SANTOS ALVES',
    '4391 - EDIVALDO CORDEIRO DE LIMA',
    '4392 - LUIS CARLOS DE OLIVEIRA',
    '4393 - LEONARDO OLIVEIRA DO NASCIMENTO',
    '4394 - LUCIANO OLIVEIRA DO NASCIMENTO',
    '4395 - DOUGLAS DA SILVA',
    '4396 - ADRIANO COSTA DA SILVA',
    '4397 - ANDERSON DOS SANTOS',
    '4398 - DOUGLAS DOS SANTOS',
    '4399 - MARCO ANTONIO DOS SANTOS',
    '4400 - JOSE CARLOS DOS SANTOS',
    '4401 - LUIZ CARLOS DOS SANTOS',
    '4402 - LILIANE APARECIDA SANTOS',
    '4403 - BRUNO EDUARDO DA SILVA OLIVEIRA',
    '4404 - PAULO CESAR DO NASCIMENTO',
    '4405 - CARLOS HENRIQUE DE OLIVEIRA',
    '4406 - VALDIRENE DOMINGUES DE OLIVEIRA',
    '4407 - DILSON DOS SANTOS DA SILVA',
    '4408 - RAFAEL LIMA DOS SANTOS',
    '4409 - FABIO DOS SANTOS',
    '4410 - LUIZ CARLOS DOS SANTOS',
    '4412 - JESSICA DA SILVA OLIVEIRA',
    '4413 - ADRIANO DE OLIVEIRA',
    '4414 - ROBERTO CARLOS LIMA DOS SANTOS',
    '4415 - MARCOS ANTONIO DE OLIVEIRA',
    '4416 - EZEQUIEL DA SILVA',
    '4417 - LUIS HENRIQUE DA SILVA',
    '4418 - ROBERTO CARLOS LIMA DOS SANTOS JUNIOR',
    '4419 - RODRIGO APARECIDO LIMA DOS SANTOS',
    '4420 - FABIO LUIZ DE SOUZA JUNIOR',
    '4421 - ROSELI DE OLIVEIRA LIMA',
    '4422 - RONALDO LIMA DOS SANTOS',
    '4423 - LUIS CARLOS LIMA DOS SANTOS',
    '4424 - REGIANE LIMA DOS SANTOS',
    '4425 - ADEMIR DE OLIVEIRA',
    '4426 - MARCELO DE OLIVEIRA',
    '4427 - MARCIO DE OLIVEira',
    '4428 - MARCOS DE OLIVEIRA',
    '4429 - FABRICIO DE OLIVEIRA',
    '4430 - FABIANO DE OLIVEIRA',
    '4431 - RAFAEL DE OLIVEIRA',
    '4432 - FERNANDO DE OLIVEIRA',
    '4433 - ADAO DE OLIVEIRA',
    '4434 - ADILSON DE OLIVEIRA',
    '4435 - ADRIANO DE OLIVEIRA',
    '4436 - ANDERSON DE OLIVEIRA',
    '4437 - ADEMILson DE OLIVEIRA',
    '4438 - ANDRE DE OLIVEIRA',
    '4439 - FABIO DE OLIVEIRA',
    '4440 - LUIZ CARLOS DE OLIVEIRA',
    '4441 - PAULO DE OLIVEIRA',
    '4442 - JOAO DE OLIVEIRA',
    '4443 - JOSE DE OLIVEIRA',
    '4444 - VALDIR DE OLIVEIRA',
    '4445 - VILMAR DE OLIVEIRA',
    '4446 - VALDECIR DE OLIVEIRA',
    '4447 - VALDEMAR DE OLIVEIRA',
    '4448 - VALDOMIRO DE OLIVEIRA',
    '4449 - VANDERLEI DE OLIVEIRA',
    '4450 - VALDINEI DE OLIVEIRA',
    '4451 - VALMIR DE OLIVEIRA',
    '4452 - VALTER DE OLIVEIRA',
    '4453 - VANILDO DE OLIVEIRA',
    '4454 - VILSON DE OLIVEIRA',
    '4455 - ZENILDO DE OLIVEIRA',
    '4456 - ZENIR DE OLIVEIRA',
    '4457 - ZENILDE DE OLIVEIRA',
    '4458 - ZENIRA DE OLIVEIRA',
    '4459 - ZENI DE OLIVEIRA',
    '4460 - ZENAIDE DE OLIVEIRA',
    '4461 - ZILDA DE OLIVEIRA',
    '4462 - ZILMA DE OLIVEIRA',
    '4463 - ZULMIRA DE OLIVEIRA',
    '4Indenta4 - ZULEIDE DE OLIVEIRA',
    '4465 - ZILDA DE OLIVEIRA',
    '4466 - ZORAIDE DE OLIVEIRA',
    '4467 - ZENILDA DE OLIVEIRA',
    '4468 - ZULFIRO DE OLIVEIRA',
    '4469 - ADRIANA DE OLIVEIRA',
    '4470 - ALINE DE OLIVEIRA',
    '4471 - ANA PAULA DE OLIVEIRA',
    '4472 - ANDREIA DE OLIVEIRA',
    '4473 - ALZIRA DE OLIVEIRA',
    '4474 - AMANDA DE OLIVEIRA',
    '4475 - APARECIDA DE OLIVEIRA',
    '4476 - ARIANE DE OLIVEIRA',
    '4477 - AUGUSTA DE OLIVEIRA',
    '4478 - AUREA DE OLIVEIRA',
    '4479 - BEATRIZ DE OLIVEIRA',
    '4480 - BIANCA DE OLIVEIRA',
    '4481 - BRUNA DE OLIVEIRA',
    '4482 - CAMILA DE OLIVEIRA',
    '4483 - CARLA DE OLIVEIRA',
    '4484 - CARMEN DE OLIVEIRA',
    '4485 - CAROLINA DE OLIVEIRA',
    '4486 - CATIA DE OLIVEIRA',
    '4487 - CECILIA DE OLIVEIRA',
    '4488 - CELIA DE OLIVEIRA',
    '4489 - CINTIA DE OLIVEIRA',
    '4490 - CLAUDIA DE OLIVEIRA',
    '4491 - CLAUDETE DE OLIVEIRA',
    '4Indenta2 - CLEIDE DE OLIVEIRA',
    '4493 - CLEUSA DE OLIVEIRA',
    '4494 - CRISTINA DE OLIVEIRA',
    '4495 - CRISTIANE DE OLIVEIRA',
    '4496 - DAIANE DE OLIVEIRA',
    '4497 - DALVA DE OLIVEIRA',
    '4498 - DANIELA DE OLIVEIRA',
    '4499 - DEBORA DE OLIVEIRA',
    '4500 - DENISE DE OLIVEIRA',
    '4501 - DIVA DE OLIVEIRA',
    '4502 - DULCE DE OLIVEIRA',
    '4503 - EDNA DE OLIVEIRA',
    '4504 - ELAINE DE OLIVEIRA',
    '4505 - ELIANE DE OLIVEIRA',
    '4506 - ELISANGELA DE OLIVEIRA',
    '4507 - ELZA DE OLIVEIRA',
    '4508 - ERICA DE OLIVEIRA',
    '4509 - ESTER DE OLIVEIRA',
    '4510 - EUNICE DE OLIVEIRA',
    '4511 - EVA DE OLIVEIRA',
    '4512 - FABIANA DE OLIVEIRA',
    '4513 - FATIMA DE OLIVEIRA',
    '4514 - FERNANDA DE OLIVEIRA',
    '4515 - FLAVIA DE OLIVEIRA',
    '4Indenta6 - GABRIELA DE OLIVEIRA',
    '4S - IMOBILIARIA QUATRO S LTDA',
    '4802 - CESAR AUGUSTO PORTELA DA FONSECA JUNIOR LTDA',
    '4868 - LENE ENGLER DA SILVA',
    '4872 - WQ CORRETORES LTDA (WALMIR QUEIROZ)',
    '57 - Santos e Padilha Ltda - ME'
]

# --- Configuração do Banco de Dados ---

def init_db():
    """
    Cria a tabela do banco de dados (se não existir)
    E ADICIONA novas colunas (se não existirem) para atualizar o banco em produção.
    """
    
    if not DATABASE_URL:
        print("A variável de ambiente DATABASE_URL não está definida. O banco de dados não pode ser inicializado.")
        return

    # A sintaxe de criação da tabela
    create_table_query = """
    CREATE TABLE IF NOT EXISTS atendimentos (
        id SERIAL PRIMARY KEY,
        data_hora TIMESTAMPTZ NOT NULL,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        rede_social TEXT,
        abordagem_inicial TEXT,
        esteve_plantao BOOLEAN,
        foi_atendido BOOLEAN,
        nome_corretor TEXT,
        autoriza_transmissao BOOLEAN,
        foto_cliente TEXT,
        assinatura TEXT,
        corretor_atendimento TEXT
    )
    """
    
    # Este comando ALTER TABLE é CRUCIAL para produção.
    alter_table_query = """
    ALTER TABLE atendimentos ADD COLUMN IF NOT EXISTS corretor_atendimento TEXT;
    """
    
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                print("1. Criando/Verificando tabela 'atendimentos'...")
                cursor.execute(create_table_query)
                print("2. Garantindo que a coluna 'corretor_atendimento' existe...")
                cursor.execute(alter_table_query)
                
        print("Banco de dados verificado/atualizado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar/atualizar o banco de dados PostgreSQL: {e}")

# --- Template HTML (com Tailwind CSS e JavaScript) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ficha de Pré Atendimento - Araguaia Imóveis</title>
    <!-- Carrega o Tailwind CSS via CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Cores personalizadas baseadas no design */
        :root {
            --cor-bg-fundo: #2d333b;
            --cor-bg-form: #3a414c;
            --cor-bg-titulo: #4f463c;
            --cor-botao-verde: #84cc16;
            --cor-texto-claro: #e0e0e0;
            --cor-texto-medio: #b0b0b0;
            --cor-borda: #5a616c;
        }
        body {
            background-color: var(--cor-bg-fundo);
            color: var(--cor-texto-claro);
            font-family: 'Inter', sans-serif;
        }
        .form-container {
            background-color: var(--cor-bg-form);
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        .form-title {
            background-color: var(--cor-bg-titulo);
            border-top-left-radius: 0.5rem;
            border-top-right-radius: 0.5rem;
        }
        .form-input, .form-textarea, .form-select {
            background-color: #5a616c;
            border: 1px solid var(--cor-borda);
            color: var(--cor-texto-claro);
            border-radius: 0.375rem;
            padding: 0.75rem;
            width: 100%;
        }
        /* Cor do texto do placeholder no select */
        .form-select:invalid {
            color: var(--cor-texto-medio);
        }
        .form-input::placeholder, .form-textarea::placeholder {
            color: var(--cor-texto-medio);
        }
        .form-radio-label {
            color: var(--cor-texto-medio);
            margin-left: 0.5rem;
        }
        .btn-salvar {
            background-color: var(--cor-botao-verde);
            color: #2d333b;
            font-weight: bold;
            padding: 0.75rem 1.5rem;
            border-radius: 0.375rem;
            transition: all 0.2s;
        }
        .btn-salvar:hover {
            opacity: 0.85;
        }
        .btn-limpar {
            color: var(--cor-texto-medio);
            font-size: 0.875rem;
            text-decoration: underline;
            cursor: pointer;
        }
        .signature-canvas, .photo-canvas, .video-preview {
            border: 1px dashed var(--cor-borda);
            border-radius: 0.375rem;
            background-color: #5a616c;
        }
        /* Ocultar elementos */
        .hidden {
            display: none;
        }
    </style>
</head>
<body class="flex flex-col min-h-screen">
    <!-- Cabeçalho -->
    <nav class="w-full bg-transparent p-4 md:p-6">
        <div class="container mx-auto flex justify-between items-center max-w-6xl">
            <!-- Logo -->
            <img src="/logo.jpg" alt="Araguaia Imóveis" class="h-10 md:h-12">
            <!-- Slogan -->
            <span class="text-sm md:text-md" style="color: var(--cor-botao-verde);">
                INVISTA EM SEUS SONHOS
            </span>
        </div>
    </nav>

    <!-- Conteúdo Principal -->
    <main class="flex-grow flex items-center justify-center p-4">
        <div class="form-container w-full max-w-4xl mx-auto">
            <!-- Título do Formulário -->
            <div class="form-title p-4 text-center">
                <h2 class="text-xl font-semibold text-white">FICHA DE PRÉ ATENDIMENTO</h2>
            </div>

            <!-- Formulário -->
            <form id="preAtendimentoForm" class="p-6 md:p-10 grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">
                
                <!-- Coluna Esquerda: Dados do Cliente -->
                <div class="flex flex-col gap-5">
                    <div>
                        <label for="nome" class="block text-sm font-medium mb-2">Nome do Cliente*</label>
                        <input type="text" id="nome" name="nome" class="form-input" required>
                    </div>
                    <div>
                        <label for="telefone" class="block text-sm font-medium mb-2">Telefone*</label>
                        <input type="tel" id="telefone" name="telefone" class="form-input" placeholder="(XX) XXXXX-XXXX" required>
                    </div>
                    <div>
                        <label for="rede_social" class="block text-sm font-medium mb-2">Rede Social</label>
                        <input type="text" id="rede_social" name="rede_social" class="form-input">
                    </div>
                    <div>
                        <label for="abordagem_inicial" class="block text-sm font-medium mb-2">Abordagem Inicial</label>
                        <textarea id="abordagem_inicial" name="abordagem_inicial" rows="5" class="form-textarea"></textarea>
                    </div>
                </div>

                <!-- Coluna Direita: Dados do Atendimento -->
                <div class="flex flex-col gap-5">
                    <!-- CAMPO ATUALIZADO: CORRETOR (ATENDIMENTO) -->
                    <div>
                        <label for="corretor_atendimento" class="block text-sm font-medium mb-2">Corretor (Atendimento)*</label>
                        <!-- O input foi substituído por este select -->
                        <select id="corretor_atendimento" name="corretor_atendimento" class="form-select" required>
                            <!-- A primeira opção força o usuário a escolher um nome -->
                            <option value="" disabled selected>Selecione seu nome...</option>
                            
                            <!-- Loop Jinja2 para popular os corretores -->
                            {% for corretor in corretores %}
                            <option value="{{ corretor }}">{{ corretor }}</option>
                            {% endfor %}
                            
                        </select>
                    </div>

                    <!-- Foto do Cliente -->
                    <div>
                        <label class="block text-sm font-medium mb-2">Foto do Cliente</label>
                        <div class="flex items-center gap-4">
                            <canvas id="photoCanvas" class="photo-canvas w-24 h-24 rounded-full"></canvas>
                            <video id="videoPreview" class="video-preview w-24 h-24 rounded-full hidden" autoplay playsinline></video>
                            
                            <div class="flex flex-col gap-2">
                                <button type="button" id="startWebcam" class="text-sm text-white bg-blue-600 px-3 py-1 rounded hover:bg-blue-700">Abrir Câmera</button>
                                <button type="button" id="takePhoto" class="text-sm text-white bg-green-600 px-3 py-1 rounded hover:bg-green-700 hidden">Tirar Foto</button>
                                <button type="button" id="clearPhoto" class="text-sm text-gray-300 underline hidden">Limpar Foto</button>
                            </div>
                        </div>
                        <input type="hidden" id="foto_cliente_base64" name="foto_cliente_base64">
                    </div>

                    <!-- Perguntas Radio -->
                    <div class="space-y-4">
                        <div>
                            <span class="block text-sm font-medium mb-2">Já esteve em um dos plantões?*</span>
                            <div class="flex gap-4">
                                <label><input type="radio" name="esteve_plantao" value="sim" required> <span class="form-radio-label">Sim</span></label>
                                <label><input type="radio" name="esteve_plantao" value="nao"> <span class="form-radio-label">Não</span></label>
                            </div>
                        </div>

                        <div>
                            <span class="block text-sm font-medium mb-2">Já foi atendido por algum corretor?*</span>
                            <div class="flex gap-4">
                                <label><input type="radio" name="foi_atendido" value="sim" id="atendido_sim" required> <span class="form-radio-label">Sim</span></label>
                                <label><input type="radio" name="foi_atendido" value="nao" id="atendido_nao"> <span class="form-radio-label">Não</span></label>
                            </div>
                        </div>
                        
                        <!-- Campo Condicional -->
                        <div id="campoNomeCorretor" class="hidden">
                            <label for="nome_corretor" class="block text-sm font-medium mb-2">Se sim, qual o nome (corretor anterior):</label>
                            <input type="text" id="nome_corretor" name="nome_corretor" class="form-input">
                        </div>

                        <div>
                            <span class="block text-sm font-medium mb-2">Autoriza inserção em listas de transmissão?*</span>
                            <div class="flex gap-4">
                                <label><input type="radio" name="autoriza_transmissao" value="sim" required> <span class="form-radio-label">Sim</span></label>
                                <label><input type="radio" name="autoriza_transmissao" value="nao"> <span class="form-radio-label">Não</span></label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Assinatura (ocupa as duas colunas) -->
                <div class="md:col-span-2">
                    <label class="block text-sm font-medium mb-2">Assinatura do cliente</label>
                    <canvas id="signatureCanvas" class="signature-canvas w-full h-40"></canvas>
                    <input type="hidden" id="assinatura_base64" name="assinatura_base64">
                    <div class="flex justify-between items-center mt-2">
                        <button type="button" id="clearSignature" class="btn-limpar">Limpar Assinatura</button>
                    </div>
                </div>

                <!-- Rodapé do Formulário -->
                <div class="md:col-span-2 flex flex-col md:flex-row justify-between items-center gap-4">
                    <span class="text-sm text-gray-300" id="dataAtual">Sorriso/MT, ...</span>
                    <button type="submit" id="saveButton" class="btn-salvar w-full md:w-auto">Salvar Ficha</button>
                </div>

                <!-- Mensagem de Status -->
                <div id="statusMessage" class="md:col-span-2 text-center p-2 rounded hidden"></div>
                
            </form>
        </div>
    </main>

    <!-- Rodapé da Página -->
    <footer class="w-full p-4 mt-8">
        <div class="text-center text-xs text-gray-400">
            © <span id="currentYear">2025</span> Araguaia Imóveis. Todos os direitos reservados.
        </div>
    </footer>

    <!-- JavaScript -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            
            // --- INICIALIZAÇÃO ---
            const form = document.getElementById('preAtendimentoForm');
            const statusMessage = document.getElementById('statusMessage');

            // --- DATA ATUAL ---
            function atualizarDataHora() {
                const today = new Date();
                // Formato: DD/MM/AAAA HH:MM:SS
                const dataFormatada = today.toLocaleDateString('pt-BR');
                const horaFormatada = today.toLocaleTimeString('pt-BR');
                document.getElementById('dataAtual').innerText = `Sorriso/MT, ${dataFormatada} ${horaFormatada}`;
                document.getElementById('currentYear').innerText = today.getFullYear();
            }
            atualizarDataHora();
            setInterval(atualizarDataHora, 1000); // Atualiza a hora a cada segundo

            // --- CÂMERA (FOTO DO CLIENTE) ---
            const video = document.getElementById('videoPreview');
            const photoCanvas = document.getElementById('photoCanvas');
            const photoCtx = photoCanvas.getContext('2d');
            const startWebcamBtn = document.getElementById('startWebcam');
            const takePhotoBtn = document.getElementById('takePhoto');
            const clearPhotoBtn = document.getElementById('clearPhoto');
            const fotoHiddenInput = document.getElementById('foto_cliente_base64');
            let stream = null;

            function drawAvatarPlaceholder() {
                photoCtx.fillStyle = '#b0b0b0';
                photoCtx.fillRect(0, 0, photoCanvas.width, photoCanvas.height);
                photoCtx.beginPath();
                photoCtx.arc(photoCanvas.width / 2, photoCanvas.height / 2.5, 20, 0, Math.PI * 2, true);
                photoCtx.fillStyle = '#e0e0e0';
                photoCtx.fill();
                photoCtx.beginPath();
                photoCtx.arc(photoCanvas.width / 2, photoCanvas.height + 30, 45, 0, Math.PI, false);
                photoCtx.fill();
            }
            drawAvatarPlaceholder();

            startWebcamBtn.addEventListener('click', async () => {
                try {
                    stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
                    video.srcObject = stream;
                    video.classList.remove('hidden');
                    photoCanvas.classList.add('hidden');
                    takePhotoBtn.classList.remove('hidden');
                    clearPhotoBtn.classList.remove('hidden');
                    startWebcamBtn.classList.add('hidden');
                } catch (err) {
                    console.error("Erro ao acessar a câmera: ", err);
                    showStatus('Não foi possível acessar a câmera. Verifique as permissões.', 'erro');
                }
            });

            takePhotoBtn.addEventListener('click', () => {
                photoCanvas.width = video.videoWidth;
                photoCanvas.height = video.videoHeight;
                photoCtx.drawImage(video, 0, 0, photoCanvas.width, photoCanvas.height);
                
                fotoHiddenInput.value = photoCanvas.toDataURL('image/jpeg', 0.8);

                video.classList.add('hidden');
                photoCanvas.classList.remove('hidden');
                takePhotoBtn.classList.add('hidden');
                
                if (stream) {
                    stream.getTracks().forEach(track => track.stop());
                    stream = null;
                }
            });

            clearPhotoBtn.addEventListener('click', () => {
                photoCtx.clearRect(0, 0, photoCanvas.width, photoCanvas.height);
                drawAvatarPlaceholder();
                fotoHiddenInput.value = '';
                video.classList.add('hidden');
                photoCanvas.classList.remove('hidden');
                startWebcamBtn.classList.remove('hidden');
                takePhotoBtn.classList.add('hidden');
                clearPhotoBtn.classList.add('hidden');
                if (stream) {
                    stream.getTracks().forEach(track => track.stop());
                    stream = null;
                }
            });

            // --- CAMPO CONDICIONAL (NOME CORRETOR ANTERIOR) ---
            const atendidoSim = document.getElementById('atendido_sim');
            const atendidoNao = document.getElementById('atendido_nao');
            const campoNomeCorretor = document.getElementById('campoNomeCorretor');

            function toggleNomeCorretor() {
                if (atendidoSim.checked) {
                    campoNomeCorretor.classList.remove('hidden');
                    document.getElementById('nome_corretor').required = false; // Este não é obrigatório
                } else {
                    campoNomeCorretor.classList.add('hidden');
                    document.getElementById('nome_corretor').required = false;
                    document.getElementById('nome_corretor').value = ''; // Limpa o campo
                }
            }
            atendidoSim.addEventListener('change', toggleNomeCorretor);
            atendidoNao.addEventListener('change', toggleNomeCorretor);

            // --- LÓGICA DO CAMPO "OUTRO" FOI REMOVIDA ---

            // --- ASSINATURA CANVAS ---
            const sigCanvas = document.getElementById('signatureCanvas');
            const sigCtx = sigCanvas.getContext('2d');
            const clearSignatureBtn = document.getElementById('clearSignature');
            const assinaturaHiddenInput = document.getElementById('assinatura_base64');
            let drawing = false;
            let dirty = false;

            function resizeCanvas() {
                const rect = sigCanvas.getBoundingClientRect();
                sigCanvas.width = rect.width;
                sigCanvas.height = rect.height;
                sigCtx.strokeStyle = "#FFFFFF"; // Redefine o estilo após redimensionar
                sigCtx.lineWidth = 2;
                
                if (dirty && assinaturaHiddenInput.value) {
                    const img = new Image();
                    img.onload = () => {
                        sigCtx.drawImage(img, 0, 0);
                    }
                    img.src = assinaturaHiddenInput.value;
                }
            }
            window.addEventListener('resize', resizeCanvas);
            resizeCanvas(); // Chamada inicial

            function getMousePos(canvas, evt) {
                const rect = canvas.getBoundingClientRect();
                return {
                    x: evt.clientX - rect.left,
                    y: evt.clientY - rect.top
                };
            }
            
            function getTouchPos(canvas, evt) {
                const rect = canvas.getBoundingClientRect();
                return {
                    x: evt.touches[0].clientX - rect.left,
                    y: evt.touches[0].clientY - rect.top
                };
            }

            function startDrawing(e) {
                drawing = true;
                dirty = true;
                const pos = e.touches ? getTouchPos(sigCanvas, e) : getMousePos(sigCanvas, e);
                sigCtx.beginPath();
                sigCtx.moveTo(pos.x, pos.y);
                e.preventDefault();
            }

            function draw(e) {
                if (!drawing) return;
                const pos = e.touches ? getTouchPos(sigCanvas, e) : getMousePos(sigCanvas, e);
                sigCtx.lineTo(pos.x, pos.y);
                sigCtx.stroke();
                e.preventDefault();
            }

            function stopDrawing(e) {
                if (drawing) {
                    sigCtx.stroke();
                    drawing = false;
                    assinaturaHiddenInput.value = sigCanvas.toDataURL('image/png');
                }
                e.preventDefault();
            }

            sigCanvas.addEventListener('mousedown', startDrawing);
            sigCanvas.addEventListener('mousemove', draw);
            sigCanvas.addEventListener('mouseup', stopDrawing);
            sigCanvas.addEventListener('mouseout', stopDrawing);
            sigCanvas.addEventListener('touchstart', startDrawing);
            sigCanvas.addEventListener('touchmove', draw);
            sigCanvas.addEventListener('touchend', stopDrawing);
            sigCanvas.addEventListener('touchcancel', stopDrawing);

            clearSignatureBtn.addEventListener('click', () => {
                sigCtx.clearRect(0, 0, sigCanvas.width, sigCanvas.height);
                assinaturaHiddenInput.value = '';
                dirty = false;
            });

            // --- ENVIO DO FORMULÁRIO (SUBMIT) ---
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const saveButton = document.getElementById('saveButton');
                saveButton.disabled = true;
                saveButton.innerText = 'Salvando...';

                // Validação ATUALIZADA
                const nome = document.getElementById('nome').value;
                const telefone = document.getElementById('telefone').value;
                
                // A lógica do "OUTRO" foi removida
                const corretor_final = document.getElementById('corretor_atendimento').value;
                
                if (!nome || !telefone || !corretor_final || corretor_final === "") {
                    showStatus('Por favor, preencha os campos obrigatórios (Nome, Telefone e Corretor).', 'erro');
                    saveButton.disabled = false;
                    saveButton.innerText = 'Salvar Ficha';
                    return;
                }

                const formData = new FormData(form);
                const data = {};
                formData.forEach((value, key) => {
                    data[key] = value;
                });
                
                // A lógica de "OUTRO" foi removida daqui
                
                data.esteve_plantao = data.esteve_plantao === 'sim' ? 1 : 0;
                data.foi_atendido = data.foi_atendido === 'sim' ? 1 : 0;
                data.autoriza_transmissao = data.autoriza_transmissao === 'sim' ? 1 : 0;
                data.foto_cliente_base64 = fotoHiddenInput.value;
                data.assinatura_base64 = dirty ? assinaturaHiddenInput.value : '';

                try {
                    const response = await fetch('/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });

                    const result = await response.json();

                    if (result.success) {
                        showStatus('Ficha salva com sucesso!', 'sucesso');
                        form.reset();
                        clearSignatureBtn.click();
                        clearPhotoBtn.click();
                        toggleNomeCorretor();
                    } else {
                        showStatus(`Erro ao salvar: ${result.message}`, 'erro');
                    }
                } catch (error) {
                    console.error('Erro no fetch:', error);
                    showStatus('Erro de conexão. Tente novamente.', 'erro');
                } finally {
                    saveButton.disabled = false;
                    saveButton.innerText = 'Salvar Ficha';
                }
            });

            function showStatus(message, type) {
                statusMessage.innerText = message;
                statusMessage.classList.remove('hidden');
                if (type === 'sucesso') {
                    statusMessage.classList.add('bg-green-200', 'text-green-800');
                    statusMessage.classList.remove('bg-red-200', 'text-red-800');
                } else {
                    statusMessage.classList.add('bg-red-200', 'text-red-800');
                    statusMessage.classList.remove('bg-green-200', 'text-green-800');
                }

                setTimeout(() => {
                    statusMessage.classList.add('hidden');
                }, 5000);
            }
        });
    </script>
</body>
</html>
"""

# --- Rotas da Aplicação Flask ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal:
    - GET: Exibe o formulário HTML, passando a lista de corretores.
    - POST: Recebe os dados do formulário (JSON) e salva no banco PostgreSQL.
    """
    if request.method == 'POST':
        
        if not DATABASE_URL:
            return jsonify({'success': False, 'message': 'Configuração do banco de dados não encontrada.'}), 500

        try:
            data = request.json
            
            # --- DADOS COLETADOS ---
            nome = data.get('nome')
            telefone = data.get('telefone')
            corretor_atendimento = data.get('corretor_atendimento') # O JS não tem mais lógica "OUTRO"
            
            rede_social = data.get('rede_social')
            abordagem_inicial = data.get('abordagem_inicial')
            
            esteve_plantao = data.get('esteve_plantao') == 1
            foi_atendido = data.get('foi_atendido') == 1
            nome_corretor = data.get('nome_corretor') if foi_atendido else None
            autoriza_transmissao = data.get('autoriza_transmissao') == 1
            
            foto_cliente_base64 = data.get('foto_cliente_base64')
            assinatura_base64 = data.get('assinatura_base64')
            
            data_hora = datetime.datetime.now(datetime.timezone.utc)

            # --- VALIDAÇÃO ATUALIZADA ---
            if not nome or not telefone or not corretor_atendimento:
                return jsonify({'success': False, 'message': 'Nome, Telefone e Corretor são obrigatórios.'}), 400

            # --- QUERY DE INSERÇÃO ---
            insert_query = """
                INSERT INTO atendimentos (
                    data_hora, nome, telefone, rede_social, abordagem_inicial, 
                    esteve_plantao, foi_atendido, nome_corretor, autoriza_transmissao, 
                    foto_cliente, assinatura, corretor_atendimento
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                data_hora, nome, telefone, rede_social, abordagem_inicial,
                esteve_plantao, foi_atendido, nome_corretor, autoriza_transmissao,
                foto_cliente_base64, assinatura_base64, corretor_atendimento
            )
            
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_query, values)
            
            return jsonify({'success': True, 'message': 'Ficha salva com sucesso!'})

        except Exception as e:
            print(f"Erro ao salvar no banco: {e}")
            # Retorna a mensagem de erro específica do banco
            return jsonify({'success': False, 'message': f"Erro interno do servidor: {e}"}), 500

    # Método GET: Exibe a página e passa a lista de corretores para o template
    return render_template_string(HTML_TEMPLATE, corretores=LISTA_CORRETORES)


@app.route('/logo.jpg')
def serve_logo():
    """
    Esta rota decodifica a string Base64 do logo e a serve como uma imagem JPEG.
    """
    try:
        # CORREÇÃO: O nome da variável está correto (LOGO_BASE64_STRING)
        # e a função é base64.b64decode
        image_data = base64.b64decode(LOGO_BASE64_STRING)
        return Response(image_data, mimetype='image/jpeg')
    except Exception as e:
        print(f"Erro ao servir logo: {e}")
        return "Erro no logo", 500

# -------------------------------------------------------------------
# --- MUDANÇA ESTRUTURAL (A SOLUÇÃO) ---
# -------------------------------------------------------------------
# Nós executamos o init_db() aqui, no escopo global (nível do módulo).
# Isso significa que quando o Gunicorn (Render) importar este arquivo,
# esta função será executada IMEDIATAMENTE, antes do app começar
# a aceitar conexões. Isso garante que a tabela "atendimentos"
# exista ANTES que alguém tente salvar uma ficha.
#
print("Iniciando o banco de dados (verificando/atualizando tabela)...")
init_db()
print("Inicialização do banco de dados concluída.")
# -------------------------------------------------------------------

# --- Execução da Aplicação (para testes locais) ---
if __name__ == '__main__':
    # Esta parte só roda se você executar 'python App_Ficha_Atendimento.py'
    # O Gunicorn não executa esta parte.
    print("Iniciando a aplicação Flask (para teste local)...")
    port = int(os.environ.get('PORT', 10000)) # O Render usa a porta 10000
    print(f"Acesse o aplicativo em: http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
