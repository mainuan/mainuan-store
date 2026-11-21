# Changelog

Todas as alterações relevantes deste projeto são registadas neste ficheiro.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-PT/1.1.0/).

## [0.6.3] - 2026-11-21

### Adicionado
- Banner temporário "8 apps exclusivas Mainuan" (`banners/00-apps-exclusivas-mainuan.jpg`), mostrado como 2.º banner, logo a seguir ao BEM-VINDO, de 2026-11-21 até 2027-08-30 (configurado em `banners/banners.json`).
- Pasta `/appimage` na raiz do disco, criada na instalação.

### Alterado
- As AppImages passam de `~/AppImages` para `/appimage`. As que já existiam são migradas automaticamente.
- `/appimage` fica protegida enquanto houver AppImages configuradas na loja: dono root e atributo imutável, sem permissões para o utilizador apagar ou alterar pastas ou ficheiros. Adicionar, atualizar e remover AppImages passa pelo helper (pkexec).
- Ao desinstalar a loja, a proteção é retirada e a pasta é devolvida ao utilizador.
- Novo ícone: azul da app (`#0399b2` → `#02829a`) e saco branco maior.
- Nova dependência: `e2fsprogs` (chattr).

### Corrigido
- Idioma pt-BR: sistemas em português do Brasil eram detetados como pt-PT. A deteção percorre agora todas as entradas de `LANGUAGE`, aceita `pt-BR`, e distingue a região quando só vem `pt`.


## 🎉 Lançamento inicial --> [0.6.2] - 2026-11-19

### Estado da versão
- Instalação, atualização e remoção de aplicações a partir de APT, Flathub (Flatpak), AppImage e ficheiros DEB locais.
- Início com banner de boas-vindas, banners rotativos, aplicações exclusivas Mainuan e Ranking de Transferências.
- Explorar com catálogo de 42 aplicações em 13 categorias e pesquisa em APT, Flatpak e AppImage.
- Atualizações de APT, Flatpak, AppImage e firmware (LVFS, com `fwupd`), com aviso na área de notificações.
- Gestão de AppImage: instalar por ficheiro ou arrastando para a janela, integração no menu e atualização por URL (GitHub, GitLab, Codeberg ou ligação direta).
- Definições: fonte padrão, repositórios APT e Flatpak, atualizações de firmware e avisos de atualizações.
- Menu lateral reduzido ou expandido, com a escolha guardada.
- Operações de administrador através de polkit (`pkexec`) com um programa auxiliar que só aceita comandos permitidos.
- Interface em português (PT), português (BR), inglês, francês e espanhol.

## Author

Desenvolvido e mantido por David Caixinha

## Contribute

Para reportar erros ou pedir funcionalidades:
- **Issues**: https://github.com/mainuan/mainuan-store/issues
- **Discussions**: https://github.com/mainuan/mainuan-store/discussions
- **Email**: info@mainuanlinux.com

[0.6.2]: https://github.com/mainuan/mainuan-store/releases/tag/v0.6.2
