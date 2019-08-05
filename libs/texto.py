import re
import os
import unicodedata

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TratamentoTexto:
    """
    Classe utilitária para realizar tratamentos no texto,
    uniformizar e eliminar palavras e símbolos dispensáveis.
    """

    re_padrao_horas = re.compile(r'(^|\b)(\d)+(h|hr|hrs)($|\b)', re.IGNORECASE)
    re_nomes_proprios = None
    re_stopwords = None
    re_contracoes = None
    re_numeros_por_extenso = None
    re_pronomes = None
    re_adverbios = None

    re_remover_espacos_excessivos = re.compile(' +')
    re_tratar_numeros = re.compile(r'([\d]+)([./-])*([\d ])')
    re_remover_numeros = re.compile(r'(^|\b)(\d+)(\b|$)')
    re_remover_urls = re.compile(r'[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?')

    @staticmethod
    def ler_dicionario(nome):
        path = os.path.join(BASE_DIR, 'dicionarios', nome)
        palavras = []
        with open(path, 'r', encoding='utf-8') as arq_dic:
            palavras = [p.replace('\n', '') for p in arq_dic]
        return palavras

    @staticmethod
    def stopwords():
        palavras = TratamentoTexto.ler_dicionario('stopwords_nltk.dic')
        complemento = [
            
        ]
        return palavras + complemento

    @staticmethod
    def remover_padroes_especificos(texto):
        return TratamentoTexto.re_padrao_horas.sub(' ', texto)

    @staticmethod
    def remover_nomes_proprios(texto):
        if not TratamentoTexto.re_nomes_proprios:
            palavras = TratamentoTexto.ler_dicionario('nomes_proprios.dic')
            TratamentoTexto.re_nomes_proprios = re.compile(r'(^|\b)(' + r'|'.join(palavras) + r')($|\b)')
        return TratamentoTexto.re_nomes_proprios.sub(' ', texto)

    @staticmethod
    def remover_pronomes(texto):
        if not TratamentoTexto.re_pronomes:
            palavras = TratamentoTexto.ler_dicionario('pronomes.dic')
            TratamentoTexto.re_pronomes = re.compile(r'(^|\b)(' + r'|'.join(palavras) + r')($|\b)')
        return TratamentoTexto.re_pronomes.sub(' ', texto)

    @staticmethod
    def remover_contracoes(texto):
        if not TratamentoTexto.re_contracoes:
            palavras = TratamentoTexto.ler_dicionario('contracoes.dic')
            TratamentoTexto.re_contracoes = re.compile(r'(^|\b)(' + r'|'.join(palavras) + r')($|\b)')
        return TratamentoTexto.re_contracoes.sub(' ', texto)

    @staticmethod
    def remover_adverbios(texto):
        if not TratamentoTexto.re_adverbios:
            palavras = TratamentoTexto.ler_dicionario('adverbios.dic')
            TratamentoTexto.re_adverbios = re.compile(r'(^|\b)(' + r'|'.join(palavras) + r')($|\b)')
        return TratamentoTexto.re_adverbios.sub(' ', texto)

    @staticmethod
    def remover_caracteres_especiais(texto):
        lista = u'-#?º°ª.:/;~^`[{]}\\|!$%"\'&*()=+,><\t\r\n…'
        resultado = texto
        for i in range(0, len(lista)):
            resultado = resultado.replace(lista[i], u' ')
        return resultado

    @staticmethod
    def remover_espacos_excessivos(texto):
        if texto is None or len(texto.strip()) == 0:
            # return texto
            return re.sub(' +', ' ', texto)
        return TratamentoTexto.re_remover_espacos_excessivos.sub(' ', texto)

    @staticmethod
    def remover_acentuacao(texto):
        if texto is None or len(texto.strip()) == 0:
            return texto
        resultado = texto
        resultado = unicodedata.normalize('NFKD', resultado).encode(
            'ASCII', 'ignore').decode('ASCII')
        return resultado

    @staticmethod
    def tratar_numeros(texto):
        resultado = texto
        # resultado = re.sub(r'([\d]+)([./-])*([\d ])', r'\1\3', resultado)
        resultado = TratamentoTexto.re_tratar_numeros.sub(r'\1\3', resultado)
        return resultado

    @staticmethod
    def remover_numeros(texto):
        resultado = texto
        # resultado = re.sub(r'(^|\b)(\d+)(\b|$)', r' ', resultado)
        resultado = TratamentoTexto.re_remover_numeros.sub(r' ', resultado)
        return resultado

    @staticmethod
    def remover_numeros_por_extenso(texto):
        if not TratamentoTexto.re_numeros_por_extenso:
            palavras = TratamentoTexto.ler_dicionario('numeros_por_extenso.dic')
            TratamentoTexto.re_numeros_por_extenso = re.compile(r'(^|\b)(' + r'|'.join(palavras) + r')($|\b)')
        return TratamentoTexto.re_numeros_por_extenso.sub(' ', texto)

    @staticmethod
    def remover_urls(texto):
        resultado = texto
        resultado = TratamentoTexto.re_remover_urls.sub(r' ', resultado)
        return resultado

    @staticmethod
    def remover_stopwords(texto):
        if not TratamentoTexto.re_stopwords:
            stopwords = TratamentoTexto.stopwords()
            TratamentoTexto.re_stopwords = re.compile(r'(^|\b)(' + r'|'.join(stopwords) + r')($|\b)')
        return TratamentoTexto.re_stopwords.sub(' ', texto)

    @staticmethod
    def tratar_texto(texto, remover_caracteres_especiais=True):
        if not texto or len(texto) == 0:
            return ''
			
        resultado = texto
        resultado = TratamentoTexto.remover_nomes_proprios(resultado)
        resultado = TratamentoTexto.remover_contracoes(resultado)
        resultado = TratamentoTexto.remover_pronomes(resultado)
        resultado = TratamentoTexto.remover_adverbios(resultado)
        resultado = TratamentoTexto.remover_numeros_por_extenso(resultado)
        resultado = TratamentoTexto.tratar_numeros(resultado)
        resultado = TratamentoTexto.remover_urls(resultado)
        resultado = resultado.lower()
        resultado = TratamentoTexto.remover_stopwords(resultado)
		
        if remover_caracteres_especiais:
            resultado = TratamentoTexto.remover_caracteres_especiais(resultado)
			
        resultado = TratamentoTexto.remover_acentuacao(resultado)
        resultado = TratamentoTexto.remover_numeros(resultado)
        resultado = TratamentoTexto.remover_espacos_excessivos(resultado)
        resultado = resultado.strip()
		
        return resultado
