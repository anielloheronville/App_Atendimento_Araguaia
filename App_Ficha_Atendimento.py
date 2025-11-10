import flask
from flask import Flask, request, render_template_string, jsonify, Response
# import sqlite3
import psycopg2  # Substituído sqlite3 por psycopg2
import base64
import os
import datetime

# --- Configuração da Aplicação ---
app = Flask(__name__)

# --- Variável de Ambiente do Banco de Dados ---
# O Render irá injetar esta variável automaticamente
DATABASE_URL = os.environ.get('DATABASE_URL')

# --- Dados do Logo (embutido) ---
# O logo 'araguaia_imoveis_logo.jpg' foi codificado em Base64 e embutido aqui
# para que o script seja um arquivo único.
# CORREÇÃO: Renomeado de LOGO_BASE6S_STRING para LOGO_BASE64_STRING
LOGO_BASE64_STRING = (
    "/9j/4AAQSkZJRgABAQEAYABgAAD/4QAiRXhpZgAATU0AKgAAAAgAAQESAAMAAAABAAEAAAAAAAD/2wBDAAIBAQIBAQIB"
    "AQQCAQIEAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBgcLDAsKDAwL/2wBDAQICAgQDBAUD"
    "BgYFBAQGBQcFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU/8AAEQgB9AH0AwEi"
    "AAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUS"
    "ITEGEkFRB2FxEyIygQgUQpGhscEJIzNS8BVictEKFiQ04SXxFxgZGiYnKCkqNTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZ"
    "naGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5u"
    "fo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAEC"
    "AxEEIRIxAUFRB2FxEyIyBkgUobHwI1cRcsEJIzNS8BVictEKFicKGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2Rl"
    "ZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OX"
    "m5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
    "KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK"
ServicesKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA/9k="
)

# --- Configuração do Banco de Dados ---
# DATABASE_FILE = 'araguaia.db' # Não é mais usado

def init_db():
    """Cria a tabela do banco de dados PostgreSQL se ela não existir."""
    
    if not DATABASE_URL:
        print("A variável de ambiente DATABASE_URL não está definida. O banco de dados não pode ser inicializado.")
        return

    # A sintaxe de criação da tabela foi ajustada para PostgreSQL
    create_table_query = '''
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
        assinatura TEXT
    )
    '''
    
    try:
        # Usa 'with' para garantir que a conexão e o cursor sejam fechados
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute(create_table_query)
        print("Tabela 'atendimentos' verificada/criada com sucesso no PostgreSQL.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados PostgreSQL: {e}")

# --- Template HTML (com Tailwind CSS e JavaScript) ---
# Todo o frontend está contido nesta string
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
        .form-input, .form-textarea {
            background-color: #5a616c;
            border: 1px solid var(--cor-borda);
            color: var(--cor-texto-claro);
            border-radius: 0.375rem;
            padding: 0.75rem;
            width: 100%;
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
                
                <!-- Coluna Esquerda -->
                <div class="flex flex-col gap-5">
                    <div>
                        <label for="nome" class="block text-sm font-medium mb-2">Nome*</label>
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

                <!-- Coluna Direita -->
                <div class="flex flex-col gap-5">
                    <!-- Foto do Cliente -->
                    <div>
                        <label class="block text-sm font-medium mb-2">Foto do Cliente</label>
                        <div class="flex items-center gap-4">
                            <canvas id="photoCanvas" class="photo-canvas w-24 h-24 rounded-full"></canvas>
                            <!-- Elementos de vídeo (inicialmente ocultos) -->
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
                            <span class="block text-sm font-medium mb-2">Já esteve em um dos plantões de atendimento da Araguaia Imóveis?*</span>
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
                            <label for="nome_corretor" class="block text-sm font-medium mb-2">Se sim, qual o nome:</label>
                            <input type="text" id="nome_corretor" name="nome_corretor" class="form-input">
                        </div>

                        <div>
                            <span class="block text-sm font-medium mb-2">Autoriza a empresa Araguaia Imóveis te inserir na lista de transmissões de lançamentos?*</span>
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
                    <span class="text-sm text-gray-300" id="dataAtual">Sorriso/MT, 10/11/2025</span>
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
            const today = new Date();
            const dataFormatada = today.toLocaleDateString('pt-BR');
            document.getElementById('dataAtual').innerText = `Sorriso/MT, ${dataFormatada}`;
            document.getElementById('currentYear').innerText = today.getFullYear();

            // --- CÂMERA (FOTO DO CLIENTE) ---
            const video = document.getElementById('videoPreview');
            const photoCanvas = document.getElementById('photoCanvas');
            const photoCtx = photoCanvas.getContext('2d');
            const startWebcamBtn = document.getElementById('startWebcam');
            const takePhotoBtn = document.getElementById('takePhoto');
            const clearPhotoBtn = document.getElementById('clearPhoto');
            const fotoHiddenInput = document.getElementById('foto_cliente_base64');
            let stream = null;

            // Desenha um avatar placeholder
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
                    alert("Não foi possível acessar a câmera. Verifique as permissões.");
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

            // --- CAMPO CONDICIONAL (NOME CORRETOR) ---
            const atendidoSim = document.getElementById('atendido_sim');
            const atendidoNao = document.getElementById('atendido_nao');
            const campoNomeCorretor = document.getElementById('campoNomeCorretor');

            function toggleNomeCorretor() {
                if (atendidoSim.checked) {
                    campoNomeCorretor.classList.remove('hidden');
                    document.getElementById('nome_corretor').required = true;
                } else {
                    campoNomeCorretor.classList.add('hidden');
                    document.getElementById('nome_corretor').required = false;
                }
            }
            atendidoSim.addEventListener('change', toggleNomeCorretor);
            atendidoNao.addEventListener('change', toggleNomeCorretor);

            // --- ASSINATURA CANVAS ---
            const sigCanvas = document.getElementById('signatureCanvas');
            const sigCtx = sigCanvas.getContext('2d');
            const clearSignatureBtn = document.getElementById('clearSignature');
            const assinaturaHiddenInput = document.getElementById('assinatura_base64');
            let drawing = false;
            let dirty = false;

            // Ajustar o tamanho do canvas para corresponder ao CSS
            function resizeCanvas() {
                const rect = sigCanvas.getBoundingClientRect();
                sigCanvas.width = rect.width;
                sigCanvas.height = rect.height;
            }
            window.addEventListener('resize', resizeCanvas);
            resizeCanvas();

            sigCtx.strokeStyle = "#FFFFFF"; // Cor da linha
            sigCtx.lineWidth = 2;

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
                    // Salva a assinatura no campo oculto
                    assinaturaHiddenInput.value = sigCanvas.toDataURL('image/png');
                }
                e.preventDefault();
            }

            // Eventos do Mouse
            sigCanvas.addEventListener('mousedown', startDrawing);
            sigCanvas.addEventListener('mousemove', draw);
            sigCanvas.addEventListener('mouseup', stopDrawing);
            sigCanvas.addEventListener('mouseout', stopDrawing);
            
            // Eventos de Toque (para mobile)
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

                // Validação simples
                const nome = document.getElementById('nome').value;
                const telefone = document.getElementById('telefone').value;
                if (!nome || !telefone) {
                    showStatus('Por favor, preencha os campos obrigatórios (Nome e Telefone).', 'erro');
                    saveButton.disabled = false;
                    saveButton.innerText = 'Salvar Ficha';
                    return;
                }

                // Coletar dados do formulário
                const formData = new FormData(form);
                const data = {};
                formData.forEach((value, key) => {
                    data[key] = value;
                });
                
                // Converte valores 'sim'/'nao' para 1/0
                data.esteve_plantao = data.esteve_plantao === 'sim' ? 1 : 0;
                data.foi_atendido = data.foi_atendido === 'sim' ? 1 : 0;
                data.autoriza_transmissao = data.autoriza_transmissao === 'sim' ? 1 : 0;

                // Adiciona os dados Base64 dos canvases
                data.foto_cliente_base64 = fotoHiddenInput.value;
                data.assinatura_base64 = assinaturaHiddenInput.value;

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
    - GET: Exibe o formulário HTML.
    - POST: Recebe os dados do formulário (JSON) e salva no banco PostgreSQL.
    """
    if request.method == 'POST':
        
        if not DATABASE_URL:
            return jsonify({'success': False, 'message': 'Configuração do banco de dados não encontrada.'}), 500

        try:
            data = request.json
            
            # Dados principais
            nome = data.get('nome')
            telefone = data.get('telefone')
            rede_social = data.get('rede_social')
            abordagem_inicial = data.get('abordagem_inicial')
            
            # Converte 1/0 (do JS) para True/False (para o PostgreSQL)
            esteve_plantao = data.get('esteve_plantao') == 1
            foi_atendido = data.get('foi_atendido') == 1
            nome_corretor = data.get('nome_corretor') if foi_atendido else None
            autoriza_transmissao = data.get('autoriza_transmissao') == 1
            
            # Dados Base64 (foto e assinatura)
            foto_cliente_base64 = data.get('foto_cliente_base64')
            assinatura_base64 = data.get('assinatura_base64')
            
            # Data/Hora (com fuso horário UTC, recomendado para BDs)
            data_hora = datetime.datetime.now(datetime.timezone.utc)

            # Validação básica no servidor
            if not nome or not telefone:
                return jsonify({'success': False, 'message': 'Nome e Telefone são obrigatórios.'}), 400

            # Inserir no banco de dados
            # A sintaxe de placeholders mudou de '?' para '%s'
            insert_query = '''
                INSERT INTO atendimentos (
                    data_hora, nome, telefone, rede_social, abordagem_inicial, 
                    esteve_plantao, foi_atendido, nome_corretor, autoriza_transmissao, 
                    foto_cliente, assinatura
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            values = (
                data_hora, nome, telefone, rede_social, abordagem_inicial,
                esteve_plantao, foi_atendido, nome_corretor, autoriza_transmissao,
                foto_cliente_base64, assinatura_base64
            )
            
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_query, values)
            
            return jsonify({'success': True, 'message': 'Ficha salva com sucesso!'})

        except Exception as e:
            print(f"Erro ao salvar no banco: {e}")
            return jsonify({'success': False, 'message': f"Erro interno do servidor: {e}"}), 500

    # Método GET: Apenas exibe a página
    return render_template_string(HTML_TEMPLATE)


@app.route('/logo.jpg')
def serve_logo():
    """
    Esta rota decodifica a string Base64 do logo e a serve como uma imagem JPEG.
    O HTML usa <img src="/logo.jpg"> para acessá-la.
    """
    try:
        # A variável com o nome correto (LOGO_BASE64_STRING) é usada aqui
        image_data = base64.b64decode(LOGO_BASE64_STRING)
        return Response(image_data, mimetype='image/jpeg')
    except Exception as e:
        print(f"Erro ao servir logo: {e}")
        return "Erro no logo", 500

# --- Execução da Aplicação ---
if __name__ == '__main__':
    if not DATABASE_URL:
        print("---------------------------------------------------------------")
        print("ATENÇÃO: A variável de ambiente DATABASE_URL não está definida.")
        print("Para testes locais, defina-a. Ex (Linux/Mac):")
        print("export DATABASE_URL='postgresql://user:pass@host:port/dbname'")
        print("Ex (Windows):")
        print("set DATABASE_URL='postgresql://user:pass@host:port/dbname'")
        print("---------------------------------------------------------------")
    
    print("Iniciando o banco de dados...")
    init_db()
    
    print("Iniciando a aplicação Flask...")
    print("Acesse o aplicativo em: http://127.0.0.1:5000")
    # app.run(debug=True)
    
    # Usando 'host="0.0.0.0"' para tornar acessível na rede local (ex: por tablets)
    app.run(host='0.0.0.0', port=5000, debug=True)