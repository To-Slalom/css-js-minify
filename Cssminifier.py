import sublime, sublime_plugin
import re , sys , os
# https://hastebin.com/ohaqisuver.py
# importante nome da Class tem de ser igual "command": "css_tominifier",
class CssTominifierCommand ( sublime_plugin.TextCommand ) :
    # desactivar botao caso nao seja ficheiros de css ou js
    def is_enabled ( self ) :
        return self.view.match_selector ( 0 , "source.css, source.js" )

    # funcao para minify o codigo de css ou js
    def minify ( self , file , ext ) :
        # HEX_PATTERN = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$";
        # shorten collapsable colors: #aabbcc to #abc
        all_hex = re.findall ( r'#[A-Fa-f0-9]{6}' , file , re.I )
        for new in all_hex :
            file = re.sub ( new , new[0]+new[1]+new[3]+new[5] , file )
        # remover todo tipo de comentarios
        file    = re.sub ( r'(/\*([^*]|(\*+([^*/])))*\*+/)|(\s//.*)' , '' , file )
        # remover todos os espacos a mais e quebras de linas
        file    = re.sub ( r'\t|\n|\r|\s\s+' , '' , file )
        # remover  todos os espacos em braco entre ()
        file    = re.sub ( r'(calc|translate[|X]|rgba|attr)+\(.*?\)' , lambda x: ''.join ( x.group ( 0 ).split ( ) ) , file )
        # criar ereg para o css e javascript em separados
        pattern = r'\s*(\=|\?|\[|\]|{|}|!|:|,|;|/|<|>|\|\||\(|\)|&&|!==)\s*' if ext == 'css' else r'\s*(\=|\+|\?|\[|\]|{|}|!|:|,|;|/|<|>|\|\||\(|\)|&&|!==)\s*'
        file    = re.sub ( pattern , r'\1' , file )
        lines   = []                        # meter tudo numa lista o css ou js limpo
        lines.append(file)                  # Adicionar todas as linhas
        return ''.join ( l for l in lines ) # Juntar tudo numa so linha

    def run ( self , edit ) :
        file_types_to_minify    = ['js', 'css']
        minify_ext              = ['min']
        # conteudo Selecionado 
        # selections = self.view.sel()
        # ler ficheiro todo
        content                 = self.view.substr ( sublime.Region ( 0 , len ( self.view ) ) )
        SplitWhat               = '\\' if sys.platform == 'win32' else '/'
        selections              = self.view.sel()
        file_name_parts         = self.view.file_name().split( '.' )
        current_file_and_path   = self.view.file_name()
        parts_of_file_and_path  = self.view.file_name().split( SplitWhat )
        current_file            = parts_of_file_and_path[-1]
        current_file_name       = current_file.split('.')[0]
        current_file_size       = self.view.size()
        current_file_ext        = file_name_parts[-1]
        current_path            = current_file_and_path.replace ( current_file , "" )
        full_file               = current_path + current_file_name +'.'+ minify_ext[0] + '.' + current_file_ext
        # print ( sublime.version() )     # prython version
        # print ( self.view.is_dirty() )  # True if file dont exist ned to be save 1
        # Create target Directory if don't exist
        #if self.view.is_dirty() == True :
        if not os.path.exists(current_path):
            # os.makedirs(name) will create the directory on given path,
            # also if any intermediate-level directory don’t exists then it will create that too.
            os.makedirs(current_path)
        # sublime.error_message( " PATH DONT EXIT save file first ")
        if current_file_ext in file_types_to_minify :                   # verificar se o script atual é css ou js
            minify_file = self.minify ( content , current_file_ext )    # defenir var com novo conteudo
            with open( full_file , 'w+' ) as min_file :                 # Abrir novo ficheiro e escrever
                min_file.write( minify_file )                           # escrever novo conteudo
            self.view.window().open_file( full_file )                   # abrir o novo ficheiro numa nova tab

        ############################################################################
        # Adiciona nova info na janela actual mas nao limpa a info antiga
        # view    = sublime.active_window()
        # view.run_command("append", {"characters": 'nova info'})
        ############################################################################
        ############################################################################
        # Abrir nova janela com o conteudo sem savar,...
        #
        # inside of a TextCommand, sefl.view represents the current file.
        # .window() is asking the current file to tell you what window it's in,
        #  and .new_file() asks that window to create a new file tab 
        #  (which is stored in the variable view so you can continue to access it)
        # 
        # view    = self.view.window().new_file()
        # # correr linha de commandoe enviar conteudo para la
        # view.run_command("append", {"characters": content})
        ############################################################################