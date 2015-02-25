#!/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
import zipfile
import uuid
import re
from pyramid.response import Response
from ocscacicserver.model import session, tmp_dir
from logging import getLogger
from ocscacicserver.lib import conv

FILE_BEGIN = '{"results":['
FILE_END = '], "result_count": %s}'

# Computer class and properties filters
COMPUTER_FILTER = {
    "OperatingSystem": [
        "Caption".lower(),
        "Version".lower(),
        "InstallDate".lower()
    ],
    "Win32_Processor": [
        "Manufacturer".lower(),
        "Caption".lower(),
        "NumberOfLogicalProcessors".lower(),
        "MaxClockSpeed".lower(),
        "Family".lower()
    ],
    "Win32_BIOS": [
        "Manufacturer".lower(),
    ],
    "Win32_PhysicalMemory": [
        "MemoryType".lower(),
        "Capacity".lower()
    ],
    "Win32_DiskDrive": [
        "Caption".lower(),
        "Model".lower(),
        "Size".lower()
    ],
    "SoftwareList": []
}

FILTER_KEYS = str(tuple(COMPUTER_FILTER.keys()))

log = getLogger()


def viewcoleta(request):
    filename = tmp_dir + '/coleta-' + str(uuid.uuid4())
    json_file = filename + '.json'
    zip_file = filename + '.zip'
    # Please ensure this index exists on database
    # CREATE INDEX idx_id_computador ON computador_coleta(id_computador);
    if request.params.get('limit') is None:
        stmt1 = """
        SELECT h.id as hardware_id
        FROM hardware h
        ORDER BY h.id DESC;
        """
    else:
        stmt1 = """
            SELECT h.id as hardware_id
            FROM hardware h
            ORDER BY h.id DESC
            LIMIT {};
            """.format(request.params.get('limit'))

    computer_ids = session.execute(stmt1)

    stmt2 = """
        SELECT name
        FROM softwares
        WHERE hardware_id = {};
        """

    # FIXME: No momento ainda não estamos tratanto atributos multivalorados
    # Retornamos somente o primeiro valor
    stmt3 = """
        SELECT h.id as hardware_id,
                h.osname as operatingsystem_caption,
                h.osversion as operatingsystem_version,
                h.processort as win32_processor_caption,
                c.id as cpu_id,
                c.manufacturer as win32_processor_manufacturer,
                c.logical_cpus as win32_processor_numberoflogicalprocessors,
                c.speed as win32_processor_maxclockspeed,
                c.type as win32_processor_family,
                b.bmanufacturer as win32_bios_manufacturer,
                m.id as memory_id,
                m.type as win32_physicalmemory_memorytype,
                m.capacity as win32_physicalmemory_capacity,
                s.id as storage_id,
                s.name as win32_diskdrive_caption,
                s.model as win32_diskdrive_model,
                s.disksize as win32_diskdrive_size
        FROM hardware h
        LEFT JOIN cpus c ON h.id = c.hardware_id
        LEFT JOIN bios b ON b.hardware_id = h.id
        LEFT JOIN memories m ON h.id = m.hardware_id
        LEFT JOIN storages s ON h.id = s.hardware_id
        WHERE h.id = {}
        ORDER BY h.id DESC
        LIMIT 1
    """

    with open(json_file, 'w') as f:

        f.write(FILE_BEGIN)

        count = computer_ids.rowcount

        for computer in computer_ids.fetchall():

            software_list = session.execute(
                stmt2.format(computer.hardware_id, FILTER_KEYS)
            ).fetchall()

            computer_group = session.execute(
                stmt3.format(computer.hardware_id, FILTER_KEYS)
            ).first()

            computer_json = build_computer_json(computer_group, software_list)

            f.write(computer_json)
            count -= 1

            if count is not 0:
                f.write(',')

        f.write(FILE_END % computer_ids.rowcount)

    if '1' in tuple(request.params.get('zip', '0')):

        with zipfile.ZipFile(zip_file, 'w') as myzip:
            myzip.write(json_file)

        return Response(
            content_type='application/zip',
            content_disposition='filename=coleta.zip',
            body_file=open(zip_file, 'rb')
        )
    else:
        return Response(
            content_type='application/json',
            content_disposition='filename=coleta.json',
            body_file=open(json_file, 'rb')
        )


def build_computer_json(computer_group, software_list):

    convert = {
        'win32_processor_family': 'processor_converter',
        'win32_physicalmemory_memorytype': 'memory_converter'
    }

    computer = {
        "OperatingSystem".lower(): {},
        "Win32_Processor".lower(): {},
        "Win32_BIOS".lower(): {},
        "Win32_PhysicalMemory".lower(): {},
        "Win32_DiskDrive".lower(): {},
        "SoftwareList".lower(): []
    }

    # Primeiro trata dos softwares
    for software in software_list:
        if software.name.lower().find('office') > -1:
            # Adiciona somente os que forem Office
            computer["SoftwareList".lower()].append(software.name)

    for column in computer_group.keys():
        # Organiza um dicionário organizado por colunas
        regex = re.compile("^(.*)_(.+)$")
        r = regex.findall(column)
        if len(r) > 0:
            elm = r[0]
            class_ = elm[0]
            property_ = elm[1]
            value = computer_group[column]
            # Adiciona no JSON somente se a classe estiver registrada acima
            if class_ in computer.keys() and value is not None:
                # Corrige para transformar valores em inteiroes
                if type(value) != int and value is not None:
                    if value.isdigit():
                        value = int(value)

                if column in convert.keys():
                    # Executa funçao de conversao para atributo
                    func = getattr(conv, convert[column])
                    log.debug("Executando funçao de conversao para atributo %s", column)
                    value = func(value)

                computer[class_][column] = value

    return json.dumps(computer)
