# AutoPP

## Visão Geral
O **AutoPP** é uma ferramenta automatizada para gerenciar repositórios Git de forma intuitiva e eficiente. Com uma interface amigável baseada em **CustomTkinter**, ele permite que os usuários realizem operações comuns do Git, como inicializar repositórios, fazer commits, realizar push e pull, além de armazenar configurações personalizadas (presets) para facilitar o trabalho repetitivo.

## Funcionalidades
- Interface gráfica moderna e intuitiva
- Inicialização automática de repositórios Git
- Adição de repositórios remotos
- Commit e push com mensagens personalizadas
- Pull e reset forçado para sincronização com repositórios remotos
- Gerenciamento de presets para salvar caminhos e URLs frequentes

## Tecnologias Utilizadas
- **Python** 3
- **CustomTkinter** para a interface gráfica
- **Git** para gerenciamento de controle de versão
- **JSON** para armazenamento de presets

## Instalação
### 1. Requisitos
Antes de instalar, certifique-se de ter os seguintes requisitos atendidos:
- Python 3.6+
- Git instalado e configurado no sistema

### 2. Clonar o repositório
```sh
 git clone https://github.com/gabrielbtt/AutoPP.git
 cd AutoPP
```

### 3. Instalar dependências
```sh
pip install -r requirements.txt
```

### 4. Executar a aplicação
```sh
python AutoPP.py
```

## Uso
1. **Selecionar a pasta** do repositório local.
2. Se o repositório ainda não existir, o AutoPP o inicializará automaticamente.
3. **(Opcional)** Adicionar a URL do repositório remoto.
4. Preencher uma mensagem de commit e clicar em **Enviar** para realizar o push.
5. Utilizar a função de presets para salvar caminhos e URLs frequentemente usadas.

## Contribuição
Contribuições são bem-vindas! Para contribuir:
1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b minha-feature`)
3. Commit suas mudanças (`git commit -m 'Adicionando uma nova funcionalidade'`)
4. Push para sua branch (`git push origin minha-feature`)
5. Abra um Pull Request

## Licença
Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato
Desenvolvido por [Gabriel Batista](https://www.linkedin.com/in/gabrielbtt/)

Para mais informações ou sugestões, entre em contato via Linkedin.
