__author__ = 'eduardo'


def processor_converter(value):
    """
    Converte a string no processor family do WMI

    :param value: valor a procurar
    :return: 2 (Unknown)
    """
    # FIXME: não encontrei uma forma de identificar o processor family no OCS

    return 2


def memory_converter(value):
    """
    Converte o valor recebido para um memorytype cadastrado

    :param value: valor lido pelo OCS
    :return: int
    """
    # FIXME: colocar todos os modelos aqui
    memory_types = {
        'Unknown': 0,
        'Other': 1,
        'DRAM': 2,
        'RAM': 9,
        'ROM': 10,
        'Flash': 11,
        'DDR': 20,
        'DDR-2': 21
    }

    saida = memory_types.get(value)
    if saida is None:
        # Retorna 0 como padrão
        saida = 0

    return saida