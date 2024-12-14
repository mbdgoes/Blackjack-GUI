# Trabalho Prático - Teste de Software

### Integrantes
- Marcelo Lommez Rodrigues de Jesus
- Mateus Brandão Damasceno Góes
<hr></hr>

### **Blackjack usando a GUI do Tkinter**
Este projeto é um jogo de blackjack desenvolvido em Python com uma interface gráfica criada usando Tkinter. Ele permite que o jogador jogue contra o dealer, incorporando funcionalidades como apostas, controle de fichas, registro de estatísticas do jogador (vitórias, derrotas, empates e sessões jogadas), e um sistema de log das partidas. Além disso, o jogo inclui opções para salvar logs e visualizar estatísticas diretamente pela interface

### **Descrição das tecnologias usadas**
- **Python**: Linguagem principal usada no desenvolvimento
- **Tkinter**: Biblioteca padrão do Python para criação de interfaces gráficas de usuário (GUIs). Tkinter fornece um conjunto de widgets e ferramentas que permitem a criação de janelas, botões, labels e outros componentes interativos de forma simples e eficiente.
- **Pillow**: Biblioteca para manipulação de imagens em Python. No projeto, é utilizada para redimensionar e exibir as imagens das cartas no jogo de forma otimizada
- **Pytest**: Framework de testes automatizados para Python. O Pytest permite a criação de testes unitários e funcionais de maneira concisa e mais simples que o unittest.
- **Coverage.py**: Ferramenta que mede a cobertura de testes no código Python. Coverage.py analisa quais partes do código são executadas durante os testes, ajudando a identificar áreas não cobertas e a melhorar a qualidade dos testes.
- **Codecov**: Serviço de integração contínua que gera relatórios detalhados de cobertura de código. O Codecov ajuda a monitorar a qualidade do código ao longo do desenvolvimento, exibindo métricas de cobertura e garantindo que o código mantenha uma boa cobertura de testes.


### Instruções de instalação
1. Requerimentos:
```bash
sudo apt-get update
sudo apt-get install python3-tk python3-pil.imagetk
```
2. Clonar o repositório:
```bash
git clone https://github.com/mbdgoes/Blackjack-GUI.git
cd /Blackjack-GUI
```
3. Instalar as dependências do Python:
```bash
pip install -r requirements.txt
```
4. Rodar o programa:
```bash
python3 main.py
```
